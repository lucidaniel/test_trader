import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from main import load_config

class GradientBoostingModel:
    def __init__(self, config_path='../config/settings.yaml'):
        self.config = load_config(config_path)
        self.data_path = self.config['data_path']  # Assuming you have a 'data_path' in your config
        self.model_path = '../models/gradient_boost_model.pkl'
        self.model = GradientBoostingClassifier()

    def load_data(self):
        self.data = pd.read_csv(self.data_path)
        X = self.data.drop('target_column', axis=1)
        y = self.data['target_column']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        accuracy = self.model.score(self.X_test, self.y_test)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")

    def save(self):
        joblib.dump(self.model, self.model_path)

    def load(self):
        self.model = joblib.load(self.model_path)

    async def predict(self, data):
        features = data[-1:].drop("label", axis=1)
        return self.model.predict(features)[0]

if __name__ == "__main__":
    model = GradientBoostingModel()
    model.load_data()
    model.train()
    model.evaluate()
    model.save()
