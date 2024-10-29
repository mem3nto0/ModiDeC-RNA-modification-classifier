## Tutorial Part 2: Training of the neural network 

### Training Data Input
For training the neural network with own data, the directories containing the data need to be specified. First, the training data directory should contain the raw signal sequence stored in a .npz file obtained from the data curation step before. In the validation data directory, the labels should also be stored in a .npz file. The save model folder specifies the path where the trained model will be stored.

### General Variables
Additional specifications are needed for training the neural network. The batch size (1) specifies the number of samples which are propagated through the network during training. The k-mer model (2) can be adjusted to type of data used for training. Both data sequenced from RNA002 and RNA004 flowcells from Oxford Nanopore Technologies can be used for training the model: for RNA002, the 5-mer model should be specified, for RNA004, the 9-mer model should specified accordingly. Batch sizes like 128 or 256 are recommended dependening on the memory available for training. We recommend to set the number of epochs (2) to four. The variable name NN specifies the name of the saved model. The user can also specify if a validation of the retrained model is needed, by typing yes or no. 
