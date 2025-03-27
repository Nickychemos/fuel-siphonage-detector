#Utility file

import pandas as pd
import numpy as np
from geopy.distance import geodesic

def preprocess_data(df):
    """
    Preprocesses vehicle telemetry data for siphonage detection.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['vehicle_id', 'timestamp'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    df['time_diff'] = df.groupby('vehicle_id')['timestamp'].diff().dt.total_seconds() / 60
    df['time_diff'].fillna(0, inplace=True)

    df['fuel_drop'] = df.groupby('vehicle_id')['fuel_level'].diff().fillna(0)
    df['lat_change'] = df.groupby('vehicle_id')['location_lat'].diff().abs().fillna(0)
    df['lon_change'] = df.groupby('vehicle_id')['location_lon'].diff().abs().fillna(0)

    df['prev_lat'] = df.groupby('vehicle_id')['location_lat'].shift(1)
    df['prev_lon'] = df.groupby('vehicle_id')['location_lon'].shift(1)

    def check_movement(row, distance_threshold=0.01):
        if pd.isnull(row['prev_lat']) or pd.isnull(row['prev_lon']):
            return 0 #-->For the first column where there is no movement
        prev_coords = (row['prev_lat'], row['prev_lon'])
        current_coords = (row['location_lat'], row['location_lon'])
        distance = geodesic(prev_coords, current_coords).km
        return int(distance >= distance_threshold)
    
    df['is_moving'] = df.apply(check_movement, axis=1)
    df.drop(columns=['prev_lat', 'prev_lon'], inplace=True)

    df['engine_status_flag'] = np.where(df['engine_status'] == 'ON', 1, 0) ##--> Creating a new column that shows the encoded engine status

    return df
