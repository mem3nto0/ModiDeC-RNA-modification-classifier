import tensorflow as tf
import numpy as np
import pod5
from remora import io
import matplotlib.pyplot as plt

def NN_analyzer(variables, pod5_dr, bam_fh, read_id, sig_map_refiner, model, reference, labels_mod = 4):

    chunck_size = variables[2]
    max_seq_len = variables[3]
    labels = 4
    N_miss = 0
    
    reference_track_mod = np.zeros([len(reference), labels_mod])     

    if variables[1] == -1:

        variables[1] = len(read_id)

    if len(read_id) > variables[1]:

        end_reads = variables[1]

    else:
        end_reads = len(read_id)

    if end_reads < variables[0]:

        if end_reads - np.abs(variables[0] - variables[1]) < 0:
            start_reads = 0
    
        else:
            start_reads = end_reads - np.abs(variables[0] - variables[1])

    else:
        start_reads = variables[0]

    #print(len(read_id))
    #print(start_reads, end_reads)

    for name_id in read_id[start_reads: end_reads]:

        pod5_read = pod5_dr.get_read(name_id)
        bam_read = bam_fh.get_first_alignment(name_id)

        seq_resquigle = ""
        position_adjusting = 0
        Error_read = False

        if bam_read.is_reverse: #correct the signal for forward direction
            flip = False
        else:
            flip = True

        try:
            #/// read data
            read_analysed = io.Read.from_pod5_and_alignment(pod5_read, bam_read, reverse_signal = flip)
            
            #/// If data were aligned with U, U in sequence will be replaced by the T. Important for resquiggle
            prob_ref = read_analysed.ref_seq
            prob_ref = prob_ref.replace("U", "T")
            read_analysed.ref_seq = prob_ref
            
            # // resquigle the data with the reference
            read_analysed.set_refine_signal_mapping(sig_map_refiner, ref_mapping=True)
            
            start_of_mapping = read_analysed.extract_ref_reg(
                read_analysed.ref_reg.adjust(start_adjust = 0, end_adjust=read_analysed.ref_reg.len))

            Raw_signal = start_of_mapping.norm_signal
            seq_resquigle = start_of_mapping.seq
            start_end_resquigle = start_of_mapping.seq_to_sig_map

            # /// check if the modification position has to be adjusted ///
            position_adjusting = start_of_mapping.ref_reg.start
        
        except:
            position_adjusting = 0
            seq_resquigle = ""
            Error_read = True
        
        if Error_read == False:
            
            base_dict = {"A":1, "C":2, "G":3, "T":4}
            bases_onehot = np.zeros([len(Raw_signal),4 + 1])

            try:

                for k in range(len(seq_resquigle)):

                    start_resq = start_end_resquigle[k]
                    bases_onehot[start_resq,base_dict[seq_resquigle[k]]] = 1


                N_segments = int(len(Raw_signal)/chunck_size)
                Input_1 = np.zeros([N_segments +1,chunck_size])            # initialize the first input of the NN
                Input_2 = np.zeros([N_segments +1,max_seq_len,labels])     # initialize the second input of the NN

                for k in range (N_segments):

                    start = k*chunck_size
                    Input_1[k] = Raw_signal[start: start + chunck_size]

                    window_onehot = bases_onehot[start: start + chunck_size,:]
                    probe = np.argmax(window_onehot, axis=-1)
                    probe = probe[probe != 0]
                    probe = probe -1

                    for kk in range(len(probe)):

                        Input_2[k, kk, probe[kk]] = 1

                #find the number of point not overlapping
                not_overlaping_last_seg = len(Raw_signal) - (start + chunck_size)

                # the extention to +1 is for keeping the full dimention of the output
                Input_1[N_segments] = Raw_signal[-chunck_size:]

                Additional_window = bases_onehot[-chunck_size:,:]
                probe = np.argmax(Additional_window, axis = -1)
                probe = probe[probe != 0]
                probe = probe - 1

                for kk in range (len(probe)):

                    Input_2[N_segments, kk, probe[kk]] = 1 

                #probe the overlapping bases for the last segment
                Window_overlap = bases_onehot[-chunck_size:-not_overlaping_last_seg,:]
                seq_overlap = np.zeros([Window_overlap.shape[0],4])
                probe = np.argmax(Window_overlap, axis = -1)
                probe = probe[probe != 0]
                probe = probe - 1

                for kk in range (len(probe)):

                    seq_overlap[kk, probe[kk]] = 1 

                seq_overlap = np.sum(seq_overlap, axis = 1)
                seq_overlap = np.where(seq_overlap > 0.5)[0] 
                len_overlap = len(seq_overlap)

                Input_1 = np.expand_dims(Input_1, axis=-1) 
                #Input_2 = np.expand_dims(Input_2, axis=-1) 

                X_total ={"Input_1": Input_1, "Input_2": Input_2}

                #analyze the read with the NN

                prediction = model.predict(X_total, verbose=0) #  

                # reconstruct the final output removing the null part of the predictions
                Final_seq_binary = []

                for kk in range(N_segments): #

                    full_position = np.sum(prediction[kk], axis = 1)
                    full_position = np.where(full_position> 0.5)[0]

                    real_part =  np.argmax(prediction[kk,:len(full_position)], axis=-1)
                    Final_seq_binary = np.concatenate((Final_seq_binary,real_part), axis=0)

                full_position = np.sum(prediction[N_segments], axis = 1)
                full_position = np.where(full_position> 0.5)[0]

                real_part = np.argmax(prediction[N_segments,:len(full_position)], axis=-1)
                not_overlaping_part = real_part[len_overlap:]
                Final_seq_binary = np.concatenate((Final_seq_binary,not_overlaping_part), axis=0)

                if (len(Final_seq_binary) - len(seq_resquigle)) != 0:

                    N_miss += 1

                else:

                    where_mod = np.where(Final_seq_binary >= 1)[0]
                    modific_detec = np.zeros(len(where_mod))

                    for j in range(len(where_mod)):

                        modific_detec[j] = Final_seq_binary[where_mod[j]]
                
                    if len(modific_detec) > 1:

                        for n in range(len(modific_detec)):

                            mod_probe_position = where_mod[n]
                            mod_probe_predicted = modific_detec[n]

                            reference_track_mod[int(mod_probe_position) + int(position_adjusting), int(mod_probe_predicted -1)] += 1

                    else:

                        mod_probe_position = where_mod[0]
                        mod_probe_predicted = modific_detec[0]

                        reference_track_mod[int(mod_probe_position) + int(position_adjusting), int(mod_probe_predicted -1)] += 1   

            except:

                None
   
   
    print("analysis finished")
    print("Total data to analyize:", np.abs(end_reads - start_reads))
    print("data analyized:", np.abs(end_reads - start_reads) - N_miss)

    #return reference_track_mod   

    # /// calculate the modification frequency lust by the number or reads analyzed///

    return (reference_track_mod)/(np.abs(end_reads - start_reads - N_miss))
