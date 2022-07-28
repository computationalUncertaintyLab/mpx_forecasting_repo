#mcandrew

import sys

from mods.index import index

import numpy as np
import pandas as pd

def most_recent_snapshot(x):
    x["snap_shot"] = pd.to_datetime(x.snap_shot,format="%Y-%m-%d %H %M %S")
    latest_snap_shot = snap_shots = x.snap_shot.unique().max()
    
    return x.loc[x.snap_shot==latest_snap_shot]

if __name__ == "__main__":

    idx = index("./data/")
    cdc  = idx.grab_cdc_data()
    ecdc = idx.grab_ecdc_data()

    #--most recent snapshot for each day in the cdc dataset
    cdc = cdc.groupby(["time_stamp"]).apply(most_recent_snapshot).reset_index(drop=True)
    
    #--format column names
    ecdc = ecdc.rename(columns = {"DateRep":"Day","CountryExp":"location","CountryCode":"location_abbr","ConfCases":"cases"})

    cdc = cdc.rename(columns = {"time_stamp":"Day","State":"location","Abbr":"location_abbr","Cases":"cases"})
    cdc = cdc.drop(columns = ["Range"]) # removing range from cdc data columns
    cdc["Source"] = "CDC"
    
    cdc_and_ecdc = cdc.append(ecdc)
    cdc_and_ecdc.to_csv("./data/mpx_cdc_and_ecdc.csv",index=False)
