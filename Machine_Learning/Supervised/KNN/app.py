import streamlit as st
import joblib

# Load trained model
model = joblib.load("model.pkl")

st.title("🏠 House Price Prediction")
st.write("KNN Regression")

# User input
area = st.number_input(
    "Enter House Area (sq.ft)",
    min_value=500,
    max_value=5000,
    value=1600
)

# Prediction
if st.button("Predict Price"):

    prediction = model.predict([[area]])

    st.success(
        f"Predicted House Price: ₹{prediction[0]:.2f} Lakhs"
    )

# streamlit run app.py