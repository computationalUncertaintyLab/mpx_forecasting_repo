#mcandrew

import sys
import numpy as np
import pandas as pd

from datetime import datetime, timedelta

if __name__ == "__main__":

    data = pd.read_csv("./data/global_health.csv")

    data.loc[ data.Country.isin(["Wales", "England", "Northern Ireland", "Scotland", "Cayman Islands", "Bermuda","Gibraltar"] ), "Country"  ] = "UK"
    data.loc[ data.Country.isin(["Guadeloupe", "New Caledonia","Martinique"] ), "Country"  ] = "France"
    data.loc[ data.Country == "Puerto Rico", "Country"  ] = "United States"
    
    data["Date_entry"] = pd.to_datetime(data.Date_entry)

    min_date = data.Date_entry.min()
    max_date = data.Date_entry.max()

    countries = {"Date_entry":[], "counts":[]}

    dt = min_date
    while dt < max_date:
        countries["Date_entry"].append(dt)

        subset = data.loc[ data.Date_entry <= dt ]
        countries["counts"].append(len(subset.Country.unique()))

        dt = dt + timedelta(days=1)
    countries = pd.DataFrame(countries)
   
    countries.to_csv("./data/countries_from_globalhealth.csv",index=False)
