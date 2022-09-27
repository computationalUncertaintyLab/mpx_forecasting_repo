#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.gridspec import GridSpec


def density_plot(subset,ax,legend=False):
    colors = ["blue","red","purple"]
    for horizon,ensemble in subset.groupby(["horizon"]):
        ax.plot(ensemble.scaled_value, ensemble.value, color = colors[horizon-1], lw=2, alpha=0.80, label = "Horizon {:d}".format(horizon) )

    ax.axvline(float(subset.iloc[0].resolution), color="black", lw=2, label="Truth" )
        
    ax.tick_params(which="both", labelsize=8)

    ax.set_ylabel("Density", fontsize=10)
    ax.set_xlabel("" )
    
    ax.set_xticks(np.arange(0,1+0.2,0.2))
    ax.set_xticklabels([])
    ax.set_xlim(0,1)

    if legend:
        ax.legend(frameon=False, fontsize=10, loc="upper left")
    

def histogram_plot(subset,ax):
    colors = ["blue","red","purple"]
    for horizon,ensemble in subset.groupby(["horizon"]):
        wide = pd.pivot_table(index="question_id",columns="quantile",values="value",data=ensemble)
        wide.columns =[ np.round(_,2) for _ in wide.columns] 
        
        ax.plot([wide[0.100], wide[0.900]], [horizon]*2  , color = colors[horizon-1], lw=5, alpha=0.70, label = "Horizon {:d}".format(horizon) )
        ax.scatter([wide[0.500]], [horizon]*1, s=30, color = colors[horizon-1], alpha=1. )

        ax.axvline(float(subset.iloc[0].resolution), color="black", lw=2, label="Truth" )
        ax.set_ylabel("")
        
        ax.set_xticks(np.arange(0,1+0.2,0.2))
        ax.set_xlabel( fromQid2Labels[qid], fontsize =10 )

        ax.tick_params(which="both", labelsize=8)

        ax.set_yticks([1,2,3])
        ax.set_ylim(-0.5,3.75)
        ax.set_xlim(0,1)
        ax.set_yticklabels([])

def mm2inch(x):
    return x/25.4

        
if __name__ == "__main__":

    #--predictions
    continuous_predictions_at_all_horizons = pd.read_csv("../../data/continuous_predictions/ensemble_predictions.csv")
    ensemble_quantiles                     = pd.read_csv("../../data/continuous_predictions/ensemble_quantiles.csv")
    
    #--truth
    ecdc = pd.read_csv("../../data/ecdc_data.csv")


    #11039 - Canada
    #10981 - US states
    #10979 - US cases
    #10978 - Europe cases

    plt.style.use("fivethirtyeight")
    fig = plt.figure()

    fromQid2Labels = { 11039:"Incident MPX cases in Canada"
                      ,10981:"Num of US states with >1 MPX case"
                      ,10979:"Incident MPX cases in US"
                      ,10978:"Incident MPX cases in Europe"}

    #--QID 11039

    gs00 = GridSpec(2,1, left=0.05, right=0.48, top = 0.95 , bottom = 0.60, wspace=0.05, height_ratios = [3,1])
    
    qid = 11039
    ax0,ax1 = fig.add_subplot(gs00[0]), fig.add_subplot(gs00[1])
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    density_plot(subset,ax0)
    histogram_plot(quants,ax1)

    #--QID 10981
    gs01 = GridSpec(2,1, left=0.52, right=0.95, top = 0.95 , bottom = 0.60, wspace=0.05, height_ratios = [3,1])
    
    qid = 10981
    ax0,ax1 = fig.add_subplot(gs01[0]), fig.add_subplot(gs01[1])
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    density_plot(subset,ax0)
    histogram_plot(quants,ax1)

    #--QID 10979
    gs10 = GridSpec(2,1, left=0.05, right=0.48, top = 0.50 , bottom = 0.08, wspace=0.05, height_ratios = [3,1])
    
    qid = 10979
    ax0,ax1 = fig.add_subplot(gs10[0]), fig.add_subplot(gs10[1])
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    density_plot(subset,ax0)
    histogram_plot(quants,ax1)

    #--QID 10978
    gs11 = GridSpec(2,1, left=0.52, right=0.95, top = 0.50 , bottom = 0.08, wspace=0.05, height_ratios = [3,1])
    
    qid = 10978
    ax0,ax1 = fig.add_subplot(gs11[0]), fig.add_subplot(gs11[1])
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    density_plot(subset,ax0, legend=True)
    histogram_plot(quants,ax1)

    w = mm2inch(183)
    
    fig.set_size_inches(w,w/1.5)

    plt.savefig("supp1_density_and_hist.pdf")
    plt.close()
