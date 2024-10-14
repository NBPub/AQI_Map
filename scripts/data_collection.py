import json
import requests as re
from datetime import datetime
from pathlib import Path
import numpy as np
# from dotenv import load_dotenv # for local use only
from os import getenv

from .kriging_draw import draw_kriging
from .aqi_calc import aqi_calc


def collect_data():
    # load settings via environment variables
    # load_dotenv() # for local use only
    geo_bbox = [float(val) for val in getenv('geo_bbox').split(',')]
    api_key = getenv('api_key')
    variogram_model = getenv('variogram_model', default='hole-effect')
    
    print('Querying Purple Air API')
    # Query Purple Air API
    # https://api.purpleair.com/#api-sensors-get-sensors-data
    base_url = 'https://api.purpleair.com/v1/sensors/'
    payload = {
        'nwlat':geo_bbox[3], 'nwlng':geo_bbox[0], 'selat':geo_bbox[2], 'selng':geo_bbox[1],
        'location_type':0, 
        'fields':'name,latitude,longitude,confidence,position_rating,pm2.5_30minute',
        'max_age':1800, # select sensors updated within last 30 minutes
    }
    api_header = {'X-API-Key' : api_key}
    r = re.get(f'{base_url}', params=payload, headers=api_header)
    
    # failed API request, return error message and placeholders
    if r.status_code !=200:
        print ('Failed API request', r.status_code, r.text)
        return r.text, _, _, _, _
    
    retrieved = datetime.fromtimestamp(r.json()['data_time_stamp']).strftime('%x %X')
    d = r.json()['data']
    
    # store sensor data as lists --> arrays
    sensor_id = []
    sensor_lat = []
    sensor_lng = []
    sensor_name = []
    sensor_aqi = []
    sensor_color = []
    
    # filter for high confidence and location rating
    for sens in d:
        if sens[5]==100 and sens[2]==5:
            sensor_id.append(sens[0])
            sensor_name.append(sens[1])
            sensor_lat.append(sens[3])
            sensor_lng.append(sens[4])
            aqi, color = aqi_calc(sens[6])
            sensor_aqi.append(aqi)
            sensor_color.append(color)
            
    sensor_data = {
        'id': np.array(sensor_id),
        'name': np.array(sensor_name),
        'lat': np.array(sensor_lat),
        'lng': np.array(sensor_lng),
        'aqi': np.array(sensor_aqi),
        'color': np.array(sensor_color),
    }

    # generate Kriging Graph from AQI sensors
    draw_kriging(sensor_data, geo_bbox, model=variogram_model)  
    
    return sensor_data, len(d), retrieved, geo_bbox, variogram_model