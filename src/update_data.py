from nfl_data_py import import_pbp_data
import pandas as pd
import os

seasons = list(range(2024)) 

def update_pbp_data():
    for season in seasons:
        print(f"Loading {season} data...")
        df = import_pbp_data([season])
        out_path = os.path.join(DATA_DIR, f"pbp_{season}.parquet")
        df.to_parquet(out_path, index=False)
        print(f"Saved to {out_path}")

if __name__ == "__main__":
    update_pbp_data()
