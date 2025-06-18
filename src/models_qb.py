import pandas as pd
import numpy as np
from load_data import load_pbp_by_season
from models_common import add_def_passing_avg_stats

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

pbp_data = load_pbp_by_season(2023)

add_def_passing_avg_stats(pbp_data, 'complete_pass', 'sum', 'def_avg_comp_pct_allowed')
add_def_passing_avg_stats(pbp_data, 'air_yards', 'sum', 'def_avg_air_yards_per_attempt_allowed')
add_def_passing_avg_stats(pbp_data, 'air_epa', 'sum', 'def_avg_epa_allowed')
add_def_passing_avg_stats(pbp_data, 'pressure', 'sum', 'def_avg_pressure_rate')
add_def_passing_avg_stats(pbp_data, 'sack', 'sum', 'def_avg_pressure_rate')


def calculate_cpoe(pbp):
    """
    Calculate Completion Percentage over Expected (CPOE).
    CPOE = (Actual Completion Percentage - Expected Completion Percentage)
    """

    pbp_pass = pbp[(pbp['pass'] == 1) & (pbp['play_type'] != 'no_play')]  

    pbp_pass['obvious_pass'] = np.where((pbp_pass['down'] == 3) & (pbp_pass['ydstogo'] >= 6), 1, 0)


