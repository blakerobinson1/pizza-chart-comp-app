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


def load_all_pbp():
    all_data = []
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("pbp_") and filename.endswith(".parquet"):
            season = int(filename.split("_")[1].split(".")[0])
            df = load_pbp_by_season(season)
            if not df.empty:
                all_data.append(df)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("No play-by-play data found.")
        return pd.DataFrame()  

