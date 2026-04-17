import warnings
warnings.filterwarnings('ignore')

import streamlit as st


def input_features():
    temperature = st.sidebar.slider('Temperature', 0.0, 50.0, 25.0)
    humidity = st.sidebar.slider('Humidity', 0.0, 100.0, 50.0)
    pm25 = st.sidebar.slider('PM2.5', 0.0, 200.0, 20.0)
    pm10 = st.sidebar.slider('PM10', 0.0, 300.0, 30.0)
    no2 = st.sidebar.slider('NO2', 0.0, 200.0, 20.0)
    so2 = st.sidebar.slider('SO2', 0.0, 100.0, 10.0)
    co = st.sidebar.slider('CO', 0.0, 10.0, 1.0)
    prox = st.sidebar.slider('Proximite_zones_industrielles', 0.0, 20.0, 5.0)
    densite = st.sidebar.slider('Densite_population', 0.0, 1000.0, 300.0)

    data = {
        'Temperature': temperature,
        'Humidity': humidity,
        'PM2.5': pm25,
        'PM10': pm10,
        'NO2': no2,
        'SO2': so2,
        'CO': co,
        'Proximite_zones_industrielles': prox,
        'Densite_population': densite
    }

    return data