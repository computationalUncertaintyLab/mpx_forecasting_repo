#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.gridspec import GridSpec

import matplotlib.dates as mdates
import datetime

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
    ensemble_binary_quantiles              = pd.read_csv("../../data/binary_predictions/ensemble_quantiles.csv")
    
    ensemble_quantiles["resolve_time"] = pd.to_datetime(ensemble_quantiles.resolve_time)
    ensemble_quantiles["quantile"]     = np.round(ensemble_quantiles["quantile"],2)

    #--binary
    ensemble_binary_quantiles["resolve_time"] = pd.to_datetime(ensemble_binary_quantiles.resolve_time)
    ensemble_binary_quantiles["quantile"]     = np.round(ensemble_binary_quantiles["quantile"],2)
 
    myFmt = mdates.DateFormatter('%m-%d')



    
    #--truth
    ecdc   = pd.read_csv("../../data/ecdc_data.csv")
    
    canada = pd.read_csv("../../data/canada_cases_from_globalhealth.csv")
    canada["date"] = pd.to_datetime(canada["Date_entry"])
    canada = canada.loc[canada["date"] < "2022-07-01"]

    row = canada.iloc[-1]

    extend = {"date":pd.to_datetime(["2022-07-01","2022-07-02","2022-07-03","2022-07-04","2022-07-05"]),"cumulative_cases":[row.cumulative_cases]*5}
    extend = pd.DataFrame(extend)

    canada = canada.append(extend)
    
    #11039 - Canada
    #10981 - US states
    #10979 - US cases
    #10978 - Europe cases

    #10975
    #10977 Binary

    plt.style.use("fivethirtyeight")
    fig, axs = plt.subplots(3,2)

    fromQid2Labels = { 11039:"Ttl cases in Canada"
                      ,10981:"Num of US states"
                      ,10979:"Ttl cases in US"
                      ,10978:"Ttl cases in Europe"
                      ,10975:"Num of Countries"
                      ,10977:"PHEIC"}
    #--QID 11039
    ax = axs[0,0]
   
    qid = 11039
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]
    
    ax.plot( canada["date"],canada["cumulative_cases"], color="black", lw=2 )

    #ax.set_xticks( [x for x in canada["date"][::20]]    )
    
    #--hj predictions
    for horizon,Q in quants.groupby(["horizon"]):
        Q = Q.set_index(["quantile"])
        resolve_time = Q.iloc[0]["resolve_time"]
        
        ax.plot(   [resolve_time + datetime.timedelta(days=horizon)]*2, [Q.loc[0.10,"value"], Q.loc[0.90,"value"]], lw=2,alpha=0.65  )
        ax.scatter( resolve_time + datetime.timedelta(days=horizon), Q.loc[0.50,"value"],s=10)

    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel(fromQid2Labels[qid],fontsize=10)

    ax.axvline(pd.to_datetime("2022-07-01"),lw=1,color="black",ls="--")
    ax.xaxis.set_major_formatter(myFmt)
    
    #--QID 10981
    cdc = pd.read_csv("../../data/cdc_data.csv")

    def oldest_snapshot(d):
        most_recent = d.snap_shot.min()
        return d.loc[d.snap_shot==most_recent]
    recent_snapshots = cdc.groupby(["time_stamp"]).apply(oldest_snapshot).reset_index(drop=True)
    
    number_of_states = recent_snapshots.groupby(["time_stamp"]).apply(lambda x: pd.Series({"states":len(x)})).reset_index()
    number_of_states["time_stamp"] = pd.to_datetime(number_of_states.time_stamp)

    number_of_states = number_of_states.loc[number_of_states.time_stamp <= pd.to_datetime("2022-07-01")]

    row = number_of_states.iloc[-1]
    extend = {"time_stamp":pd.to_datetime(["2022-07-02","2022-07-03","2022-07-04","2022-07-05"]),"states":[row.states]*4}
    extend = pd.DataFrame(extend)

    number_of_states= number_of_states.append(extend)
    
    ax = axs[0,1]
    qid = 10981
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    ax.plot( number_of_states["time_stamp"],number_of_states["states"], color="black", lw=2 )
    
     #--hj predictions
    for horizon,Q in quants.groupby(["horizon"]):
        Q = Q.set_index(["quantile"])
        resolve_time = Q.iloc[0]["resolve_time"]
        
        ax.plot(   [resolve_time + datetime.timedelta(days=horizon)]*2, [Q.loc[0.10,"value"], Q.loc[0.90,"value"]], lw=2,alpha=0.65  )
        ax.scatter( resolve_time + datetime.timedelta(days=horizon), Q.loc[0.50,"value"],s=10)

    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel(fromQid2Labels[qid],fontsize=10)

    ax.axvline(pd.to_datetime("2022-07-01"),lw=1,color="black",ls="--")
    
    ax.xaxis.set_major_formatter(myFmt)
    
    #--QID 10979
    qid = 10979
    ax = axs[1,0]
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]


    usa = pd.read_csv("../../data/usa_cases_from_globalhealth.csv")
    usa["date"] = pd.to_datetime(usa["Date_entry"])
    usa = usa.loc[usa["date"] <= "2022-07-01"]

    row = usa.iloc[-1]

    extend = {"date":pd.to_datetime(["2022-07-01","2022-07-02","2022-07-03","2022-07-04","2022-07-05"]),"cumulative_cases":[row.cumulative_cases]*5}
    extend = pd.DataFrame(extend)

    usa = usa.append(extend)

    ax.plot( usa["date"],usa["cumulative_cases"], color="black", lw=2 )
    
    #--hj predictions
    for horizon,Q in quants.groupby(["horizon"]):
        Q = Q.set_index(["quantile"])
        resolve_time = Q.iloc[0]["resolve_time"]
        
        ax.plot(   [resolve_time + datetime.timedelta(days=horizon)]*2, [Q.loc[0.10,"value"], Q.loc[0.90,"value"]], lw=2,alpha=0.65  )
        ax.scatter( resolve_time + datetime.timedelta(days=horizon), Q.loc[0.50,"value"],s=10)

    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel(fromQid2Labels[qid],fontsize=10)

    ax.axvline(pd.to_datetime("2022-07-01"),lw=1,color="black",ls="--")

    ax.xaxis.set_major_formatter(myFmt)
    #--QID 10978
    qid = 10978
    ax = axs[1,1]
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    europe = pd.read_csv("../../data/europe_cases_from_globalhealth.csv")
    europe["date"] = pd.to_datetime(europe["Date_entry"])
    europe = europe.loc[europe["date"] <= "2022-07-01"]

    row = europe.iloc[-1]

    extend = {"date":pd.to_datetime(["2022-07-01","2022-07-02","2022-07-03","2022-07-04","2022-07-05"]),"cumulative_cases":[row.cumulative_cases]*5}
    extend = pd.DataFrame(extend)

    europe = europe.append(extend)

    ax.plot( europe["date"],europe["cumulative_cases"], color="black", lw=2 )
    
    #--hj predictions
    for horizon,Q in quants.groupby(["horizon"]):
        Q = Q.set_index(["quantile"])
        resolve_time = Q.iloc[0]["resolve_time"]
        
        ax.plot(   [resolve_time + datetime.timedelta(days=horizon)]*2, [Q.loc[0.10,"value"], Q.loc[0.90,"value"]], lw=2,alpha=0.65  )
        ax.scatter( resolve_time + datetime.timedelta(days=horizon), Q.loc[0.50,"value"],s=10)

    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel(fromQid2Labels[qid],fontsize=10)

    ax.axvline(pd.to_datetime("2022-07-01"),lw=1,color="black",ls="--")

    ax.xaxis.set_major_formatter(myFmt)
    #--QID 10975
    qid = 10975
    ax = axs[2,0]
    subset = continuous_predictions_at_all_horizons.loc[ continuous_predictions_at_all_horizons.question_id==qid ]
    quants = ensemble_quantiles.loc[ensemble_quantiles.question_id==qid]

    europe = pd.read_csv("../../data/countries_from_globalhealth.csv")
    europe["date"] = pd.to_datetime(europe["Date_entry"])
    europe = europe.loc[europe["date"] <= "2022-07-31"]
   
    row = europe.iloc[-1]

    extend = {"date":pd.to_datetime(["2022-08-01","2022-08-02","2022-08-03","2022-08-04","2022-08-05"]),"counts":[row.counts]*5}
    extend = pd.DataFrame(extend)

    europe = europe.append(extend)

    ax.plot( europe["date"],europe["counts"], color="black", lw=2 )
    
    #--hj predictions
    for horizon,Q in quants.groupby(["horizon"]):
        Q = Q.set_index(["quantile"])
        resolve_time = Q.iloc[0]["resolve_time"]
        
        ax.plot(   [resolve_time + datetime.timedelta(days=horizon)]*2, [Q.loc[0.10,"value"], Q.loc[0.90,"value"]], lw=2,alpha=0.65  )
        ax.scatter( resolve_time + datetime.timedelta(days=horizon), Q.loc[0.50,"value"],s=10)

    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel(fromQid2Labels[qid],fontsize=10)

    ax.axvline(pd.to_datetime("2022-07-31"),lw=1,color="black",ls="--")

    ax.xaxis.set_major_formatter(myFmt)
    
    #--QID 10977
    qid = 10977
    ax = axs[2,1]

    binary_predictions_at_all_horizons = pd.read_csv("../../data/binary_predictions/all_horizons_predictions.csv")
    quants = ensemble_binary_quantiles.loc[ensemble_binary_quantiles.question_id==qid]

    times = []
    for horizon,Q in quants.groupby(["horizon"]):
        Q = Q.set_index(["quantile"])
        resolve_time = Q.iloc[0]["resolve_time"]
        
        ax.plot( [horizon]*2, [Q.loc[0.10,"value"], Q.loc[0.90,"value"]], lw=2,alpha=0.65, label = "{:d} wk ahead".format(horizon)  )
        ax.scatter( horizon, Q.loc[0.50,"value"],s=10)
        
    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel(fromQid2Labels[qid],fontsize=10)

    ax.axhline(1.,lw=1,color="black",ls="--")

    ax.set_xlabel("Time horizon",fontsize=10)

    ax.legend(frameon=False, fontsize=10, labelspacing=0.25)

    ax.set_xticks([1,2,3])
    
    w = mm2inch(183)
    
    fig.set_size_inches(w,w/1.5)

    plt.savefig("hj_forecasts_and_truth.pdf")
    plt.savefig("hj_forecasts_and_truth.png", dpi=300)
    plt.close()
