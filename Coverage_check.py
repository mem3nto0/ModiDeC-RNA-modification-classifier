import numpy as np

# /// Function to penalize low covarage sites while calculating frequency ///

def Coverage_analysis(N_max, Data, Track_coverage, threshold = 0.2):

    Filtered_covarage = Track_coverage[ Track_coverage > 1]  
    median_covarage = np.median(Filtered_covarage)    
    MAD_covarage = np.median(np.absolute(Filtered_covarage - median_covarage))    

    if median_covarage > 2*N_max*threshold:

        lower_bound = median_covarage - MAD_covarage
        mask = np.where((Track_coverage >= lower_bound), 1, 0)

        Division_factor = N_max*(1 - (1 - Track_coverage/N_max)*mask)
        Final_results = Data / Division_factor[:,np.newaxis]

    else:

        if median_covarage < N_max*threshold:

            Final_results = (Data/N_max)         

        else:

            lower_bound = median_covarage
            mask = np.where((Track_coverage >= lower_bound), 1, 0)

            Division_factor = N_max*(1 - (1 - Track_coverage/N_max)*mask)
            Final_results = Data / Division_factor[:,np.newaxis]


    return Final_results