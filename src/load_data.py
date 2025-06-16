import os
import pandas as pd

DATA_DIR = "data"

def load_pbp_by_season(season):
    filename = f"pbp_{season}.parquet"
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        df = pd.read_parquet(path)
        return df
    else:
        print(f"No data found for season {season}")
        return pd.DataFrame()  



