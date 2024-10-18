#%%
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLineEdit, QLabel, QHBoxLayout, QCheckBox
from Remora_resquigle_generate_data import Remora_resquigle_Generation_data
import json
import os
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # list of variables
        self.paths = {"folder1": None, "folder2": None, "folder3": None, "folder4": None, "folder5": None}

        # Set up the main window
        self.setWindowTitle('Remora Resquigle - Generata training data for NN')
        self.setGeometry(100, 100, 320, 100)

        # Create a QWidget and set it as the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create buttons and add them to the layout
        self.button1 = QPushButton('Pod5 file folder')
        self.button1.clicked.connect(lambda: self.open_directory_dialog('folder1'))
        layout.addWidget(self.button1)

        self.button2 = QPushButton('bam file folder')
        self.button2.clicked.connect(lambda: self.open_directory_dialog('folder2'))
        layout.addWidget(self.button2)

        self.button3 = QPushButton('Save path')
        self.button3.clicked.connect(lambda: self.open_directory_dialog('folder4'))
        layout.addWidget(self.button3)

        self.button3 = QPushButton('kmer-level table file')
        self.button3.clicked.connect(lambda: self.open_filename_dialog('folder5'))
        layout.addWidget(self.button3)

        # set the first set of variables
        textbox1 = QLabel("General variables for training data:")
        layout.addWidget(textbox1)
        self.setup_variables(layout)

        # set the second set of variables
        textbox1 = QLabel("segmentation variables for training data:")
        layout.addWidget(textbox1)
        self.setup_variables_segmentation(layout)

        # Create buttons and add them to the layout
        self.button4 = QPushButton('Start resquigle')
        self.button4.clicked.connect(lambda: self.start_resquigle())
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


    def open_filename_dialog(self, file_type):
        # Open a dialog to choose a file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, f"Select {file_type}", "", "All Files (*);;FASTA Files (*.fasta)", options=options)        
        if file_name:
            self.paths[file_type] = file_name
            print(f"Selected path for {file_type}: {file_name}")

    def setup_variables(self, layout):
        # Creating layout and widgets for each variable in Variables tuple # "mod_mapping or basecalling?", 
        labels = ["modified_data? (bool)", 
                  "take_modifed_region? (bool)", "name_save_file (str)", 
                  "what type of modification? (str)", 
                  "modification pos. (int)", "Bases before modfication (int)", "modification dictionary (str)"]
        
        self.vars_entries = ["mod_mapping"] # "mod_mapping"
        for i, label in enumerate(labels):
            row_layout = QHBoxLayout()
            label_widget = QLabel(label + ":")
            input_widget = QLineEdit()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_widget)
            layout.addLayout(row_layout)
            self.vars_entries.append(input_widget)


    def setup_variables_segmentation(self, layout):
        labels_segmentation = ["batch size (int)", "max seq. length (int)", 
                               "chunk length (int)", "shift in time (int)", 
                               "start read number (int)", "end read number (int)"]
        
        self.segmentation_entries = []
        for label in labels_segmentation:
            row_layout = QHBoxLayout()
            label_widget = QLabel(label + ":")
            input_widget = QLineEdit()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_widget)
            layout.addLayout(row_layout)
            self.segmentation_entries.append(input_widget)

    """ """
    def start_resquigle(self):

        #level_table_folder = self.paths["folder5"]
        #level_table_list = os.listdir(level_table_folder) #maybe to change to read the file and not the folder                
        #level_table_file = level_table_folder + "/" + level_table_list[0]

        level_table_file = self.paths["folder5"]

        save_path = self.paths["folder4"]

        pod5_folder = self.paths["folder1"]
        bam_folder = self.paths["folder2"]
        bam_list = os.listdir(bam_folder)

        var1_bool = []
        var2_bool = []

        if self.vars_entries[1].text() == "yes" or self.vars_entries[1].text() == "Yes":
            
            var1_bool = True

        else:

            var1_bool = False


        if self.vars_entries[2].text() == "yes" or self.vars_entries[2].text() == "Yes":
            
            var2_bool = True

        else:

            var2_bool = False


        Variables = (self.vars_entries[0], #.text()
                     var1_bool, #bool, 
                     var2_bool, #bool, 
                     self.vars_entries[3].text(), 
                     self.vars_entries[4].text(),
                     int( self.vars_entries[5].text()), 
                     int( self.vars_entries[6].text())
                     )

        variables_segmentation = (int( self.segmentation_entries[0].text()), 
                                  int( self.segmentation_entries[1].text()), 
                                  int( self.segmentation_entries[2].text()), 
                                  int( self.segmentation_entries[3].text())
                                  )

        Indexes = (int( self.segmentation_entries[4].text()),
                    int( self.segmentation_entries[5].text()))

        # /// create a dictionary ///

        probe_names = self.vars_entries[7].text()
        probe_names = probe_names.split(',')

        values = np.arange(2, len(probe_names) + 2, 1)

        # Convert the list into a dictionary with default values
        mod_dictionary = {probe_names[i]: values[i] for i in range(len(probe_names))}


        print(mod_dictionary)
        print(Variables)
        print(variables_segmentation)
        print(Indexes)
         
        for i in range (len(bam_list)):

            bam_file = bam_folder + "/" +  bam_list[i]
            
            Remora_resquigle_Generation_data(pod5_folder, bam_file, 
                                             level_table_file, save_path,
                                             Variables, variables_segmentation, 
                                             Indexes, mod_dictionary, i)

            """
            # /// save each bam file in a different generated folder
            bam_file = bam_folder + "/" +  bam_list[i]
            
            #this creates several folder and save inside the data
            Directory = self.vars_entries[3].text() + f"reference_{i}"
            Final_path = os.path.join(save_path, Directory) 
            os.mkdir(Final_path)

            Remora_resquigle_Generation_data(pod5_folder, bam_file, 
                                             level_table_file, Final_path, #save_path
                                             Variables, variables_segmentation, 
                                             Indexes, mod_dictionary, i)            
            """
            
        print("Resquigle finished")                     

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()