import pandas as pd
import numpy as np
from load_data import load_pbp_by_season

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

def calculate_cpoe(pbp):
    """
    Calculate Completion Percentage over Expected (CPOE).
    CPOE = (Actual Completion Percentage - Expected Completion Percentage)
    """

    pbp_pass = pbp[(pbp['pass'] == 1) & (pbp['play_type'] != 'no_play')]  

    pbp_pass['obvious_pass'] = np.where((pbp_pass['down'] == 3) & (pbp_pass['ydstogo'] >= 6), 1, 0)


