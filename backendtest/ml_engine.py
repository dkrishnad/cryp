from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, cross_val_score

DB_PATH = "trades.db"
MODEL_PATH = "model.joblib"
SCALER_PATH = "scaler.joblib"

# ...existing code for ML engine (see attachment for full content)...
