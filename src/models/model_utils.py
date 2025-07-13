from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
import joblib

def train_logistic_pipeline(X, y, preprocessor, max_iter=5000, feature_weights=False):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('clf', LogisticRegression(max_iter=max_iter))
    ])
    pipeline.fit(X_train, y_train)

    if (feature_weights):
        model = pipeline.named_steps['clf']
        feature_names = pipeline.named_steps['preprocess'].get_feature_names_out()
        coefs = model.coef_[0]

        top_features = sorted(zip(feature_names, coefs), key=lambda x: abs(x[1]), reverse=True)
        for name, coef in top_features[:15]:
            print(f"{name}: {coef:.4f}")


    y_probs = pipeline.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_probs)
    print(f"Model AUC: {auc:.4f}")

    return pipeline

def save_model(model, path):
    joblib.dump(model, path)
    print(f"Model saved to {path}")

def cross_validate_xcomp_model(X, y, preprocessor, cv=5):
    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('clf', LogisticRegression(max_iter=5000))
    ])

    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    auc_scores = cross_val_score(pipeline, X, y, cv=skf, scoring='roc_auc')

    print(f"{cv}-Fold CV AUC scores: {auc_scores}")
    print(f"Mean AUC: {auc_scores.mean():.4f}")
    print(f"Std AUC: {auc_scores.std():.4f}")

    return auc_scores