import os
import pandas as pd


def get_station_data(station_id):
    filename = f"data-small/TG_STAID{str(station_id).zfill(6)}.txt"

    if not os.path.exists(filename):
        return None

    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df.columns = [col.strip() for col in df.columns]
    return df
