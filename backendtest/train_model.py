import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import optuna
from sklearn.model_selection import cross_val_score

# Optional: import XGBoost and CatBoost if available
try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None
try:
    from lightgbm import LGBMClassifier
except ImportError:
    LGBMClassifier = None
try:
    from catboost import CatBoostClassifier
except ImportError:
    CatBoostClassifier = None

# Load your data

csv_path = r"c:/Users/Hari/Desktop/Crypto bot/test.csv"
df = pd.read_csv(csv_path)

# Model versioning setup
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
os.makedirs(MODELS_DIR, exist_ok=True)
version_time = datetime.now().strftime('%Y%m%d_%H%M%S')
version_registry_path = os.path.join(MODELS_DIR, 'model_versions.json')
if os.path.exists(version_registry_path):
    with open(version_registry_path, 'r') as f:
        version_registry = json.load(f)
else:
    version_registry = {}

# Example: Predict if next day's close > today's close (binary classification)
df['target'] = (df['close'].shift(-1) > df['close']).astype(int)
df = df.dropna()

feature_cols = [
    'open', 'high', 'low', 'close', 'volume', 'rsi', 'stoch_k', 'stoch_d', 'williams_r', 'roc', 'ao',
    'macd', 'macd_signal', 'macd_diff', 'adx', 'cci', 'sma_20', 'ema_20', 'bb_high', 'bb_low', 'atr', 'obv', 'cmf'
]
X = df[feature_cols].fillna(0)
y = df['target']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

models = {}
results = {}

def optimize_lgbm(X, y):
    def objective(trial):
        params = {
            'num_leaves': trial.suggest_int('num_leaves', 16, 128),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'n_estimators': trial.suggest_int('n_estimators', 50, 300),
            'random_state': 42,
            'n_jobs': -1
        }
        model = LGBMClassifier(**params)
        score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
        return score
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20, timeout=600)
    return study.best_params, study.best_value

def optimize_rf(X, y):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 300),
            'max_depth': trial.suggest_int('max_depth', 3, 20),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 8),
            'random_state': 42,
            'n_jobs': -1
        }
        model = RandomForestClassifier(**params)
        score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
        return score
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20, timeout=600)
    return study.best_params, study.best_value

def optimize_xgb(X, y):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 300),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'random_state': 42,
            'n_jobs': -1,
            'use_label_encoder': False,
            'eval_metric': 'logloss'
        }
        model = XGBClassifier(**params)
        score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
        return score
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20, timeout=600)
    return study.best_params, study.best_value

def optimize_cat(X, y):
    def objective(trial):
        params = {
            'iterations': trial.suggest_int('iterations', 50, 300),
            'depth': trial.suggest_int('depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'random_state': 42,
            'verbose': 0
        }
        model = CatBoostClassifier(**params)
        score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
        return score
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20, timeout=600)
    return study.best_params, study.best_value

def optimize_gb(X, y):
    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 300),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'random_state': 42
        }
        model = GradientBoostingClassifier(**params)
        score = cross_val_score(model, X, y, cv=3, scoring='accuracy').mean()
        return score
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20, timeout=600)
    return study.best_params, study.best_value


# LightGBM with Optuna fail-safe
if LGBMClassifier is not None:
    print("Optimizing LightGBM with Optuna...")
    best_params, best_cv = optimize_lgbm(X_train, y_train)
    print(f"Best LGBM params: {best_params}, CV accuracy: {best_cv:.4f}")
    lgbm = LGBMClassifier(**best_params)
    lgbm.fit(X_train, y_train)
    test_acc = accuracy_score(y_test, lgbm.predict(X_test))
    print(f"LGBM test accuracy: {test_acc:.4f}")
    prev_best = max([v['accuracy'] for v in version_registry.get('lgbm', [])], default=0.0)
    if test_acc >= prev_best:
        models['lgbm'] = lgbm
        lgbm_path = os.path.join(MODELS_DIR, f"lgbm_{version_time}.joblib")
        joblib.dump(lgbm, lgbm_path)
        results['lgbm'] = test_acc
    else:
        print("LGBM: New model did not outperform previous best. Not updating.")


# RandomForest with Optuna fail-safe
print("Optimizing RandomForest with Optuna...")
best_params, best_cv = optimize_rf(X_train, y_train)
print(f"Best RF params: {best_params}, CV accuracy: {best_cv:.4f}")
rf = RandomForestClassifier(**best_params)
rf.fit(X_train, y_train)
test_acc = accuracy_score(y_test, rf.predict(X_test))
print(f"RF test accuracy: {test_acc:.4f}")
prev_best = max([v['accuracy'] for v in version_registry.get('rf', [])], default=0.0)
if test_acc >= prev_best:
    models['rf'] = rf
    rf_path = os.path.join(MODELS_DIR, f"rf_{version_time}.joblib")
    joblib.dump(rf, rf_path)
    results['rf'] = test_acc
