#mcandrew

import sys
sys.path.append("../../")

from mods.index import index

import numpy as np
import pandas as pd

from datetime import timedelta

import scipy.stats

class model(object):
    def __init__(self, data):
        self.data = data
        #self.add_model_days()
        self.all_locations()
        self.horizon = 28 #--28 day horizon

    def all_locations(self):
        self.all_locations = self.data.location.unique()
        
    def add_model_days(self):
        import sys
        sys.path.append("../../")

        from mods.time_help import from_date_to_model_day
        
        self.data["model_days"] = self.data.apply(lambda x: from_date_to_model_day(x.Day),1)
        
    def arima_model(self,d):
        from statsmodels.tsa.arima.model import ARIMA

        #--find best order based on AIC
        def find_best_aic(y,x=None):
            best_aic = np.inf
            for a in range(3):
                for b in range(3):
                    for c in range(3):
                        
                        if x is not None:
                            model = ARIMA(endog = y ,exog = x, order = (a,b,c))
                            model = model.fit()
                        else:
                            model = ARIMA(endog = y, order = (a,b,c))
                            model = model.fit()
                            
                        if model.aic < best_aic:
                            best_aic = model.aic
                            best_order = (a,b,c)
            return best_order

        best_order = find_best_aic(y=d[:,1],x=d[:,0])
                        
        #--best fitting model to y
        model = ARIMA(endog = d[:,1] ,exog = d[:,0], order = best_order)
        model = model.fit()

        x = d[:,0]
        max_x = max(x)
        extra_xs = np.arange(max_x+1,(max_x+1)+4)

        prediction_object = model.get_forecast(exog=extra_xs, steps=4)

        #--best guess
        means       = prediction_object.predicted_mean
        se_of_means = prediction_object.se_mean 

        return means,se_of_means
        
    def forecast_location(self,location):
        loc_data = self.data.loc[self.data.location==location]
        loc_data = loc_data.loc[:,["model_days","values"]]
        self.loc_data  = loc_data

        d = loc_data.to_numpy()
        print(d.shape)

        #--fit model
        means,se_of_means = self.arima_model(d)
        return means,se_of_means

if __name__ == "__main__":

    #--data. First column is time and second column is values to forecast

    def reformat_data(x,loc,old_name="cumulative_cases"):
        x["model_days"] = np.arange(0,len(x))
        x["location"]        = loc
        
        x = x.rename(columns= {old_name:"values"})
        return x
    
    #--QID 10979
    us_cases = pd.read_csv("../../data/usa_cases_from_globalhealth.csv")
    us_cases = reformat_data(us_cases,"us_cases")
    us_cases["question_id"] = 10979
    
    #--QID 11039
    canada_cases = pd.read_csv("../../data/canada_cases_from_globalhealth.csv")
    canada_cases = reformat_data(canada_cases,"canada_cases")
    canada_cases["question_id"] = 11039

    #--QID 10981
    us_states = pd.read_csv("../../data/number_of_us_states.csv")
    us_states = reformat_data(us_states,"us_states","states")
    us_states["question_id"] = 10981

    us_states = us_states.rename(columns = {"time_stamp":"Date_entry"})
    
    #--QID 10978
    europe_cases = pd.read_csv("../../data/europe_cases_from_globalhealth.csv")
    europe_cases = reformat_data(europe_cases,"europe_cases")
    europe_cases["question_id"] = 10978
        
    #--QID 10975:
    all_countries = pd.read_csv("../../data/countries_from_globalhealth.csv")
    all_countries = reformat_data(all_countries,"all_countries","counts")
    all_countries["question_id"] = 10975

    training_data = us_states.append( canada_cases ).append(us_states).append(europe_cases).append(all_countries) 

    #--cutpoint data
    cutpoint = pd.read_csv("../../data/cut_points_resolve_times_qids.csv")

    training_data = training_data.merge(cutpoint, on = ["question_id"] )

    #--collect specific columns and tranform columns to date time objects
    training_data = training_data[["model_days","location","question_id","values","cut_point","resolve_time","Date_entry","horizon"]]
    training_data["Date_entry"] = pd.to_datetime(training_data["Date_entry"])
    training_data["cut_point"] = pd.to_datetime(training_data["cut_point"])

    #--run through all training data and build a model
    all_quantiles = pd.DataFrame()
    all_means_and_ses = pd.DataFrame()
    for (loc,qid,hor,cut,res), subset in training_data.groupby(["location","question_id","horizon","cut_point","resolve_time"]):
        data = subset.loc[subset.Date_entry<=subset.cut_point]

        if len(data)<=2:
            continue
        
        times = [pd.Timestamp(x) for x in data.Date_entry.values]

        #--add more time units
        last_time      = times[-1]
        last_model_day = int(data.model_days.values[-1] )

        time_data = { "times":times, "model_days": list(data.model_days.values)}
        for _ in range(27):
            last_time      =  pd.Timestamp(last_time) + timedelta(days=1)
            last_model_day +=1
            
            time_data["times"].append(last_time) 
            time_data["model_days"].append(last_model_day)
        time_data = pd.DataFrame(time_data)
            
        data = data[["model_days","location","values"]]

        mdl = model( data )
        means,se_of_means = mdl.forecast_location(loc)

        #--save predicted mean and se
        stats = {"mean":[ means[hor-1] ], "se":[ se_of_means[hor-1] ]}
        stats = pd.DataFrame(stats)
        stats["target"]       = loc
        stats["question_id"]  = qid
        stats["horizon"]      = hor
        stats["cut_point"]    = cut
        stats["resolve_time"] = res

        all_means_and_ses = all_means_and_ses.append(stats)

        #--construct quantiles from the samples
        def build_quantiles(means,se_of_means,hor):
            quantiles = [0.01,0.025] + list(np.arange(0.05,0.95+0.05,0.05)) + [0.975, 0.99] 
            h = hor-1
            quantiles_values = scipy.stats.norm(means[h], se_of_means[h]).ppf(quantiles)
            return pd.DataFrame({"quantile":quantiles, "value":quantiles_values})

        quantiles = build_quantiles(means,se_of_means,hor)
        quantiles["target"]       = loc
        quantiles["question_id"]  = qid
        quantiles["horizon"]      = hor
        quantiles["cut_point"]    = cut
        quantiles["resolve_time"] = res

        all_quantiles = all_quantiles.append(quantiles)

    #--store dataframes
    all_means_and_ses["model"] = "ARIMA"
    all_means_and_ses.to_csv("all_means_and_ses.csv",index=False)
        
    all_quantiles["model"] = "ARIMA"
    all_quantiles.to_csv("all_quantiles.csv",index=False)

