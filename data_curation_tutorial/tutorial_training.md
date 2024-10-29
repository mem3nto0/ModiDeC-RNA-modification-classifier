# Tutorial Part 2: Training of the neural network 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/Figure_training.png)


### Training Data Input
For training the neural network with your own data, the directories containing the data need to be specified. data has to be created using the "Resguiggle_remora_Gui.py" to use the training user interface.
  1) select the folder where the training data were created by pressing the button "training data folder".
  2) (optional) if validation data are created as well using the "Resguiggle_remora_Gui.py", select the validation folder using the "validation data folder" button. if you don't have validation data, remember to set the "validation during training" variable with "no".
  3) Select the folder where the retrained ModiDeC model will be saved by pressing the button "save model folder". This will specify the path where the model will be stored.

### General Variables
Additional specifications are needed for training the neural network:
  1) The batch size (1) specifies the number of samples which are propagated through the network during training. Batch sizes like 128 or 256 are recommended depending on the memory available for training.
  2) The k-mer model (2) can be adjusted to the type of data used for training. Both data sequenced from RNA002 and RNA004 flowcells from Oxford Nanopore Technologies can be used for training the model: for RNA002, insert the number 5 (5-mer). For RNA004, insert the number 9 (9-mer).
  3)  Insert the number of epochs for the training (3). We recommend setting the number of epochs to four.
  4)  The variable name NN specifies the name of the saved model (4).
  5)  The user can also specify if a validation of the retrained model is needed, by typing yes or no. 

After the settings are settled, press the button "Start training" to retrain ModiDeC. When the training is finished, a folder with the name of the neural network will be created in the "save folder" that contains the trained neural network.
