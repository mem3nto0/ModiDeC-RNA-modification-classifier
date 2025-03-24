import pod5
from remora import io , refine_signal_map, util
import os
import numpy as np


def Remora_resquigle_Generation_data(data_path, bam_file, level_table_file, save_path, Variables, variables_segmentation, Indexes, mod_dictionary, ind_loop):

    #initial variable
    type_analysis = Variables[0]
    modified_data = Variables[1]
    take_mod_region = Variables[2]
    name_save_file = Variables[3]
    Modfied_base = Variables[4]
    mod_pos_initial = Variables[5]
    start_base_resquigle = Variables[6]

    #second variable for chunk size creations
    batch_size = variables_segmentation[0]
    max_label_length = variables_segmentation[1]
    time_segment = variables_segmentation[2]
    shift = variables_segmentation[3]

    # /////// read the files //////

    pod5_dr = pod5.DatasetReader(data_path)
    bam_fh = io.ReadIndexedBam(bam_file)

    # /////// take the name of reads////

    read_id = bam_fh.read_ids

    # /// define the function for resquile from Remora ///
    # // old version used for DNA. maybe DNA data has to be analysed again //

    sig_map_refiner = refine_signal_map.SigMapRefiner(
                        kmer_model_filename=level_table_file,
                        do_rough_rescale=True,
                        scale_iters=0,
                        do_fix_guage=True)
    
    if type_analysis == "mod_mapping":

        labels = len(mod_dictionary)

    if type_analysis == "basecalling":

        labels = 4

    start_Index = Indexes[0]

    for name_id in read_id[Indexes[0]: Indexes[1]]: #need to find a way to choose the ids.

        start_Index += 1
        print(start_Index)
        seq_resquigle = ""
        position_adjusting = 0
        Error_read = False

        # /// extract the select read and info from bam file ///

        pod5_read = pod5_dr.get_read(name_id)
        bam_read = bam_fh.get_first_alignment(name_id)

        # /// after extraction, obtain the basecalling information ///

        if bam_read.is_reverse: #correct the signal for forward direction
            flip = False
        else:
            flip = True

        try:
            #/// read data
            read_analysed = io.Read.from_pod5_and_alignment(pod5_read, bam_read, reverse_signal = flip)
            prob_ref = read_analysed.ref_seq
            prob_ref = probe_new_ref.replace("U", "T")
            read_analysed.ref_seq = prob_ref
            
            # // resquigle the data with the refence
            read_analysed.set_refine_signal_mapping(sig_map_refiner, ref_mapping=True)

            start_of_mapping = read_analysed.extract_ref_reg(
                read_analysed.ref_reg.adjust(start_adjust = 0, end_adjust=read_analysed.ref_reg.len))

            Raw_signal = start_of_mapping.norm_signal
            seq_resquigle = start_of_mapping.seq
            start_end_resquigle = start_of_mapping.seq_to_sig_map

            # /// check if the modification position has to be adjusted ///
            position_adjusting =start_of_mapping.ref_reg.start
            
        except:

            print("error")
            position_adjusting = 0
            seq_resquigle = ""
            Error_read = True

        """
        mod_pos = mod_pos_initial - position_adjusting - 1            
        max_signal_length = Raw_signal[0 : mod_pos + time_segment]
        """
        
        val_total_seq = position_adjusting + len(seq_resquigle)
        high_threshold = mod_pos_initial + 20
        
        # // select only high score quality, extrapolate signal and save data //

        start_analysis = False

        if take_mod_region == True:

            if high_threshold < val_total_seq and position_adjusting < mod_pos_initial and Error_read == False: 

                start_analysis = True

        else:

            if  Error_read == False:

                    start_analysis = True


        if  start_analysis == True: # ///////// TO CHECK !!! ////////////

            Signal_onehot = np.zeros([len(Raw_signal),4 + 1])
            Output_onehot = np.zeros([len(Raw_signal), labels + 2])

            mod_pos = mod_pos_initial - position_adjusting - 1            

            if modified_data == True:

                seq_resquigle_mod = seq_resquigle[:mod_pos] + "X" + seq_resquigle[mod_pos +1:] 

            else:

                seq_resquigle_mod = seq_resquigle

            if type_analysis == "mod_mapping":
                
                #modification_dict = {"G":2, "M":3, "I":4, "P":5}
                value_modification = int(mod_dictionary[Modfied_base])
                base_dict_output = { "A":1, "C":1, "G":1, "T":1,"X":value_modification} # variable

            if type_analysis == "basecalling":

                base_dict_output = { "A":1, "C":2, "G":3, "T":4, "X":5}
                
            base_dict = {"A":1, "C":2, "G":3, "T":4}

            try:

                for k in range(len(seq_resquigle)):

                    start_resq = start_end_resquigle[k]
                    Signal_onehot[start_resq,base_dict[seq_resquigle[k]]] = 1
                    Output_onehot[start_resq,base_dict_output[seq_resquigle_mod[k]]] = 1

                if type_analysis == "mod_mapping" and modified_data == True:

                    mod_position = np.where(Output_onehot[:,value_modification] > 0)[0][0]

                if type_analysis == "mod_mapping" and modified_data == False:

                    if take_mod_region == True:

                        mod_position = np.where(Output_onehot[:,1] > 0)[0][mod_pos]

                    else:
                        
                        mod_position = 0
                        
                if type_analysis == "basecalling" and modified_data == True:

                    mod_position = np.where(Output_onehot[:,5] > 0)[0][0]

                if type_analysis == "basecalling" and modified_data == False: # to check for the others

                    if take_mod_region == True:

                        mod_position = np.where(Output_onehot[:,1] > 0)[0][mod_pos]

                    else:
                        
                        mod_position = 0

                if take_mod_region == True:

                    minus_start = np.abs(start_end_resquigle[mod_pos - start_base_resquigle] - mod_position)

                    N_shift = int((time_segment + minus_start)/shift)

                else:

                    N_shift = int((len(Raw_signal) - time_segment)/shift)

                for n in range(int(N_shift/batch_size)):

                    train1_batch = np.zeros([batch_size, time_segment])
                    train2_batch = np.zeros([batch_size, max_label_length, 4])
                    output_batch = np.zeros([batch_size, max_label_length, 1 + labels])

                    for m in range(batch_size):

                        if take_mod_region == True:
                            
                            midlle_mod_position = mod_position #+ int(0.5*np.abs(start_end_resquigle[mod_pos + 1] - start_end_resquigle[mod_pos]))
                            start = midlle_mod_position - n*batch_size*shift - m*shift
                            end = start + time_segment

                        else:

                            start = n*batch_size*shift + m*shift
                            end = start + time_segment

                        output_for_batch = np.zeros([max_label_length,1 + labels])
                        train2_for_batch = np.zeros([max_label_length,4])

                        # // here I am using a trick. All the bases has no zero value
                        # making again the one-hot into an array and removing the 0 values,
                        # I obtain the index of the final one-hot sequence for train2 and output

                        probe_1 = np.argmax(Signal_onehot[start:end,:], axis = -1)
                        probe_1 = probe_1[probe_1 != 0]
                        probe_1 = probe_1 - 1

                        probe_2 = np.argmax(Output_onehot[start:end,:], axis = -1)
                        probe_2 = probe_2[probe_2 != 0]
                        probe_2 = probe_2 - 1

                        try:

                            for kk in range(len(probe_1)):
                                
                                train2_for_batch[kk, probe_1[kk]] = 1
                                output_for_batch[kk, probe_2[kk]] = 1

                        except:

                            for kk in range(max_label_length):
                                
                                train2_for_batch[kk, probe_1[kk]] = 1
                                output_for_batch[kk, probe_2[kk]] = 1

                        # try/expect is places for data that are too short for storage
                        # the problem is only related to modified data.

                        try:

                            train1_batch[m] = Raw_signal[start:end]
                            train2_batch[m] = train2_for_batch
                            output_batch[m] = output_for_batch

                        except:

                            if mod_position < int(time_segment/2):                            
                                start = mod_position
                                end = start + time_segment

                            else:     
                                start = mod_position - int(time_segment/2)
                                end = start + time_segment

                            probe_1 = np.argmax(Signal_onehot[start:end,:], axis = -1)
                            probe_1 = probe_1[probe_1 != 0]
                            probe_1 = probe_1 - 1

                            probe_2 = np.argmax(Output_onehot[start:end,:], axis = -1)
                            probe_2 = probe_2[probe_2 != 0]
                            probe_2 = probe_2 - 1

                            try:

                                for kk in range(len(probe_1)):
                                    
                                    train2_for_batch[kk, probe_1[kk]] = 1
                                    output_for_batch[kk, probe_2[kk]] = 1

                            except:

                                for kk in range(max_label_length):
                                    
                                    train2_for_batch[kk, probe_1[kk]] = 1
                                    output_for_batch[kk, probe_2[kk]] = 1

                            train1_batch[m] = Raw_signal[start:end]
                            train2_batch[m] = train2_for_batch
                            output_batch[m] = output_for_batch

                    file_name = name_save_file + f"{int(ind_loop)}_{int(start_Index)}" + f"_{n}.npz"

                    np.savez_compressed(os.path.join(save_path,file_name), 
                                        train_input = train1_batch,
                                        train_input2 = train2_batch,
                                        train_output = output_batch)
                                            
            # // save long rads enter in the quality check. maybe is not necessary

            
            except:
                print("resquigle error")
            
