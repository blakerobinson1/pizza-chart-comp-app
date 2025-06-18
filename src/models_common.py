import pandas as pd
import numpy as np
from load_data import load_pbp_by_season

"""
1. Average Completion Percentage Allowed by Defense
2. Average Air Yards per Attempt Allowed by Defense
3. Average Expected Points Added (EPA) Allowed by Defense
4. Average Pressure Rate by Defense
5. Average Sack Rate by Defense
"""

def add_def_passing_avg_stats(pbp, pbp_column, operation, new_column_name):
    """
    Generic function to add average passing stats for defense.

    Performs operation on column and divides the result by the number of pass attempts faced by the defense.
    
    Parameters:
    - pbp: DataFrame containing play-by-play data.
    - pbp_column: Column to group by (e.g., 'defteam').
    - operation: Aggregation operation (e.g., 'mean', 'sum').
    - new_column_name: Name of the new column to be created.
    
    Returns:
    - DataFrame with the new column added.
    """
    passes = pbp[
        (pbp['pass_attempt'] == 1) &
        (pbp['qb_spike'] != 1) &
        (pbp['play_type'] == 'pass') &
        (pbp['pass_result'].isin(['C', 'I'])) & 
        ~(pbp['qb_dropback'].isna()) &
        ~((pbp['air_yards'] >= 40) & (pbp['half_seconds_remaining'] <= 15)) # dropping hail marys
    ].copy()

    def_pass_stats = (
        passes.groupby(['season', 'defteam'])
        .agg(
            column_with_operation=(pbp_column, operation),
            pass_attempts_faced=('pass_attempt', 'count')
        )
        .reset_index()
    )

    def_pass_stats[new_column_name] = (def_pass_stats['column_with_operation'] / def_pass_stats['pass_attempts_faced'])

    pbp = pbp.merge(
        def_pass_stats[['season', 'defteam', new_column_name]],
        how='left',
        on=['season', 'defteam']
    )
    
    return pbp



'''
def def_avg_comp_percent_allowed(pbp):
    """
    Calculate the average completion percentage allowed by the defense.
    """
    passes = pbp[
        (pbp['pass_attempt'] == 1) &
        (pbp['qb_spike'] != 1) &
        (pbp['play_type'] == 'pass') &
        (pbp['pass_result'].isin(['C', 'I'])) & 
        ~(pbp['qb_dropback'].isna()) &
        ~((pbp['air_yards'] >= 40) & (pbp['half_seconds_remaining'] <= 15)) #dropping hail marys
    ].copy()

    def_pass_stats = (
        passes.groupby(['season', 'defteam'])
        .agg(
            completions_allowed=('complete_pass', 'sum'),
            pass_attempts_faced=('pass_attempt', 'count')
        )
        .reset_index()
    )

    def_pass_stats['def_completion_pct_allowed'] = (def_pass_stats['total_completions_allowed'] / def_pass_stats['pass_attempts_faced'])

    pbp = pbp.merge(
        def_pass_stats[['season', 'defteam', 'def_completion_pct_allowed']],
        how='left',
        on=['season', 'defteam']
    )
    
    return pbp


def def_avg_yards_per_attempt_allowed(pbp):
    # Methodize this later
    passes = pbp[
        (pbp['pass_attempt'] == 1) &
        (pbp['qb_spike'] != 1) &
        (pbp['play_type'] == 'pass') &
        (pbp['pass_result'].isin(['C', 'I'])) & 
        ~(pbp['qb_dropback'].isna()) &
        ~((pbp['air_yards'] >= 40) & (pbp['half_seconds_remaining'] <= 15)) # dropping hail marys
    ].copy()

    passes = passes[passes['pass_result'] == 'C']  # Completions only

    def_pass_stats = (
        passes.groupby(['season', 'defteam'])
        .agg(
            air_yards_sum=('air_yards', 'sum'),
            pass_attempts_faced=('pass_attempt', 'count')
        )
        .reset_index()
    )

    def_pass_stats['def_air_yards_per_attempt_allowed'] = (def_pass_stats['air_yards_sum'] / def_pass_stats['pass_attempts_faced'])

    pbp = pbp.merge(
        def_pass_stats[['season', 'defteam', 'def_air_yards_per_attempt_allowed']],
        how='left',
        on=['season', 'defteam']
    )
    
    return pbp


def def_avg_epa_allowed(pbp):
    
    passes = pbp[
        (pbp['pass_attempt'] == 1) &
        (pbp['qb_spike'] != 1) &
        (pbp['play_type'] == 'pass') &
        (pbp['pass_result'].isin(['C', 'I'])) & 
        ~(pbp['qb_dropback'].isna()) &
        ~((pbp['air_yards'] >= 40) & (pbp['half_seconds_remaining'] <= 15)) # dropping hail marys
    ].copy()

    def_pass_stats = (
        passes.groupby(['season', 'defteam'])
        .agg(
            air_epa_sum=('air_epa', 'sum'),
            pass_attempts_faced=('pass_attempt', 'count')
        )
        .reset_index()
    )

    def_pass_stats['def_avg_epa_allowed'] = (def_pass_stats['air_epa_sum'] / def_pass_stats['pass_attempts_faced'])

    pbp = pbp.merge(
        def_pass_stats[['season', 'defteam', 'def_avg_epa_allowed']],
        how='left',
        on=['season', 'defteam']
    )
    
    return pbp
'''