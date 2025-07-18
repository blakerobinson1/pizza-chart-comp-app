"""
Pizza chart visualization for player comparison
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash import Dash, html
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

from ..config import MODEL_CONFIG

logger = logging.getLogger(__name__)

class PizzaChartVisualizer:
    """Create pizza charts for player comparison"""
    
    
        