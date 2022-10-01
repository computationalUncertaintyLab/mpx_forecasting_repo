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

    def sum_counts(x):
        return pd.Series({"counts":len(x)})
    counts_data = europe.groupby(["Date_entry"]).apply(sum_counts).reset_index()
    counts_data["Date_entry"] = pd.to_datetime(counts_data.Date_entry)

    counts_data["cumulative_cases"] = counts_data["counts"].cumsum()

    #--interpolation
    min_date = counts_data.Date_entry.min()
    max_date = counts_data.Date_entry.max()

    all_dates = {"Date_entry": [] }

    curent_day = min_date
    while curent_day < max_date:
        all_dates["Date_entry"].append(curent_day)
        curent_day = curent_day + timedelta(days=1)
    all_dates = pd.DataFrame(all_dates)

    counts_data = all_dates.merge(counts_data, on = ["Date_entry"], how="left")
    counts_data["counts"] = counts_data.counts.interpolate()
    counts_data["cumulative_cases"] = counts_data.cumulative_cases.interpolate()
    
    counts_data.to_csv("./data/europe_cases_from_globalhealth.csv",index=False)
