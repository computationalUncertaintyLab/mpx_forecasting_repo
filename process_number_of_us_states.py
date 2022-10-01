#mcandrew

import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":

    cdc = pd.read_csv("./data/cdc_data.csv")

    def oldest_snapshot(d):
        most_recent = d.snap_shot.min()
        return d.loc[d.snap_shot==most_recent]
    recent_snapshots = cdc.groupby(["time_stamp"]).apply(oldest_snapshot).reset_index(drop=True)
    
    number_of_states = recent_snapshots.groupby(["time_stamp"]).apply(lambda x: pd.Series({"states":len(x)})).reset_index()
    number_of_states["time_stamp"] = pd.to_datetime(number_of_states.time_stamp)

    number_of_states.to_csv("./data/number_of_us_states.csv")
