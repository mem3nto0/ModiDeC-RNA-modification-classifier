# Tutorial Part 1: Data creation for training ModiDeC 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/Figura_data_generation.png)

The "Data Curation" (or data creation) GUI was created to give the opportunity to the user to generate personalized training data for ModiDeC, which can be used
for further steps and retraining the neural network.

The figure shows three sections with several variables as inputs. In this Tutorial, we will explain the several steps to do to correctly generate your own
dataset for training ModiDeC for your specific problem.

Initially, we will give a description of the inputs that can be introduced in the GUI for data creation. In the second part of file, an example will be
provide to show what are the steps to do for creating the training data.

## Important Steps for running the GUI

data has to be basecalled using Dorado and aligned using samtools:

  1) Basecall your data using Dorado with the --emit-move. It is necessary for resquiggleling process.
  2) aligned using "samtools" to generate a .bam file

## Select Input files and save-directory (Section 1)

In this section, the input files can be selected using the several Gui buttons.

  1) "Pod5 file folder" button: Select the folder where the pod5 files are stored. The folder must contain only pod5 files.
  2) "bam file folder" button: Select the folder where the bam files are stored. The folder must contain only pod5 files.
  3) "Save path" button: select the folder where the training data will be saved. Create a specific folder for it.
  4) "kmer-level table file" button: select the k-mer level table for the 004 or 002 kit. These files are provided by ONT.

We use the bam folder instead of a single file selection because, in certain cases, multiple .bam files can be obtained by the same pod5 measurement.
If this is the case, generating multiple .bam files the GUI automatically analyzes all the bam files without any data overwriting.

Example for multiple bam: if you used the first alignment flag during the alignment using samtools, use samtools to generate a single .bam file for each
reference. then create a folder containing all the bam files created in this way. Use this folder for the GUI and all the bam files will be used for the data generation of training data.

## General variable for training data (Section 2)

This second section of the GUI focuses on giving sequence information for the data sets the user wants to use for training. Information like "modification position" or "modified data"
can be selected and let the users use their oligos for retraining the neural network. here below, a description of the input is provided:

  1) "modification_data?": it is a yes or no question. The user can specify if the data are modified or not. It is useful if the user wants to add un-modfied reads for the training.
  2) "take_modification_region?": it is a yes or no question. The user can decide to use all the read for the analysis or use only the signal region around the
     modification position that can be selected a few steps later. For example, it is useful for un-modified data for taking more k-mer for the analysis.
  3) "name_save_file": specify the name of the file that will be saved. For each modification that you want to analyze or if the data are modified or not, give a new name.
  4) "What type of modification?: it is a string linked also to the modification dictionary. For example, if you have in your dictionary two modifications (m6A and Gm), type Gm if you want
     to create training data for Gm, or type m6A to create training data for m6A.
  5) "Bases before modification": It can be a positive or negative integer. Choose the number of bases to consider before (positive values) or after (negative values) for the resquiggle. Use 0
     if you want to take only a few bases around the modification position. This feature can be useful depending on the oligos design.
  6) "Modification dictionary": come separated list of the total modifications that ModiDeC has to learn. For example, For Gm and m6A write in the box "Gm,m6A".

## Segmentation variables for training data (Section 3)

This third section focuses on raw signal and neural network features that can be personalized by the user. A description of the input is provided:

  1) "batch size": it is the number of raw signal that we will be saved in a single file. This is helpful to reduce memory problems during the saving process. Recommended value 16.
  2) "max seq- length": it is an integer linked to one of the inputs of the neural network. It is linked to the maximum number of bases to use for the input. A Good value is "chunk length" divided by 10.
  3) "chunk length": it is an integer that tells you how much is bit the time window to extract from the raw signal. IT is linked to one of the inputs of the neural network.
  4) "shift in time": indicates how many time points to move for creating a new representation of the modified raw signal. suggested value is "chunk length" divided "batch size".
  5) "start read number" and "end read number": Integers to select the pod5 reads indexes to use for generating data.

After filling all the variables, press the button "Start resguigle" and .npz files will be generated in the save-folder.

## Practical example data training generation: Create a training data set containing Gm and m6A modification

We want to give a practical example on how to fill the GUI for generating training data for ModiDeC. We have two oligos, one containing one Gm modification at position 64 in the reference and another one
containing m6A ad position 75 in the reference. Additionally, we also have an un-modified oligo as well.

First step, basecall each of the three oligos pod5 files indipently Using Dorado with the --emit-move flag. this means that I will have a .ubam file for Gm, one for m6A and one for Un-mod. After it,
Use sametools to align each basecalled data to its corresponding sequence to obtain three .bam files. in the end, we should have something like this:

  1) Gm_pod5_folder + Gm_bam_folder(containing "Gm_aligned.bam" file)
  2) m6A_pod5_folder + m6A_bam_folder(containing "m6A_aligned.bam" file)
  3) unmodified_pod5_folder + unmofied_bam_folder(containing "unmodifed_aligned.bam" file)

You want to save all of them in the same folder for the training, then create a folder called "training_data".

Now, for this case we want that ModiDeC analyzes closely the modified signal. Having this purpose, we can set the "chunck size" parameter to 400, which means that the "max seq. length" is 40.
additionally, we want to save 16 raw signal per file, which means that "batch size" is 16 and consequently shift in time is 25 (400/16). Setting in mind these values, we can run the GUI and start
fo fill the variable for analyzing first Gm, than m6a and in the end the unmodified data. in the figure below you can see how the GUI was filled with our goal with the three runs. The red squares
show what was changed in the GUI between one run and the other.
