#mcandrew

import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":

    data = pd.read_csv("./data/canada_monkeypox_map.csv")
    data = data.loc[ data.pruid==1 ]
    
    def sum_incident_cases(x):
        return pd.Series({"incident_cases":x.num_confirmedcases_delta.sum()})
    canada_monkeypox_data = data.groupby(["date"]).apply(sum_incident_cases)
    canada_monkeypox_data = canada_monkeypox_data.reset_index()

    canada_monkeypox_data.to_csv("./data/canada_cases.csv",index=False)
