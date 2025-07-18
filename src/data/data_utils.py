"""
Centralized data management for loading and processing play-by-play data
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class data_utils:
    """Centralized data manager for loading and processing play-by-play data"""
    
    def filter_pass_plays(self, pbp: pd.DataFrame) -> pd.DataFrame:
        """Filter for pass plays only"""
        filtered = pbp[
            (pbp['pass_attempt'] == 1) &
            (pbp['qb_spike'] != 1) &
            (pbp['play_type'] == 'pass') &
            ~(pbp['qb_dropback'].isna()) &
            ~((pbp['air_yards'] >= 40) & (pbp['half_seconds_remaining'] <= 15))  # Drop hail marys
        ].copy()
        
        logger.info(f"Filtered to {len(filtered)} pass plays from {len(pbp)} total plays")
        return pd.DataFrame(filtered)
    
    def add_defensive_stats(self, pbp: pd.DataFrame, stat_type: str = 'passing') -> pd.DataFrame:
        """Add defensive average stats to the dataset"""
        if stat_type == 'passing':
            return self.add_def_passing_stats(pbp)
        else:
            raise ValueError(f"Unknown stat_type: {stat_type}")
    
    def add_def_passing_stats(self, pbp: pd.DataFrame) -> pd.DataFrame:
        """Add defensive passing statistics"""
        passes = self.filter_pass_plays(pbp)
        
        # Calculate defensive stats
        def_stats = (
            passes.groupby(['season', 'defteam'])
            .agg({
                'complete_pass': ['sum', 'count'],
                'air_yards': 'sum',
                'air_epa': 'sum',
                'sack': 'sum'
            })
            .reset_index()
        )
        
        # Flatten column names
        def_stats.columns = ['season', 'defteam', 'comp_sum', 'pass_attempts', 'air_yards_sum', 'epa_sum', 'sack_sum']
        
        # Calculate rates
        def_stats['def_avg_comp_pct_allowed'] = def_stats['comp_sum'] / def_stats['pass_attempts']
        def_stats['def_avg_air_yards_per_attempt_allowed'] = def_stats['air_yards_sum'] / def_stats['pass_attempts']
        def_stats['def_avg_epa_allowed'] = def_stats['epa_sum'] / def_stats['pass_attempts']
        def_stats['def_avg_sack_rate'] = def_stats['sack_sum'] / def_stats['pass_attempts']
        
        # Merge back to original data
        result = pbp.merge(
            def_stats[['season', 'defteam', 'def_avg_comp_pct_allowed', 'def_avg_air_yards_per_attempt_allowed', 
                      'def_avg_epa_allowed', 'def_avg_sack_rate']],
            how='left',
            on=['season', 'defteam']
        )
        
        return result
    
    '''def save_processed_dataset(self, df: pd.DataFrame, position: str, season: Optional[int] = None) -> Path:
        """Save processed dataset to disk"""
        filename = f"{position}_processed"
        if season:
            filename += f"_{season}"
        filename += ".parquet"
        
        path = DATASETS_DIR / filename
        df.to_parquet(path)
        logger.info(f"Saved processed dataset to {path}")
        return path
    
    def load_processed_dataset(self, position: str, season: Optional[int] = None) -> pd.DataFrame:
        """Load processed dataset from disk"""
        filename = f"{position}_processed"
        if season:
            filename += f"_{season}"
        filename += ".parquet"
        
        path = DATASETS_DIR / filename
        if path.exists():
            return pd.read_parquet(path)
        else:
            logger.warning(f"No processed dataset found at {path}")
            return pd.DataFrame()'''