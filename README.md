# ModiDeC-RNA-modification-classifier

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/git_hub_modiDeC.png)

ModiDeC is a Personalized two input neural network that was designed to identify RNA modifications from direct RNA sequencing using
RNA002 or RNA004 Oxford Nanopore technology (ONT) kits. In detail, ModiDeC combines LSTM and a newly designed inception-res-net block for
the multi-classification process. In this GitHub repository, we offer the ModiDeC models and several user graphic interfaces to retrain 
from scratch the neural network to readapt ModiDeC to your specific problem.

## Requirements

ModiDeC uses simple libraries such as NumPy and TensorFlow. It also uses the pre-compiled library "ont-remora" from ONT.
Here below is a list of the libraries used for ModiDeC creation:

     python == 3.10.14
     TensorFlow == 2.15
     pyqt5 == 5.15.11
     matplotlib == 3.9.1
     numpy == 1.26.4 
     ont-remora == 3.2.0 

We also offer a "remora_TF2_env.yml" file to install the same conda environment to run all the ModiDeC GUI.

IMPORTANT: ont-remora libraries is a Linux-based library, which means that ModiDeC can be used in Linx system or Windows with WSL.

## General information ModiDeC GUI

ModiDeC GUI is divided in three sub-interfaces (see figure below), which each of them has a specific design. The ModiDeC GUI can be used in several ways, from retraining the neural network to directly 
analyzing an aligned sample using a pre-trained neural network. We decided to create the GUIs to give the opportunity to adapt and customize ModiDeC for specific problems.

the figure below shows a general overview of ModiDeC GUIs. The first thing that can be observed is that the GUIs are divided into ”ModiDeC data curation”, “ModiDeC training” and “ModiDeC analysis”. 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/Gui_pipeline.png)

in the tutorial folder it is possible to find detailed tutorials for each of the three GUI.

## Epi2Me pipeline link

We also implemented ModiDeC in Epi2Me. Epi2Me links repositary can be found here below.

https://github.com/Nanopore-Hackathon/wf-modidec_data-curation

https://github.com/Nanopore-Hackathon/wf-modidec_training

https://github.com/Nanopore-Hackathon/wf-modidec_analysis

## Collaboration

This work is a collaboration partnership with the group of Prof. Dr. Susanne Gerber, Uni Medical Center, Mainz. https://csg.uni-mainz.de/group-member/susanne-gerber/

## Credit and Licence

This code is provided by Dr. Nicolo Alagna and the Computational Systems Genetics Group of the University Medical Center of Mainz. © 2024 All rights reserved.
