#mcandrew

import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":

    continuous_predictions_at_all_horizons = pd.read_csv("./data/continuous_predictions/all_horizons_predictions.csv")

    def generate_EW_ensemble(x):
        EW_probs = pd.pivot_table(index="variable", columns = "user_id", values = "scaled_value", data = x ).mean(1).reset_index()
        EW_probs.columns = ["variable","scaled_value"]
        return EW_probs
    continuous_EW_ensemble = continuous_predictions_at_all_horizons.groupby(["qid","resolve_time","resolution","cut_point","horizon"]).apply(generate_EW_ensemble)
    
    
    
    

