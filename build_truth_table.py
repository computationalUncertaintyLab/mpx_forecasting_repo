#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == "__main__":


    truth = {"question_id":[], "truth":[], "date":[]}

    #--QID 11039
    canada = pd.read_csv("./data/canada_cases_from_globalhealth.csv")
    canada["date"] = pd.to_datetime(canada["Date_entry"])
    true_value = canada.loc[canada["date"] == "2022-07-01", "cumulative_cases"]

    truth["question_id"].append(11039)
    truth["date"].append("2022-07-01")
    truth["truth"].append(float(true_value))

    #--QID 10981
    number_of_us_states = pd.read_csv("./data/number_of_us_states.csv")
    number_of_us_states["time_stamp"] = pd.to_datetime(number_of_us_states["time_stamp"])
    true_value = number_of_us_states.loc[number_of_us_states["time_stamp"] == "2022-07-01", "states"]

    truth["question_id"].append(10981)
    truth["date"].append("2022-07-01")
    truth["truth"].append( float(true_value) )
    
    #--QID 10979
    usa = pd.read_csv("./data/usa_cases_from_globalhealth.csv")
    usa["date"] = pd.to_datetime(usa["Date_entry"])

    true_value = usa.loc[usa["date"] == "2022-07-01", "cumulative_cases"]

    truth["question_id"].append(10979)
    truth["date"].append("2022-07-01")
    truth["truth"].append(float(true_value))
    
    #--QID 10978
    europe = pd.read_csv("./data/europe_cases_from_globalhealth.csv")
    europe["date"] = pd.to_datetime(europe["Date_entry"])

    true_value = europe.loc[europe["date"] == "2022-07-01", "cumulative_cases"]

    truth["question_id"].append(10978)
    truth["date"].append("2022-07-01")
    truth["truth"].append(float(true_value))
    
    
    #--QID 10975
    europe = pd.read_csv("./data/countries_from_globalhealth.csv")
    europe["date"] = pd.to_datetime(europe["Date_entry"])
 
    true_value = europe.loc[europe["date"] == "2022-07-31", "counts"]

    truth["question_id"].append(10975)
    truth["date"].append("2022-07-31")
    truth["truth"].append(float(true_value))
 
    #-QID 10977 
    truth["question_id"].append(10977)
    truth["date"].append("2022-12-31")
    truth["truth"].append(1.)
    
    truth = pd.DataFrame(truth)

    truth.to_csv("./data/truths.csv")