else:
    print("RF: New model did not outperform previous best. Not updating.")

# XGBoost with Optuna fail-safe
if XGBClassifier is not None:
    print("Optimizing XGBoost with Optuna...")
    best_params, best_cv = optimize_xgb(X_train, y_train)
    print(f"Best XGB params: {best_params}, CV accuracy: {best_cv:.4f}")
    xgb = XGBClassifier(**best_params)
    xgb.fit(X_train, y_train)
    test_acc = accuracy_score(y_test, xgb.predict(X_test))
    print(f"XGBoost test accuracy: {test_acc:.4f}")
    prev_best = max([v['accuracy'] for v in version_registry.get('xgb', [])], default=0.0)
    if test_acc >= prev_best:
        models['xgb'] = xgb
        xgb_path = os.path.join(MODELS_DIR, f"xgb_{version_time}.joblib")
        joblib.dump(xgb, xgb_path)
        results['xgb'] = test_acc
    else:
        print("XGBoost: New model did not outperform previous best. Not updating.")

# CatBoost with Optuna fail-safe
if CatBoostClassifier is not None:
    print("Optimizing CatBoost with Optuna...")
    best_params, best_cv = optimize_cat(X_train, y_train)
    print(f"Best CatBoost params: {best_params}, CV accuracy: {best_cv:.4f}")
    cat = CatBoostClassifier(**best_params)
    cat.fit(X_train, y_train)
    test_acc = accuracy_score(y_test, cat.predict(X_test))
    print(f"CatBoost test accuracy: {test_acc:.4f}")
    prev_best = max([v['accuracy'] for v in version_registry.get('cat', [])], default=0.0)
    if test_acc >= prev_best:
        models['cat'] = cat
        cat_path = os.path.join(MODELS_DIR, f"cat_{version_time}.joblib")
        joblib.dump(cat, cat_path)
        results['cat'] = test_acc
    else:
        print("CatBoost: New model did not outperform previous best. Not updating.")

# GradientBoosting with Optuna fail-safe
print("Optimizing GradientBoosting with Optuna...")
best_params, best_cv = optimize_gb(X_train, y_train)
print(f"Best GB params: {best_params}, CV accuracy: {best_cv:.4f}")
gb = GradientBoostingClassifier(**best_params)
gb.fit(X_train, y_train)
test_acc = accuracy_score(y_test, gb.predict(X_test))
print(f"GradientBoosting test accuracy: {test_acc:.4f}")
prev_best = max([v['accuracy'] for v in version_registry.get('gb', [])], default=0.0)
if test_acc >= prev_best:
    models['gb'] = gb
    gb_path = os.path.join(MODELS_DIR, f"gb_{version_time}.joblib")
    joblib.dump(gb, gb_path)
    results['gb'] = test_acc
else:
    print("GradientBoosting: New model did not outperform previous best. Not updating.")

# VotingClassifier (ensemble of available models)
ensemble_estimators = []
if 'rf' in models:
    ensemble_estimators.append(('rf', models['rf']))
if 'gb' in models:
    ensemble_estimators.append(('gb', models['gb']))
if 'lgbm' in models:
    ensemble_estimators.append(('lgbm', models['lgbm']))
if 'xgb' in models:
    ensemble_estimators.append(('xgb', models['xgb']))
if 'cat' in models:
    ensemble_estimators.append(('cat', models['cat']))

if ensemble_estimators:
    print("Training VotingClassifier (ensemble)...")
    voting = VotingClassifier(ensemble_estimators, voting='soft')
    voting.fit(X_train, y_train)
    voting_path = os.path.join(MODELS_DIR, f"voting_{version_time}.joblib")
    joblib.dump(voting, voting_path)
    results['voting'] = accuracy_score(y_test, voting.predict(X_test))


# Update version registry
for name in models:
    model_file = f"{name}_{version_time}.joblib"
    entry = {
        "file": model_file,
        "timestamp": version_time,
        "accuracy": results.get(name, 0.0)
    }
    if name not in version_registry:
        version_registry[name] = []
    version_registry[name].append(entry)
with open(version_registry_path, 'w') as f:
    json.dump(version_registry, f, indent=2)

print("\nModel training complete. Test accuracies:")
for name, acc in results.items():
    print(f"{name}: {acc:.4f}")
