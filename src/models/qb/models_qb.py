import pandas as pd
import numpy as np
from src.data.load_data import load_pbp_by_season,  load_all_pbp
from src.models.models_common import add_def_passing_avg_stats
from src.data.load_data import load_pbp_by_season
from src.models.qb.qb_xcomp_utils import filter_pass_plays, preprocess_xcomp_data
from src.models.model_utils import train_logistic_pipeline, save_model

'''
Goal Metrics (QB):
1. Completion Percentage over Expected (CPOE) ***
2. EPA per Play
3. Air Yards over Expected (AYOE) ***
4. Interceptions per Attempt
5. Sacks over Expected (SOE) ***
6. Rushing Yards over Expected (RYOE) ***
7. Turnover worthy Play rate ***
8. Touchdowns over Expected (TDOE) ***
'''

def train_xcomp_model(pbp, model_path="models/xcomp_model.joblib"):
    df = filter_pass_plays(pbp)
    X, y, preprocessor = preprocess_xcomp_data(df)
    model = train_logistic_pipeline(X, y, preprocessor)
    save_model(model, model_path)
    return model


pbp_data = load_all_pbp()

add_def_passing_avg_stats(pbp_data, 'complete_pass', 'sum', 'def_avg_comp_pct_allowed')
add_def_passing_avg_stats(pbp_data, 'air_yards', 'sum', 'def_avg_air_yards_per_attempt_allowed')
add_def_passing_avg_stats(pbp_data, 'air_epa', 'sum', 'def_avg_epa_allowed')
add_def_passing_avg_stats(pbp_data, 'pressure', 'sum', 'def_avg_pressure_rate')
add_def_passing_avg_stats(pbp_data, 'sack', 'sum', 'def_avg_pressure_rate')

train_xcomp_model(pbp_data)





