"""
Base model class providing common functionality for all position-specific models
"""
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import joblib
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List


logger = logging.getLogger(__name__)

class BaseModel:
    """Base class for all position-specific models"""
    def __init__(self):
        super().__init__()
        self.pipeline = None 

    def preprocess_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, ColumnTransformer]:
        pass
    
    def train_model(self, X: pd.DataFrame, y: pd.Series, 
                   preprocessor: ColumnTransformer,
                   **kwargs) -> Pipeline:
        """
        Train the model with cross-validation
        
        Args:
            X: Features
            y: Target
            preprocessor: Fitted preprocessor
            **kwargs: Additional model parameters
            
        Returns:
            Trained pipeline
        """
        
    
    def save_model(self, pipeline: Optional[Pipeline] = None) -> Path:
        pass
    
    def load_model(self) -> Pipeline:
        pass        
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        pass
    
    def get_feature_importance(self, top_n: int = 15) -> List[Tuple[str, float]]:
        pass
    
    def print_feature_importance(self, top_n: int = 15):
        pass
