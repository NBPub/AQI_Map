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
    print(sensor_data)
    exit
    
# "MM/DD HR:MIN" from "MM/DD/YY HR:MIN:SEC TZ"
short_time_text = f"{time_text.split(' ')[0][:5]} {time_text.split(' ')[1][:5]}"
    
    
# save leaflet circleMarkers in separate JS file, maintain history
markers = sorted(Path('data','markers_history').glob('*.js'))[::-1]
for file in markers:
    if int(file.stem) >= 9:
        file.unlink()
    else:
        file.rename(Path(file.parent, f'{int(file.stem)+1}.js'))
        
base_map_link = 'https://map.purpleair.com/air-quality-standards-us-epa-aqi?opt=%2F1%2Flp%2Fa10%2Fp604800%2FcC0#17/'
template = env.get_template('markers_template.js')
with open(Path('data', 'markers_history','0.js'), 'w', encoding='utf-8') as page:
    page.write(template.render(
        sensor_data=sensor_data, base_map_link=base_map_link,
        time_text=short_time_text,
        ))


    
# read and write to main Jinja2 template
template = env.get_template('map_template.html')
with open(Path('index.html'), 'w', encoding='utf-8') as page:
    page.write(template.render(
        short_time_text=short_time_text,
        time_text=time_text,
        total_sensors=sensors, 
        used_sensors=sensor_data['id'].shape[0],
        geo_bbox=geo_bbox,
        kriging_variogram=kriging_variogram,
                               ))