from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import joblib

def train_logistic_pipeline(X, y, preprocessor, max_iter=1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('clf', LogisticRegression(max_iter=max_iter))
    ])
    pipeline.fit(X_train, y_train)

    y_probs = pipeline.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_probs)
    print(f"Model AUC: {auc:.4f}")

    return pipeline

def save_model(model, path):
    joblib.dump(model, path)
    print(f"Model saved to {path}")
