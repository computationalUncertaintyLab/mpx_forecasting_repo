class index(object):
    def __init__(self,root):
        self.root = root
        
    def grab(self,fl):
        import os
        import pandas as pd
        
        fl = os.path.join(self.root,fl)
        print("Importing {:s}".format(fl))
        return pd.read_csv(fl)

    def grab_cdc_data(self):
        return self.grab("cdc_data.csv")
    
    def grab_ecdc_data(self):
        return self.grab("ecdc_data.csv")

    def grab_cdc_and_ecdc_data(self):
        return self.grab("mpx_cdc_and_ecdc.csv")


