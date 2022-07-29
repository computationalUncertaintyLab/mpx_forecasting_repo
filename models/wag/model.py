#mcandrew

import sys
sys.path.append("../../")

from mods.index import index

import numpy as np
import pandas as pd

class model(object):
    def __init__(self, data):
        self.data = data
        self.add_model_days()
        self.all_locations()

    def all_locations(self):
        self.all_locations = self.data.location.unique()
        
    def add_model_days(self):
        import sys
        sys.path.append("../../")

        from mods.time_help import from_date_to_model_day
        
        self.data["model_days"] = self.data.apply(lambda x: from_date_to_model_day(x.Day),1)
        
    def stan_model(self):
        self.comp_model = '''
        data {
           int N;
           
           vector [N] days;
           vector [N] cases;
        }
        parameters {
            real alpha;
            real beta;

            real<lower=0> sigma;
        }
        model {
            for (n in 1:N){
                 cases[n] ~ normal( exp2(alpha+ beta*days[n]), sigma);
            }  
        }
        '''
    def forecast_location(self,location):
        import stan
        
        loc_data = self.data.loc[self.data.location==location]
        loc_data = loc_data.loc[:,["model_days","cases"]]
        self.loc_data  = loc_data

        d = loc_data.to_numpy()

        #--reference date
        ref = min(d[:,0])
        self.reference_model_day = ref
        
        #--fit model
        data = {"days": d[:,0] - ref,"cases":d[:,-1], "N": d.shape[0]  }
        self.stan_model()

        posterior = stan.build(self.comp_model, data=data)
        self.fit = posterior.sample(num_samples=5*10**3,num_chains=1)
        return self.fit

if __name__ == "__main__":

    idx = index("../../data/")
    mpxdata = idx.grab_cdc_and_ecdc_data()
    
    mdl = model( mpxdata )

    for loc in mdl.all_locations:
        mdl.forecast_location(loc)
