import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def filter_pass_plays(df):
    return df[df['pass_attempt'] == 1].copy()

def preprocess_xcomp_data(df):
    df = df[[
        'complete_pass', 'air_yards', 'pass_location', 'yardline_100',
        'down', 'ydstogo', 'obvious_pass', 'def_avg_comp_pct_allowed',
        'def_avg_air_yards_per_attempt_allowed', 'def_avg_epa_allowed', 
        'def_avg_sack_rate'
    ]].dropna()

    X = df.drop(columns='complete_pass')
    y = df['complete_pass']

    categorical = ['pass_location']
    numeric = ['air_yards', 'yardline_100', 'down', 'ydstogo', 'obvious_pass', 'def_avg_comp_pct_allowed',
               'def_avg_air_yards_per_attempt_allowed', 'def_avg_epa_allowed', 'def_avg_sack_rate']

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
    ], remainder='passthrough')

    return X, y, preprocessor
