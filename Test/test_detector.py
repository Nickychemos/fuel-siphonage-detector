#Test detector file

import pandas as pd
import pytest
from app.detector import detect_siphonage

@pytest.fixture
def sample_data():
    """Creates sample vehicle telemetry data for testing"""
    data = {
        'vehicle_id': ['V1', 'V1', 'V1'],
        'timestamp': ['2025-03-25 08:00:00', '2025-03-25 08:15:00', '2025-03-25 08:30:00'],
        'location_lat': [1.2921, 1.2921, 1.2921],
        'location_lon': [36.8219, 36.8219, 36.8219],
        'engine_status': ['ON', 'OFF', 'OFF'],
        'fuel_level': [78, 72, 71]
    }
    df = pd.DataFrame(data)
    return df

def test_siphonage_detected(sample_data):
    """Test that siphonage is detected when fuel drops, engine is OFF, and vehicle is stationary."""
    df = detect_siphonage(sample_data)
    
    #Second row should be detected as siphonage
    assert df.loc[1, 'siphonage'] == 1, "Siphonage should be detected when fuel drops, engine is OFF, and no movement"

def test_no_siphonage_when_engine_is_on(sample_data):
    """Test that no siphonage is detected when the engine is ON"""
    df = detect_siphonage(sample_data)
    
    #First row should not be siphonage because the engine is ON
    assert df.loc[0, 'siphonage'] == 0, "Siphonage should not be detected when engine is ON"

def test_no_siphonage_when_vehicle_moves():
    """Test that siphonage is not detected when the vehicle has moved"""
    data = {
        'vehicle_id': ['V1', 'V1'],
        'timestamp': ['2025-03-25 08:00:00', '2025-03-25 08:15:00'],
        'location_lat': [1.2921, 1.2930],  # Changed latitude
        'location_lon': [36.8219, 36.8225],  # Changed longitude
        'engine_status': ['ON', 'OFF'],
        'fuel_level': [78, 72]
    }
    df = pd.DataFrame(data)
    df = detect_siphonage(df)
    
    #Should not be siphonage since the vehicle has moved
    assert df.loc[1, 'siphonage'] == 0, "Siphonage should not be detected if the vehicle is moving"

if __name__ == '__main__':
    pytest.main()
