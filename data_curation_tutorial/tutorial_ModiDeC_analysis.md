# Tutorial Part 3: Data Analysis with ModiDeC 

![GUI for retraining ModiDeC](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/Analysis_GUI.png)

The data analysis GUI allows us to visualize the ModiDeC analysis in a simple way.

## Starting the analysis using ModiDeC neural network

from the above figure, it is possible to see that several buttons can be pressed to load data, neural network, and reference for the data analysis.
ModiDeC reconstructs the analysis directly on the reference. The data has to be basecalled using dorado (with the --emit-move flag) and aligned
using sametools.

This user interface allows the analysis of one reference at a time.

Here is a list of what each button does:

  1) "Pod5 file folder": load the folder containing the pod5 files that you want to analyze.
  2) "bam file": load the bam file for the analysis of the transcript
  3) "Neural network folder": load the folder where the model is stored.
  4) "kmer-level table file": kmer level table that is gives from ONT.
  5) "reference": load the reference for your single transcript.

After these steps, press the button "initialize the data". this can take a few seconds to load the model.
When the initialization is finished, you can select the total amount of reads to analyze. for example, if you want to analyze the initial
1000 reads, put as start_index = 0 and end_index = 1000. if you want to analyze all the reads, put start_index = 0 and end_index = -1.
The analysis of a lot of reads can take a lot of time. For a good statistical analysis, we suggest a value of 5000 for the first analysis.

Press the "start analysis with Neural Network" to let ModiDeC analyze your data. At the end of the analysis, a "ModiDeC_analysis.npz" file
will be created in the current working folder. The file contains the analysis of ModiDeC, which shows the modification frequency for each
modification that ModiDeC was trained on and for each nucleotide. 

The results can be also visualized using the GUI by pressing the "visualize results" button. A new window is open where the data can
be visualized.

![figure plot](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/analysis_plot1.png)

select the start and end reference points to visualize and press "plot". the window will change and the results of the selected reference
region are shown.

![figure plot 2](https://github.com/mem3nto0/ModiDeC-RNA-modification-classifier/blob/main/data_curation_tutorial/analysis_plot2.png)
