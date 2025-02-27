
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QLineEdit, QHBoxLayout , QFileDialog
from PyQt5.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pod5
from remora import io , refine_signal_map, util
import tensorflow as tf
from Analyze_data_NN import NN_analyzer


""" to generate a window into a window two main class has to be defined"""
""" second window generator"""
class RNA_analysis_platform(QWidget):
    def __init__(self, Analysis_NN):
        super().__init__()
        
        self.Analysis_NN  = Analysis_NN
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.start_label = QLabel('Start Point:')
        self.end_label = QLabel('End Point:')
        self.start_input = QLineEdit(self)
        self.end_input = QLineEdit(self)
        self.start_slider = QSlider(Qt.Horizontal, self)
        self.end_slider = QSlider(Qt.Horizontal, self)
        
        self.start_input.setText('0')
        self.end_input.setText('10')
        self.start_slider.setMinimum(0)
        self.start_slider.setMaximum(self.Analysis_NN.shape[0])
        self.start_slider.setValue(0)
        self.end_slider.setMinimum(0)
        self.end_slider.setMaximum(self.Analysis_NN.shape[0])
        self.end_slider.setValue(10)

        self.start_input.textChanged.connect(self.update_start_slider)
        self.end_input.textChanged.connect(self.update_end_slider)
        self.start_slider.valueChanged.connect(self.update_start_input)
        self.end_slider.valueChanged.connect(self.update_end_input)

        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.start_label)
        self.hbox1.addWidget(self.start_input)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.end_label)
        self.hbox2.addWidget(self.end_input)

        self.layout.addLayout(self.hbox1)
        self.layout.addWidget(self.start_slider)
        self.layout.addLayout(self.hbox2)
        self.layout.addWidget(self.end_slider)

        self.plot_button = QPushButton('Plot', self)
        self.plot_button.clicked.connect(self.plot)

        self.layout.addWidget(self.plot_button)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

    def update_start_slider(self, text):
        try:
            value = int(text)
            self.start_slider.setValue(value)
        except ValueError:
            pass

    def update_end_slider(self, text):
        try:
            value = int(text)
            self.end_slider.setValue(value)
        except ValueError:
            pass

    def update_start_input(self, value):
        self.start_input.setText(str(value))

    def update_end_input(self, value):
        self.end_input.setText(str(value))

    def plot(self):
        start = int(self.start_input.text())
        end = int(self.end_input.text())

        x_axis = np.arange(0,self.Analysis_NN.shape[0],1)

        self.ax.clear()

        """
        self.ax.plot(x_axis,self.Analysis_NN[:,0], marker= "o" , label="Gm")
        self.ax.plot(x_axis,self.Analysis_NN[:,1], marker= "o"  , label="$m^6A$")
        self.ax.plot(x_axis,self.Analysis_NN[:,2], marker= "o"  , label="Ino")
        self.ax.plot(x_axis,self.Analysis_NN[:,3], marker= "o"  , label="Psi")
        """
        self.ax.plot(x_axis,self.Analysis_NN, marker= "o" , label="label")

        self.ax.set_xlim(start,end)
        self.ax.set_ylim(-0.05,1)
        #ax2.set_xlim(0,len(reference)) #len(reference)
        self.ax.set_xlabel("ref. seq. position")
        self.ax.set_ylabel("freq. modif.")
        self.ax.legend()
        self.canvas.draw()


""" first window generator"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # list of variables
        self.paths = {"folder1": None, "folder2": None, "folder3": None, "folder4": None, "folder5": None}

        # Set up the main window
        self.setWindowTitle('Analysis data Neural network')
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

        self.button2 = QPushButton('bam file')
        self.button2.clicked.connect(lambda: self.open_filename_dialog('folder2'))
        layout.addWidget(self.button2)

        self.button3 = QPushButton('Neural Network folder')
        self.button3.clicked.connect(lambda: self.open_directory_dialog('folder3'))
        layout.addWidget(self.button3)

        self.button4 = QPushButton('kmer-level table file')
        self.button4.clicked.connect(lambda: self.open_filename_dialog('folder4'))
        layout.addWidget(self.button4)

        self.button4 = QPushButton('reference')
        self.button4.clicked.connect(lambda: self.open_filename_dialog('folder5'))
        layout.addWidget(self.button4)

        self.button4 = QPushButton('Initialize the data')
        self.button4.clicked.connect(lambda: self.Initialize_Analysis())
        layout.addWidget(self.button4)

        # set the first set of variables
        textbox1 = QLabel("General variables for the analysis:")
        layout.addWidget(textbox1)
        self.setup_variables(layout)

        self.button4 = QPushButton('start analysis with Neural network')
        self.button4.clicked.connect(lambda: self.Analysis_Neural_network())
        layout.addWidget(self.button4)

        self.button4 = QPushButton('Visualize results')
        self.button4.clicked.connect(lambda: self.open_visualization_results())
        layout.addWidget(self.button4)

        # Set the layout on the central widget
        self.central_widget.setLayout(layout)


    """ list of function used in the mainWindow"""

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
        # Creating layout and widgets for each variable in Variables tuple
        labels = ["start_index", "end_index"]
        
        self.vars_entries = []
        for i, label in enumerate(labels):
            row_layout = QHBoxLayout()
            label_widget = QLabel(label + ":")
            input_widget = QLineEdit()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_widget)
            layout.addLayout(row_layout)
            self.vars_entries.append(input_widget)


    def Initialize_Analysis(self):

        pod5_path = self.paths["folder1"]
        bam_pathr = self.paths["folder2"]
        model_path = self.paths["folder3"]
        level_table_file = self.paths["folder4"]

        self.pod5_dr = pod5.DatasetReader(pod5_path)
        self.bam_fh = io.ReadIndexedBam(bam_pathr)

        self.read_id = self.bam_fh.read_ids

        self.sig_map_refiner = refine_signal_map.SigMapRefiner(
                    kmer_model_filename=level_table_file,
                    do_rough_rescale=True,
                    scale_iters=0,
                    do_fix_guage=True)

        self.NN_model = tf.keras.models.load_model(model_path)

        input_shapes = self.NN_model.input_shape
        output_shape = self.NN_model.output_shape
        
        self.chunck_size = int(input_shapes[0][1])
        self.max_seq_len = int(input_shapes[1][1])
        self.total_mod = output_shape[2] - 1

        print("initialize: Done")

    def Analysis_Neural_network(self):

        Variables = (int(self.vars_entries[0].text()), 
                     int(self.vars_entries[1].text()), 
                     int(self.chunck_size), 
                     int(self.max_seq_len))


        reference_path = self.paths["folder5"]
        reference = open(reference_path)
        reference = reference.read()

        self.Analysis_NN = NN_analyzer(Variables, 
                                            self.pod5_dr, 
                                            self.bam_fh, 
                                            self.read_id, 
                                            self.sig_map_refiner, 
                                            self.NN_model, 
                                            reference,
                                            labels_mod = self.total_mod)

        print("Analysis finished")

    def open_visualization_results(self):
        self.gaussian_plot = RNA_analysis_platform(self.Analysis_NN)
        self.gaussian_plot.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
