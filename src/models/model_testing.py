import pandas as pd
import numpy as np
from data.load_data import load_pbp_by_season
from models.models_common import add_def_passing_avg_stats
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from joblib import load
from data.load_data import load_pbp_by_season
from models.qb.qb_xcomp_utils import filter_pass_plays, preprocess_xcomp_data
from models.model_utils import save_model,  cross_validate_xcomp_model

model = load("models/xcomp_model.joblib")

def train_xcomp_model_with_cv(pbp, cv=5, model_path="models/xcomp_model.joblib"):
    X, y, preprocessor = preprocess_xcomp_data(pbp)
    
    cross_validate_xcomp_model(X, y, preprocessor, cv=cv)
    
    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('clf', LogisticRegression(max_iter=5000))
    ])
    pipeline.fit(X, y)
    save_model(pipeline, model_path)
    return pipeline

if __name__ == "__main__":
    pbp_data = (
        load_pbp_by_season(2024)
        .pipe(filter_pass_plays)
        .assign(obvious_pass=lambda df: np.where((df['down'] == 3) & (df['ydstogo'] >= 6), 1, 0))
        .pipe(add_def_passing_avg_stats, 'complete_pass', 'sum', 'def_avg_comp_pct_allowed')
        .pipe(add_def_passing_avg_stats, 'air_yards', 'sum', 'def_avg_air_yards_per_attempt_allowed')
        .pipe(add_def_passing_avg_stats, 'air_epa', 'sum', 'def_avg_epa_allowed')
        .pipe(add_def_passing_avg_stats, 'sack', 'sum', 'def_avg_sack_rate')
    )

    train_xcomp_model_with_cv(pbp_data)