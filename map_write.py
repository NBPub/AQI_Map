from scripts.data_load import load_data
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment( 
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)


# load data
sensor_data, sensors, time_text, geo_bbox, kriging_variogram = load_data()
# Failed API request
if type(sensor_data) == str:
    exit

# Sensor JS variables for Leaflet circleMarkers
circle_var_txt = []
base_map = 'https://map.purpleair.com/air-quality-standards-us-epa-aqi?opt=%2F1%2Flp%2Fa10%2Fp604800%2FcC0#17/'
for i,val in enumerate(sensor_data['id']):
    circle_var_txt.append(f'''
var circle = L.circleMarker([{sensor_data['lat'][i]},{sensor_data['lng'][i]}], {{
        color:"{sensor_data['color'][i]}", fillColor:"{sensor_data['color'][i]}",
        fillOpacity:"0.5", radius:5,
}}).addTo(map).bindPopup("{sensor_data['name'][i]} | <b>{sensor_data['aqi'][i]}<b><br><a target='_blank' href='{base_map}{sensor_data['lat'][i]}/{sensor_data['lng'][i]}'>Purple Air {val}</a>");                         
                          ''')
    


# read and write to Jinja2 template
template = env.get_template('map_template.html')
with open(Path('index.html'), 'w', encoding='utf-8') as page:
    page.write(template.render(
        short_time_text=time_text.split(' ')[1][:5], # HR:MIN
        time_text=time_text, # DATE HR:MIN:SEC
        total_sensors=sensors, 
        used_sensors=sensor_data['id'].shape[0],
        circles=circle_var_txt,
        geo_bbox=geo_bbox,
        kriging_variogram=kriging_variogram,
                               ))