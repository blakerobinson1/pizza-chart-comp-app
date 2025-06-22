import pandas as pd
import numpy as np
from data.load_data import load_pbp_by_season,  load_all_pbp
from models.models_common import add_def_passing_avg_stats
from data.load_data import load_pbp_by_season
from models.qb.qb_xcomp_utils import filter_pass_plays, preprocess_xcomp_data
from models.model_utils import train_logistic_pipeline, save_model
from sklearn.metrics import roc_auc_score

model = load("models/xcomp_model.joblib")


df = load_pbp_by_season([2024])
df = filter_pass_plays(df)
X, _, preprocessor = preprocess_xcomp_data(df)


y_probs = model.predict_proba(X)[:, 1]
auc = roc_auc_score(_, y_probs)
print(f"AUC: {auc:.4f}")