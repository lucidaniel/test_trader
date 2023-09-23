import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

# Load your data
data = pd.read_csv('path_to_your_new_data.csv')

# Split data into features and labels
X = data.drop('target_column', axis=1)
y = data['target_column']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = GradientBoostingClassifier()

# Train the model
model.fit(X_train, y_train)

# Optionally, you can evaluate the model's performance on the test set
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the updated model
joblib.dump(model, 'models/gradient_boost_model.pkl')

async def load_model(model_path="models/gradient_boost_model.pkl"):
    """
    Asynchronously load the pre-trained Gradient Boosting model.
    
    Parameters:
    - model_path (str): The path to the saved model file. Default is "models/gradient_boost_model.pkl".
    
    Returns:
    - GradientBoostingClassifier: The loaded model.
    """
    return joblib.load(model_path)

async def make_prediction(model, data):
    """
    Asynchronously make a trading prediction based on the given data.
    
    Parameters:
    - model (GradientBoostingClassifier): The pre-trained model.
    - data (DataFrame): The processed trading data.
    
    Returns:
    - int: The trading prediction (1 for buy, 0 for hold, -1 for sell).
    """
    features = data[-1:].drop("label", axis=1)
    return model.predict(features)[0]

async def train_model(data, labels, model_path="models/gradient_boost_model.pkl"):
    """
    Asynchronously train a new Gradient Boosting model.
    
    Parameters:
    - data (DataFrame): The training data.
    - labels (Series): The training labels.
    - model_path (str): The path to save the trained model. Default is "models/gradient_boost_model.pkl".
    
    Returns:
    - GradientBoostingClassifier: The trained model.
    """
    model = GradientBoostingClassifier()
    model.fit(data, labels)
    joblib.dump(model, model_path)
    return model

if __name__ == "__main__":
    import asyncio

    async def main():
        # Test the GradientBoostClassifier functions if this script is run directly.
        # For demonstration purposes, using dummy data and labels.
        data = pd.DataFrame({"feature1": [1, 2, 3], "feature2": [4, 5, 6], "label": [1, 0, -1]})
        labels = data["label"]
        model = await train_model(data.drop("label", axis=1), labels)
        prediction = await make_prediction(model, data)
        print(f"Prediction: {prediction}")

    asyncio.run(main())