import streamlit as st
import pandas as pd
import time

df = pd.DataFrame({
    'Sensor 1': [1],
    'Sensor 2': [2],
    'Sensor 3': [3],
    'Sensor 4': [4]
})

st.write('Initial dataframe')
st.write(df)

placeholder = st.columns(4)
Sensor1 = placeholder[0].empty()
Sensor2 = placeholder[1].empty()
Sensor3 = placeholder[2].empty()
Sensor4 = placeholder[3].empty()

def update_displayed_metric(df):
    Sensor1.metric(
        label="Sensor 1 RH",
        value=df['Sensor 1'].iloc[-1]
    )
    Sensor2.metric(
        
        label="Sensor 2 RH",
        value=df['Sensor 2'].iloc[-1]
    )
    Sensor3.metric(
        
        label="Sensor 3 RH",
        value=df['Sensor 3'].iloc[-1]
    )
    Sensor4.metric(
        
        label="Sensor 4 RH",
        value=df['Sensor 4'].iloc[-1]
    )

def update_sensor_values(df):
    return df+1

i = 0
while i < 10:
    df = update_sensor_values(df)
    update_displayed_metric(df)
    time.sleep(1)
    i += 1

Sensor1.empty()
Sensor2.empty()
Sensor3.empty()
Sensor4.empty()