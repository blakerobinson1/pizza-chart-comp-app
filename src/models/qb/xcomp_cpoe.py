"""
QB-specific model for expected completion percentage
"""
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from typing import Tuple
from data.load_data import load_pbp_multiple_seasons
from data.data_utils import data_utils

from ..base_model import BaseModel
        
class XcompCpoeModel(BaseModel):
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, ColumnTransformer]:
        """
        Preprocess data for QB expected completion model
        
        Args:
            df: Raw play-by-play data
            
        Returns:
            X: Features dataframe
            y: Target series (completion)
            preprocessor: Fitted preprocessor
        """

        # Fill missing values
        df = df.copy()
        df['yards_after_catch'] = df['yards_after_catch'].fillna(0)
        df['qb_scramble'] = df['qb_scramble'].fillna(0)
        df['qb_hit'] = df['qb_hit'].fillna(0)
        
        # Select features
        feature_columns = [
            'air_yards', 'pass_location', 'yardline_100',
            'down', 'ydstogo', 'yards_after_catch', 'qb_scramble', 'qb_hit', 
            'obvious_pass', 'def_avg_comp_pct_allowed',
            'def_avg_air_yards_per_attempt_allowed', 'def_avg_sack_rate', 
            'def_avg_epa_allowed'
        ]
        
        # Filter for required columns and drop NaN
        df_filtered = df[feature_columns + ['complete_pass']].dropna()
        
        X = df_filtered.drop(columns='complete_pass')
        y = df_filtered['complete_pass']
        
        # Define categorical features
        categorical_features = ['pass_location']
        
        # Create preprocessor
        preprocessor = ColumnTransformer([
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ], remainder='passthrough')
        
        # Fit preprocessor
        preprocessor.fit(X)
        
        return pd.DataFrame(X), pd.Series(y), preprocessor

    def train_and_save(self, seasons: list = [2018, 2019, 2020, 2021, 2022, 2023]) -> 'XcompCpoeModel':
        """
        Train the QB expected completion model and save it
        
        Args:
            seasons: List of seasons to use for training. If None, uses all available.
            
        Returns:
            Self for method chaining
        """

        data_util = data_utils()
            
        # Load and process data
        pbp_data = (
            load_pbp_multiple_seasons(seasons)
            .pipe(data_util.filter_pass_plays)
            .assign(obvious_pass=lambda df: np.where((df['down'] == 3) & (df['ydstogo'] >= 6), 1, 0))
            .pipe(data_utils.add_defensive_stats, 'passing')
        )
        
        # Preprocess data
        X, y, preprocessor = self.preprocess_data(pbp_data)
        
        # Train model
        pipeline = self.train_model(X, y, preprocessor)
        
        # Save model
        self.save_model(pipeline)
        
        return self

    def predict_completion_probability(self, play_data: pd.DataFrame) -> np.ndarray:
        """
        Predict completion probability for given plays
        
        Args:
            play_data: DataFrame with play features
            
        Returns:
            Array of completion probabilities
        """
        if self.pipeline is None:
            self.pipeline = self.load_model()
            
        # Preprocess the input data
        _, _, preprocessor = self.preprocess_data(play_data)
        
        # Transform features
        X_transformed = preprocessor.transform(play_data)
        
        # Make predictions
        return self.pipeline.predict_proba(X_transformed)[:, 1]

    def calculate_cpoe(self, actual_completions: pd.Series, 
                        expected_completions: pd.Series) -> float:
        """
        Calculate Completion Percentage Over Expected (CPOE)
        
        Args:
            actual_completions: Series of actual completion percentages
            expected_completions: Series of expected completion percentages
            
        Returns:
            CPOE value
        """
        return (actual_completions - expected_completions).mean() 