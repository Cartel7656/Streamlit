import os
import pandas as pd
import streamlit as st
import joblib
from sklearn.linear_model import LinearRegression

# Get the folder where this script (app.py) is located
BASE_DIR = os.path.dirname(__file__)

# File paths
CSV_FILE = os.path.join(BASE_DIR, "beer-servings.csv")
MODEL_FILE = os.path.join(BASE_DIR, "beer_servings_model.pkl")

st.title("🍺 Beer Servings Predictor")

# Check if model already exists
if not os.path.exists(MODEL_FILE):
    st.write("🔄 Training model for the first time...")

    # Load data
    df = pd.read_csv(CSV_FILE)

    # Features and target
    X = df[["beer_servings", "wine_servings", "spirit_servings"]]
    y = df["total_litres_of_pure_alcohol"] if "total_litres_of_pure_alcohol" in df.columns else df["beer_servings"]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Save model
    joblib.dump(model, MODEL_FILE)
    st.success("✅ Model trained and saved!")
else:
    st.write("✅ Loading existing model...")
    model = joblib.load(MODEL_FILE)

# Sidebar input
st.sidebar.header("Input your servings")
beer = st.sidebar.number_input("Beer servings", min_value=0, value=50)
wine = st.sidebar.number_input("Wine servings", min_value=0, value=20)
spirit = st.sidebar.number_input("Spirit servings", min_value=0, value=10)

# Predict
input_df = pd.DataFrame({"beer_servings": [beer],
                         "wine_servings": [wine],
                         "spirit_servings": [spirit]})

prediction = model.predict(input_df)[0]

st.write(f"🍹 Predicted alcohol consumption: **{prediction:.2f} litres**")
