
import streamlit as st
import pandas as pd
import joblib
from datetime import time

# Load the trained model
model = joblib.load("traffic_model.pkl")

st.set_page_config(page_title="Traffic Prediction System", page_icon="🚗")

st.title("🚗 Traffic Prediction System")
st.write("Predict traffic volume using time and weather conditions.")

st.subheader("Enter Traffic Conditions")

col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input("Date")
    selected_time = st.time_input("Time", value=time(8, 0))
    temp = st.number_input(
        "Temperature (Kelvin)",
        min_value=200.0,
        max_value=330.0,
        value=288.0
    )
    rain = st.number_input(
        "Rainfall (mm in 1 hour)",
        min_value=0.0,
        max_value=100.0,
        value=0.0
    )

with col2:
    snow = st.number_input(
        "Snowfall reading",
        min_value=0.0,
        max_value=10.0,
        value=0.0
    )
    clouds = st.slider("Cloud coverage (%)", 0, 100, 50)

    weather = st.selectbox(
        "Weather condition",
        [
            "Clear", "Clouds", "Rain", "Drizzle", "Snow",
            "Mist", "Fog", "Haze", "Thunderstorm", "Smoke", "Squall"
        ]
    )

    holiday = st.text_input("Holiday name (or None)", value="None")

if st.button("Predict Traffic", type="primary"):
    prediction_input = pd.DataFrame([{
        "hour": selected_time.hour,
        "day_of_week": selected_date.weekday(),
        "month": selected_date.month,
        "temp": temp,
        "rain_1h": rain,
        "snow_1h": snow,
        "clouds_all": clouds,
        "weather_main": weather,
        "holiday": holiday.strip() or "None"
    }])

    prediction = model.predict(prediction_input)[0]

    st.success(
        f"Predicted traffic volume: {max(0, round(prediction))} vehicles"
    )

    st.caption(
        "This is a model estimate based on historical I-94 traffic data, "
        "not live traffic information."
    )
