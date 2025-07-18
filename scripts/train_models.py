#!/usr/bin/env python3
"""
Script to train models and generate datasets for the Pizza Chart Comparison App
"""
import sys
import logging
from models.qb.xcomp_cpoe import XcompCpoeModel
from pathlib import Path

from data.load_data import load_all_pbp



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_all_models():
    """Train all available models"""
    xcomp_cpoe = XcompCpoeModel()
    xcomp_cpoe.train_and_save()

def generate_all_pizza_chart_datasets():
    """Generate datasets for all positions"""


def evaluate_model(model_name: str):
    """Evaluate a model"""
    xcomp_cpoe = XcompCpoeModel()


def main():
    """Main function to run training and dataset generation"""

    
    # Train models
    train_all_models()
    
    # Generate datasets
    #generate_all_pizza_chart_datasets()
    

if __name__ == "__main__":
    main() 