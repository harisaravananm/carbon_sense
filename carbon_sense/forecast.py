# forecast.py
import pandas as pd
from prophet import Prophet

def load_energy_data(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={'timestamp': 'ds', 'energy_kwh': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    return df

def forecast_energy(df, periods=48):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods, freq='H')
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
