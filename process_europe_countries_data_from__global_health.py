#mcandrew

import sys
import numpy as np
import pandas as pd

from datetime import datetime, timedelta

if __name__ == "__main__":

    data = pd.read_csv("./data/global_health.csv")
    countries = {"Russia", "Turkey","Germany", "United Kingdom", "France", "Italy", "Spain", "Poland", "Ukraine"
                 ,"Romania", "Kazakhstan", "Netherlands", "Belgium", "Sweden", "Czech Republic", "Greece", "Azerbaijan"
                 ,"Portugal", "Hungary", "Belarus", "Austria", "Switzerland", "Serbia", "Bulgaria", "Denmark", "Slovakia"
                 ,"Finland", "Norway", "Ireland", "Croatia", "Georgia", "Moldova", "Bosnia and Herzegovina", "Albania"
                 ,"Armenia", "Lithuania", "Slovenia", "Latvia", "Estonia", "Cyprus", "Luxembourg", "Montenegro", "Malta"
                 ,"Iceland", "Andorra", "Faroe Islands", "Liechtenstein", "Monaco", "San Marino", "Vatican City"}
    europe = data.loc[data.Country.isin(countries)]
    europe["Date_entry"] = pd.to_datetime(europe.Date_entry)

    min_date = europe.Date_entry.min()
    max_date = europe.Date_entry.max()

    countries = {"Date_entry":[], "counts":[]}

    dt = min_date
    while dt < max_date:
        countries["Date_entry"].append(dt)

        subset = europe.loc[ europe.Date_entry <= dt ]
        countries["counts"].append(len(subset.Country.unique()))

        dt = dt + timedelta(days=1)
    countries = pd.DataFrame(countries)
   
    countries.to_csv("./data/europe_countries_from_globalhealth.csv",index=False)
