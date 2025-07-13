import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def filter_pass_plays(pbp):
   return pbp[
        (pbp['pass_attempt'] == 1) &
        (pbp['qb_spike'] != 1) &
        (pbp['play_type'] == 'pass') &
        ~(pbp['qb_dropback'].isna()) &
        ~((pbp['air_yards'] >= 40) & (pbp['half_seconds_remaining'] <= 15)) # dropping hail marys
    ].copy()

def preprocess_xcomp_data(df):
    df['yards_after_catch'] = df['yards_after_catch'].fillna(0)
    df['qb_scramble'] = df['qb_scramble'].fillna(0)
    df['qb_hit'] = df['qb_hit'].fillna(0)

    df = df[[
        'complete_pass', 'air_yards', 'pass_location', 'yardline_100',
        'down', 'ydstogo', 'yards_after_catch', 'qb_scramble', 'qb_hit', 'obvious_pass', 'def_avg_comp_pct_allowed',
        'def_avg_air_yards_per_attempt_allowed', 'def_avg_sack_rate', 'def_avg_epa_allowed' 
    ]].dropna()

    X = df.drop(columns='complete_pass')
    y = df['complete_pass']

    categorical = ['pass_location']

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
    ], remainder='passthrough')

    return X, y, preprocessor
