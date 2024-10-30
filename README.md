# ModiDeC-RNA-modification-classifier

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/Analysis_GUI.png)

ModiDeC is Personalized two input neural network that was designed to indentify RNA modifications from direct RNA sequencing using
RNA002 or RNA004 Oxford Nanopore technology (ONT) kits. In details, ModiDeC combines LSTM and new designed inception-res-net block for
the multi-classification process. Is this Github repository we offer the ModiDeC models and several usergraphic inferface to retrain 
from scratch the neural network to riadapt ModiDeC to your specific problem.

## General information ModiDeC GUI

ModiDeC GUI is divided in three sub-inferfaces (see figure below), which each of them has a specific design. The ModiDeC GUI can be used in several way, from retrain the neural network to directly 
analyzing an aligned sample using a pretrained neural network. We decided to create the GUIs to give the opportunity to adapt and customize ModiDeC for specific problems.

the figure below shows a general overview of ModiDeC GUIs. The first thing that can be observed is that the GUIs are divided in”ModiDeC data curation”, “ModiDeC training” and “ModiDeC analysis”. 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/Gui_pipeline.png)

in the tutorial folder it is possible to find detailed tutorials for each of the three GUI.

