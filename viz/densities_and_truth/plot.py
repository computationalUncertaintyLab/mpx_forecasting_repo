#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":

    continuous_predictions_at_all_horizons = pd.read_csv("../../data/continuous_predictions/ensemble_predictions.csv")
    continuous_ensemble = pd.read_csv("../../data/continuous_predictions/ensemble_predictions.csv")

    binary_predictions_at_all_horizons = pd.read_csv("../../data/binary_predictions/ensemble_predictions.csv")
    binary_ensemble = pd.read_csv("../../data/binary_predictions/ensemble_predictions.csv")

    truths = pd.read_csv("../../data/truths.csv")
    truths = truths.set_index("question_id")
    
    plt.style.use("fivethirtyeight")
    fromQid2Labels = { 11039:"Ttl cases in Canada"
                      ,10981:"Num of US states"
                      ,10979:"Ttl cases in US"
                      ,10978:"Ttl cases in Europe"
                      ,10975:"Num of Countries"
                      ,10977:"PHEIC"}

    fromQid2limits =  { 11039: [0,3000]
                        ,10981: [0,50]
                        ,10979: [0,3000]
                        ,10978: [0,2*10**4]
                        ,10975: [0,125]
                        ,10977: [0,1]}

    #--computational models
    doubling_model = pd.read_csv("")

    
    fig,axs = plt.subplots(3,2)

    axs = axs.flatten()
    for n,(qid, densities) in enumerate(continuous_predictions_at_all_horizons.groupby(["question_id"])):
        ax = axs[n]
        
        for horizon, density in densities.groupby(["horizon"]):
            ax.plot(density.original_value, density.value, lw = 2)

        ax.axvline( float(truths.loc[qid,"truth"]), color="black", lw=2 )
            
        ax.tick_params(which="both",labelsize=8)
        ax.set_xlabel(fromQid2Labels[qid],fontsize=10)
        ax.set_xlim(fromQid2limits[qid])


            
        
        
    

    
    
    

    

