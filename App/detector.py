#Detector file

import pandas as pd
from geopy.distance import geodesic

def detect_siphonage(df):
    """
    Detects siphonage events based on:
    - Fuel drop while the engine is OFF
    - Minimal location change (vehicle stationary)
    """
    
    #Converting timestamp column to datetime and sort values per vehicle
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['vehicle_id', 'timestamp'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    #Calculating time difference in minutes
    df['time_diff'] = df.groupby('vehicle_id')['timestamp'].diff().dt.total_seconds() / 60
    df['time_diff'].fillna(0, inplace=True)

    #Calculating fuel drop
    df['fuel_drop'] = df.groupby('vehicle_id')['fuel_level'].diff().fillna(0)

    #Tracking location changes
    df['prev_lat'] = df.groupby('vehicle_id')['location_lat'].shift(1)
    df['prev_lon'] = df.groupby('vehicle_id')['location_lon'].shift(1)

    def check_movement(row, distance_threshold=0.01):
        if pd.isnull(row['prev_lat']) or pd.isnull(row['prev_lon']):
            return 0
        prev_coords = (row['prev_lat'], row['prev_lon'])
        current_coords = (row['location_lat'], row['location_lon'])
        distance = geodesic(prev_coords, current_coords).km
        return int(distance >= distance_threshold)
    
    df['is_moving'] = df.apply(check_movement, axis=1)
    df.drop(columns=['prev_lat', 'prev_lon'], inplace=True)

    #Detecting siphonage (fuel drop while stationary and engine OFF)
    df['siphonage'] = ((df['fuel_drop'] < 0) & (df['engine_status'] == 'OFF') & (df['is_moving'] == 0)).astype(int)

    return df
