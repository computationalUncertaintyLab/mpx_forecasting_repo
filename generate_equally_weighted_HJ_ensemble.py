#mcandrew

import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":

    continuous_predictions_at_all_horizons = pd.read_csv("./data/continuous_predictions/all_horizons_predictions.csv")

    def generate_EW_ensemble(x):
        EW_probs = pd.pivot_table(index="original_value", columns = "user_id", values = "value", data = x ).mean(1).reset_index()
        EW_probs.columns = ["original_value","value"]
        return EW_probs
    continuous_EW_ensemble = continuous_predictions_at_all_horizons.groupby(["question_id","resolve_time","resolution","cut_point","horizon"]).apply(generate_EW_ensemble).reset_index()
 
    continuous_EW_ensemble.to_csv("./data/continuous_predictions/ensemble_predictions.csv", index=False)

    #--binary ensemble

    binary_predictions_at_all_horizons = pd.read_csv("./data/binary_predictions/all_horizons_predictions.csv")
    binary_EW_ensemble = binary_predictions_at_all_horizons

    binary_EW_ensemble.to_csv("./data/binary_predictions/ensemble_predictions.csv")
