#mcandrew

import sys
import numpy as np
import pandas as pd


def from_density_to_quantiles(x):
    from scipy.interpolate import pchip
    from scipy.optimize import root_scalar as root

    xs = x.scaled_value.values
    ys = np.cumsum(x.value.values)
    ys = ys/ys[-1]

    f = pchip(xs, ys)

    quantile_data = {"quantile":[], "value":[]}
    for q in [0.025] + list(np.arange(0.05,0.95,0.05)) + [0.975]:
        F = lambda x: f(x) - q

        lower_bracket,upper_bracket = xs[np.max(np.where(F(xs)<0)[0])],xs[np.min(np.where(F(xs)>0)[0])]
        q_value = root(F, bracket= (lower_bracket,upper_bracket)).root

        quantile_data["quantile"].append(q)
        quantile_data["value"].append(q_value)

    return pd.DataFrame(quantile_data)

if __name__ == "__main__":

    #--import data
    continuous_predictions_at_all_horizons = pd.read_csv("./data/continuous_predictions/all_horizons_predictions.csv")
    ensemble_continuous_predictions        = pd.read_csv("./data/continuous_predictions/ensemble_predictions.csv")


    ensemble_quantiles = ensemble_continuous_predictions.groupby(["question_id","resolve_time","resolution","cut_point","horizon"]).apply(from_density_to_quantiles).reset_index() 
    ensemble_quantiles = ensemble_quantiles[["question_id","resolve_time","resolution","cut_point","horizon","quantile","value"]]

    ensemble_quantiles.to_csv("./data/continuous_predictions/ensemble_quantiles.csv",index=False)
