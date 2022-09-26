#mcandrew

import sys
import numpy as np
import pandas as pd

def produce_cut_point_dataset(d,horizon):
    #--Cut point will be two weeks before the resolution time
    def subtract_weeks(x,weeks):
        import datetime
        return x - datetime.timedelta(weeks=weeks)
    d["cut_point"] = d["resolve_time"].apply(lambda x: subtract_weeks(x,weeks=horizon))

    #--submission times must be before cut point
    d_cut = d.loc[ d.time <= d.cut_point  ]

    #--most recent user submission before the cut point
    def most_recent(x):
        return  x.sort_values("time").iloc[-1]
    users_and_times  = d_cut[["user_id","question_id","time"]].drop_duplicates()
    users_and_times  = users_and_times.groupby(["user_id","question_id"]).apply(most_recent).reset_index(drop=True)

    #--merge only those users, questions, and times that are most recent
    d_cut__most_recent = d_cut.merge(users_and_times, on = ["user_id","question_id","time"]  )

    #--time horizon for these individual predictions
    d_cut__most_recent["horizon"] = horizon

    return d_cut__most_recent

if __name__ == "__main__":

    predictions = pd.read_csv("./data/predictions.csv", sep=";")

    #--restrict to questions with a resolution
    predictions = predictions.loc[~np.isnan(predictions.resolution)]

    #--separate into continuous and binary predictions
    continuous_predictions = predictions.loc[predictions.question_type=="continuous"]
    continuous_predictions = continuous_predictions.drop(columns = ["binary_prediction"])

    #--from wide to long format
    continuous_predictions = continuous_predictions.melt( id_vars = ['question_id', 'user_id', 'time', 'void', 'question_type', 'resolution','resolve_time', 'close_time'])
    
    #--remove extra text around r value
    continuous_predictions["scaled_value"] = [float(_[0]) for _ in continuous_predictions.variable.str.findall("(\d+[.]\d+|\d+)")]

    #--save all continuous predictions submitted before the close time
    continuous_predictions.to_csv("./data/continuous_predictions/all_continuous_predictions.csv",index=False)

    #--format columns
    continuous_predictions["time"] = continuous_predictions.time.astype('datetime64[ns]')
    continuous_predictions["resolve_time"] = continuous_predictions.resolve_time.astype('datetime64[ns]')

    #--cut at different time horizons
    all_horizons = pd.DataFrame()
    for week in [1,2,3]:
        d = produce_cut_point_dataset(continuous_predictions,week)
        all_horizons = all_horizons.append(d)
    all_horizons.to_csv("./data/continuous_predictions/all_horizons_predictions.csv",index=False)
    
    #--work on binary predictions
    binary_predictions = predictions.loc[predictions.question_type=="binary"]
    binary_predictions = binary_predictions.drop(columns = [_ for _ in binary_predictions.columns if "P" in _])
    binary_predictions.to_csv("./data/binary_predictions/all_binary_predictions.csv",index=False)

    #--format columns
    binary_predictions["time"] = binary_predictions.time.astype('datetime64[ns]')
    binary_predictions["resolve_time"] = binary_predictions.resolve_time.astype('datetime64[ns]')

    #--cut at different time horizons
    all_horizons = pd.DataFrame()
    for week in [1,2,3]:
        d = produce_cut_point_dataset(binary_predictions,week)
        all_horizons = all_horizons.append(d)
    all_horizons.to_csv("./data/binary_predictions/all_horizons_predictions.csv",index=False)
