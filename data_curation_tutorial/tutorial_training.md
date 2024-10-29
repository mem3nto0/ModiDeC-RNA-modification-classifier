# Tutorial Part 2: Training of the neural network 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/Figure_training.png)


### Training Data Input
For training the neural network with own data, the directories containing the data need to be specified. First, the training data directory should contain the raw signal sequence stored in a .npz file obtained from the data curation step before. In the validation data directory, the labels should also be stored in a .npz file. The save model folder specifies the path where the trained model will be stored.

### General Variables
Additional specifications are needed for training the neural network:
  1) The batch size (1) specifies the number of samples which are propagated through the network during training. Batch sizes like 128 or 256 are recommended dependening on the memory available for training.
  2) The k-mer model (2) can be adjusted to the type of data used for training. Both data sequenced from RNA002 and RNA004 flowcells from Oxford Nanopore Technologies can be used for training the model: for RNA002, insert the number 5 (5-mer). For RNA004, insert the number 9 (9-mer).
  3)  Insert the number of epochs for the training (3). We recommend setting the number of epochs to four.
  4)  The variable name NN specifies the name of the saved model (4).
  5)  The user can also specify if a validation of the retrained model is needed, by typing yes or no. 

After the settings are settled, press the button "training neural network" to retrain ModiDeC. When the training is finished, a folder with the name of the neural network will be created in the save folder that contain the trained neural network.
