import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib
from src.utils.config_manager import ConfigManager
from src.utils.helpers import setup_logging, get_env_variable

# Initialize logging
setup_logging()

# Initialize Config Manager for hyperparameters
config_manager = ConfigManager('config/hyperparameters.yaml')

# Get the absolute path to the directory where your script is located
script_location = get_env_variable('SCRIPT_LOCATION')

# Build the absolute path to your model file
model_file_path = os.path.join(script_location, 'models', 'gradient_boost_model.pkl')

# Hyperparameters grid for GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}

def train_model(data, features, target):
    try:
        X = data[features]
        y = data[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = GradientBoostingClassifier()
        grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=3)
        grid_search.fit(X_train, y_train)

        best_clf = grid_search.best_estimator_
        y_pred = best_clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        logging.info(f"Model trained with accuracy: {accuracy}")

        # Save the model
        joblib.dump(best_clf, model_file_path)

        return best_clf, accuracy
    except Exception as e:
        logging.error(f"Failed to train the model: {e}")
        return None, None

def load_model(symbol):
    model_file = f"{symbol.replace('/', '_').lower()}_gradient_boost_model.pkl"
    model_path = os.path.join(script_location, '..', '..', 'models', model_file)
    try:
        clf = joblib.load(model_path)
        logging.info(f"Model for {symbol} loaded successfully.")
        return clf
    except Exception as e:
        logging.error(f"Failed to load the model for {symbol}: {e}")
        return None
