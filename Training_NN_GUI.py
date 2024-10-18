import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLineEdit, QLabel, QHBoxLayout, QCheckBox
import tensorflow as tf
from keras.callbacks import LearningRateScheduler
from Load_data_for_training_V2 import  Load_data_RNA
from ModiDec_NN import ModiDeC_model
import os
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # list of variables
        self.paths = {"folder1": None, "folder2": None , "folder3": None}

        # Set up the main window
        self.setWindowTitle("Training Nueral network - modification classifier")
        self.setGeometry(100, 100, 320, 100)

        # Create a QWidget and set it as the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create buttons and add them to the layout
        self.button1 = QPushButton('training data folder')
        self.button1.clicked.connect(lambda: self.open_directory_dialog('folder1'))
        layout.addWidget(self.button1)

        # Create buttons and add them to the layout
        self.button2 = QPushButton('Validation data folder')
        self.button2.clicked.connect(lambda: self.open_directory_dialog('folder2'))
        layout.addWidget(self.button2)

        self.button3 = QPushButton('save model folder')
        self.button3.clicked.connect(lambda: self.open_directory_dialog('folder3'))
        layout.addWidget(self.button3)

        # set the first set of variables
        textbox1 = QLabel("General variables for training data:")
        layout.addWidget(textbox1)
        self.setup_variables(layout)

        # Create buttons and add them to the layout
        self.button4 = QPushButton('Start training')
        self.button4.clicked.connect(lambda: self.start_training())
        layout.addWidget(self.button4)

        # Set the layout on the central widget
        self.central_widget.setLayout(layout)


    """ list of function used in the main"""

    def open_directory_dialog(self, folder_name):
        # Open a dialog to choose a directory
        directory = QFileDialog.getExistingDirectory(self, f"Select {folder_name}")
        if directory:
            self.paths[folder_name] = directory
            print(f"Selected path for {folder_name}: {directory}")

    """
    labels = ["chunck_size (int)", "batch_size (int)", 
                "single_data_size (int)", "max seq. length (int)", "k-mer model (int)",
                "labels (int)", "epoches (suggeste 4) (int)", "name NN (str)" ]
    """

    def setup_variables(self, layout):
        # Creating layout and widgets for each variable in Variables tuple
        labels = ["batch_size (int)", "k-mer model (int)", "epoches (suggeste 4) (int)", "name NN (str)", "validation during training? (bool)" ]
        
        self.vars_entries = []
        for i, label in enumerate(labels):
            row_layout = QHBoxLayout()
            label_widget = QLabel(label + ":")
            input_widget = QLineEdit()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_widget)
            layout.addLayout(row_layout)
            self.vars_entries.append(input_widget)

    def start_training(self):

        """load the variables"""

        path_data = self.paths["folder1"]
        data_list = os.listdir(path_data)


        path_eval = self.paths["folder2"]
        eval_list = os.listdir(path_data)

        var1_bool = []

        # //// extract variable for training from data training datasets ///

        probe_data = np.load(path_data + "/" + data_list[0])

        probe_x1_data = probe_data["train_input"]
        probe_y_data = probe_data["train_output"]

        chunck_size = int(probe_x1_data.shape[1])
        single_data_size = int(probe_x1_data.shape[0])
        labels = int(probe_y_data.shape[2])
        max_seq_len = int(probe_y_data.shape[1])

        batch_size = int(self.vars_entries[0].text())
        k_mer = int( self.vars_entries[1].text())
        N_epoch = int( self.vars_entries[2].text())

        "validation during training? (bool)" 

        if self.vars_entries[4].text() == "yes" or self.vars_entries[4].text() == "Yes":
            
            var1_bool = True

        else:

            var1_bool = False


        """ /////define the model /////"""

        model = ModiDeC_model(Inp_1 = chunck_size, Inp_2 = max_seq_len, labels = labels, kmer_model=k_mer)

        """ /////compile the model for the training ///"""

        opt_adam =tf.keras.optimizers.Adam(learning_rate= 0.0001)

        model.compile(optimizer=opt_adam, 
                loss= tf.losses.binary_crossentropy, 
                metrics=["accuracy"])

        def lr_schedule(epoch, optimizer):

            min_lr = 0.0000125  # Set the minimum learning rate

            # Update the learning rate if needed (similar to your original code)       
            if epoch % 2 == 0 and epoch > 0:

                new_lr = tf.keras.backend.get_value(model.optimizer.lr) * 0.5  # You can adjust the decay factor as needed
                model.optimizer.lr.assign(new_lr)
                return max(new_lr, min_lr)
            
            else:
                return tf.keras.backend.get_value(model.optimizer.lr)
    
        lr_scheduler = LearningRateScheduler(lambda epoch: lr_schedule(epoch, optimizer=opt_adam))

        if var1_bool == False: 

            N_batches = int(len(data_list)/(batch_size/single_data_size))

            """loading function used for training"""

            training_generator =  Load_data_RNA(batch_size, N_batches,
                                                path_data, 
                                                data_list, 
                                                chunck_size = chunck_size, 
                                                labels= labels , 
                                                batch_loading = single_data_size,
                                                max_seq_len= max_seq_len)

            """start the training"""

            model.fit(training_generator, 
                        shuffle = True, 
                        epochs=N_epoch, 
                        workers= 6, 
                        max_queue_size=128,
                        callbacks= [lr_scheduler]) 

            """save the model"""

            model.save( self.paths["folder3"] + "/" + self.vars_entries[3].text())

            print("training complete")

        else: 

            N_batches = int(len(data_list)/(batch_size/single_data_size))
            N_batches_2 = int(len(eval_list)/(batch_size/single_data_size))

            """loading function used for training"""

            training_generator =  Load_data_RNA(batch_size, N_batches,
                                                path_data, 
                                                data_list, 
                                                chunck_size = chunck_size, 
                                                labels= labels , 
                                                batch_loading = single_data_size,
                                                max_seq_len= max_seq_len)

            validation_generator =  Load_data_RNA(batch_size, N_batches_2,
                                                path_eval, 
                                                eval_list, 
                                                chunck_size = chunck_size, 
                                                labels= labels, 
                                                batch_loading = single_data_size,
                                                max_seq_len= max_seq_len)

            """start the training"""

            model.fit(training_generator, 
                        validation_data = validation_generator,
                        shuffle = True, 
                        epochs=N_epoch, 
                        workers= 6, 
                        max_queue_size=256,
                        callbacks= [lr_scheduler]) 

            """save the model"""

            model.save( self.paths["folder3"] + "/" + self.vars_entries[3].text())

            print("training complete")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
