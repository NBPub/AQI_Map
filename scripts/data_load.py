from .data_collection import collect_data
from pathlib import Path


def load_data():
    # Create subfolders if they don't exist
    if not Path('data').exists():
        Path('data').mkdir()
    if not Path('static').exists():
        Path('static').mkdir()  
    if not Path('data', 'kriging_history').exists():
        Path('data', 'kriging_history').mkdir()
    
    # Query API and generate graphs
    sensor_data, n_sensors, time_text, geo_bbox, variogram_model  = collect_data()
    # Failed API request
    if type(sensor_data) == str:
        return sensor_data, _, _, _
        
    return sensor_data, n_sensors, time_text, geo_bbox, variogram_model
