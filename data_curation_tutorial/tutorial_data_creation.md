# Tutorial Part 1: Data creation for training ModiDeC 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/Figura_data_generation.png)

The "Data Curation" (or data creation) GUI was created to give the opportunity to the user to generate personalized training data for ModiDeC, which can be used
for further steps and retraining the neural network.

The figure shows three sections with several variables as inputs. In this Tutorial, we will explain the several steps to do to correctly generate your own
dataset for training ModiDeC for your specific problem.

## Important Steps for running the GUI

data has to be basecalled using Dorado and aligned using samtools:

  1) Basecall your data using Dorado with the --emit-move. It is necessary for resquiggleling process.
  2) aligned using "samtools" to generate a .bam file

## Select Input files and save directory (Section 1)

In this section, the input files can be selected using the several Gui buttons.

  1) "Pod5 file folder" button: Select the folder where the pod5 files are stored. The folder must contain only pod5 files.
  2) "bam file folder" button: Select the folder where the bam files are stored. The folder must contain only pod5 files.
  3) "Save path" button: select the folder where the training data will be saved. Create a specific folder for it.
  4) "kmer-level table file" button: select the k-mer level table for the 004 or 002 kit. These files are provided by ONT.

We use the bam folder instead of a single file selection because, in certain cases, multiple .bam files can be obtained by the same pod5 measurement.
if this is the case, generating multiple .bam files the GUI automatically analyzes all the bam files without any data overwriting.

Example for multiple bam: if during the alignment using samtools you used the first alignment flag, use samtools to generate a single .bam file for each
reference. then create a folder containing all the bam files created in this way. Use this folder for the GUI and all the bam files will be used for the data generation of training data.

### General variable for training data (Section 1)

In this section,


