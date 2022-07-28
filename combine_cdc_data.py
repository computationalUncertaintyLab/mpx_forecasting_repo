#mcandrew

import sys
sys.path.append("./mods/")

import pandas as pd

from glob import glob

def parse_filename(x):
    ts,ss = x.split("__")[1:]
    ss = ss.replace(".csv","")
    return ts,ss

def format_state_and_abbrev_names(row):
    from mods.state_and_abbreviations import us_state_to_abbrev
    
    us_state_to_abbrev = us_state_to_abbrev()
    abbrev_to_us_state = {ab:state for (state,ab) in us_state_to_abbrev.items()}
    
    if row.State in us_state_to_abbrev.keys():
        abbreviation = us_state_to_abbrev[row.State]
        state = row.State
    else:
        try:
            state = abbrev_to_us_state[row.State]
            abbreviation = row.State
        except:
            state = row.State
            abbreviation = row.State
    return pd.Series({"State":state, "Abbr":abbreviation})

if __name__ == "__main__":

    for n,fil in enumerate(glob("./cdc_webpage_downloads/*")):
        d = pd.read_csv(fil)

        #--rename column from State of Residence to State
        if "State of Residence" in d.columns:
            d = d.rename(columns = {"State of Residence":"State"})
        d.columns = [ _.capitalize() for _ in d.columns]

        time_stamp, snap_shot = parse_filename(fil)

        d["time_stamp"] = time_stamp
        d["snap_shot"]  = snap_shot

        state_and_abb = d.apply(format_state_and_abbrev_names ,1)
        d["State"] = state_and_abb.State
        d["Abbr"]  = state_and_abb.Abbr
        
        d = d[["time_stamp","snap_shot","State", "Abbr","Cases","Range"]]
        if n==0:
            d.to_csv("./data/cdc_data.csv", mode="w", index=False, header=True) 
        else:
            d.to_csv("./data/cdc_data.csv", mode="a", index=False, header=False) 
