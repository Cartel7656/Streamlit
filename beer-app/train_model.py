import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

BASE_DIR = os.path.dirname(__file__)
CSV_FILE = os.path.join(BASE_DIR, "beer-servings.csv")
MODEL_FILE = os.path.join(BASE_DIR, "beer_servings_model.pkl")

def train_model():
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file not found at {CSV_FILE}")
        return

    # Load data
    df = pd.read_csv(CSV_FILE)

    # Drop rows with missing values in features
    df = df.dropna(subset=["beer_servings", "wine_servings", "spirit_servings"])

    X = df[["beer_servings", "wine_servings", "spirit_servings"]]
    y = df["total_litres_of_pure_alcohol"] if "total_litres_of_pure_alcohol" in df.columns else df["beer_servings"]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    joblib.dump(model, MODEL_FILE)
    print(f"Model trained and saved to {MODEL_FILE}")

if __name__ == "__main__":
    train_model()
