#mcandrew

import sys
import numpy as np

class ecdc(object):
    def __init__(self):
        pass

    def grab_data(self):
        import pandas as pd
        
        data_url = "https://opendata.ecdc.europa.eu/monkeypox/casedistribution/csv/data.csv"
        self.ecdc = pd.read_csv(data_url)
        return self.ecdc

    def time_today(args):
        from datetime import date
        return date.today().strftime("%Y-%m-%d")
    
    def write(self):
        time_today = self.time_today()
        self.ecdc["snap_shot"] = time_today
        self.ecdc.to_csv("./data/ecdc_data.csv", index=False)
    
if __name__ == "__main__":

    data = ecdc()
    data.grab_data()
    data.write()
