#mcandrew

import sys
from metaculus_client import metaculus_client
from interfaceForServer import interfaceForServer

import numpy as np
import pandas as pd

if __name__ == "__main__":
    interface = interfaceForServer()
    
    metac = metaculus_client("../../metaculusloginInfoFlu.text")
    metac.sendRequest2Server() # ping the server
   
    questions = [10976, 10978, 10979, 10975, 10981, 10977, 11039, 10982]
    scaling_data = {"question_id":[]
                    ,"min":[]
                    ,"max":[]
                    ,"deriv_ratio":[]
    }
    
    for q in questions:
        sys.stdout.write('Downloading data from Q {:04d}\n'.format(q))
        sys.stdout.flush()

        metac.collectQdata(q) # collect json data for this specific question
        if metac.data["type"]=="discussion":
            continue

        metac.collectScaleParams()
               
        scaling_data["question_id"].append(q)
        scaling_data["min"].append( metac.minvalue )
        scaling_data["max"].append( metac.maxvalue)
        scaling_data["deriv_ratio"].append(metac.deriv_ratio)

    # write historical predictions
    scaling_data = pd.DataFrame(scaling_data)
    scaling_data.to_csv("./data/scaling_data.csv",index=False)
    
