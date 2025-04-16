from tensorflow import keras
import numpy as np
import os

class Load_data_RNA(keras.utils.Sequence):

    """generate data in sequence mode for training the neural network"""

    def __init__(self, batch_size, N_batches, path, files_list, chunck_size, labels, batch_loading, max_seq_len):

        self.batch_size = batch_size
        self.N_batches = N_batches
        self.batch_loading = batch_loading

        self.X_train = np.zeros([self.batch_size,chunck_size,1])
        self.X_train2 = np.zeros([self.batch_size,max_seq_len,4,1])
        self.labels = np.zeros([self.batch_size,max_seq_len,labels])

        # The set of characters accepted in the transcription.
        self.path = path
        self.files_list = files_list
        self.ind_rand = np.arange(0,self.N_batches,1)
        np.random.shuffle(self.ind_rand)
        np.random.shuffle(self.files_list)

    def __len__(self):
        '''
        Denotes the number of batches per epoch
        '''
        return int(self.N_batches)
    
    def __getitem__(self, index):
 
        selected_ind = self.ind_rand[index]

        const = self.batch_loading 

        for i in range(int(self.batch_size/const)):

            try:
                with np.load(self.path + "/" + self.files_list[int(self.batch_size/const)*selected_ind + i]) as data:
                    
        
                    new_x_train = data["train_input"]
                    new_x_train2 = data["train_input2"]
                    y_train = data["train_output"]

            except:

                with np.load(self.path + "/" + self.files_list[0]) as data:
                            
                    new_x_train = data["train_input"]
                    new_x_train2 = data["train_input2"]
                    y_train = data["train_output"]

            self.X_train[i*const:(i+1)*const,:,0] = new_x_train
            self.X_train2[i*const:(i+1)*const,:,:,0] = new_x_train2

            self.labels[i*const:(i+1)*const,:,:] = y_train 

        X_total = {
            "Input_1": self.X_train,
            "Input_2": self.X_train2
            }
            
        return X_total,  self.labels


    def on_epoch_end(self):
        """Shuffle indices after each epoch"""
        np.random.shuffle(self.ind_rand)   
