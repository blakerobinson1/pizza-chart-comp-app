#!/usr/bin/env python3
"""
Script to train models and generate datasets for the Pizza Chart Comparison App
"""
import sys
import logging
from models.qb.xcomp_cpoe import XcompCpoeModel
from pathlib import Path

from data.load_data import load_all_pbp, load_pbp_multiple_seasons

if __name__ == "__main__":
    loaded_pbp = load_pbp_multiple_seasons([2018, 2019, 2020, 2021, 2022, 2023])
    print(loaded_pbp.head())
    pass