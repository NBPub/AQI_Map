# AQI Map Documentation

**Contents**
 - [Usage](/docs#usage)
   - [Github Workflow](/docs#github-workflow)
   - [Requirements](/docs#python-requirements)
   - [Environment Variables](/docs#environment-variables)
 - [Run Locally](/docs#local-use)
   - [Required Changes](/docs#required-modifications)
   - [Recommended Changes](/docs#recommended-modifications)
 - [Web Page](/docs#web-page)
   - [LeafletJS](/docs#leafletjs)
   - [AQI History](/docs#aqi-history)
 - [Kriging](/docs#kriging)
   - [Variogram Models](/docs#variogram-model-selection)
     - [Central Oregon Example](/docs#central-oregon-model-comparison)
	 - [Oregon Example](/docs#oregon-model-comparison)

   
   
## Usage

Fork this repository and set repository [variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables) 
to create your own AQI map. [Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) 
should be used to store your API key. A Github [workflow](/.github/workflows/main.yml) runs the [main script](/map_write.py) 
at a [specified interval](https://en.wikipedia.org/wiki/Cron) to update the data and webpage.

The code can also be downloaded and run [locally](/docs#local-use), although some changes are 
[required](/docs#required-modifications) and [recommended](/docs#recommended-modifications). 

### Github Workflow

[Actions YAML file](/.github/workflows/main.yml) 
 - checks out repository
 - runs [`map_write`](/map_write.py) with Python 3.12
   - installs requirements, loads environment variables
     - Python package installation can specify packages listed below or use a [requirements.txt](/requirements.txt) file
   - `map_write` calls code located in the [scripts](/scripts) subdirectory
   - clears generated `__pycache__` directories 
 - commits updated files and pushes changes back to repository


### Python Requirements

**[requirements.txt](/requirements.txt) provides a full list of installed packages**
  - [requests](https://requests.readthedocs.io/en/latest/)
  - [NumPy](https://numpy.org/doc/stable/)
  - [Jinja2](https://jinja.palletsprojects.com/en/)
  - [matplotlib](https://matplotlib.org/stable/)
  - [PyKrige](https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/)
  - **remote use only**
    - [pytz](https://pythonhosted.org/pytz/)
  - **local use only**
    - [python-dotenv](https://github.com/theskumar/python-dotenv)
	
*AQI_Map code has been successfully run with Python 3.10, 3.11, and 3.12*

### Environment Variables

The example [.env](/example.env) file contains information about the required environment variables. 
They are stored and used as secrets on this repository, although only the API key will be kept private 
in the resulting webpage. A `.env` file is required for local use.

 - **api_key**
   - Purple Air API "Read" Key is required for data collection
     - [API Dashboard](https://develop.purpleair.com/dashboards/keys)
     - [API Docs](https://api.purpleair.com/#api-welcome-using-api-keys)
 - **geo_bbox**
   - geographical "bounding box" [coordinates](https://en.wikipedia.org/wiki/Geographic_coordinate_system) specify which sensors to query and where the map will be colored
   - format: `<lng1>, <lng2>, <lat1>, <lat2>`
 - **variogram_model**
   - variogram model used for Ordinary Kriging, see PyKrige [documentation](https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/generated/pykrige.ok.OrdinaryKriging.html#pykrige.ok.OrdinaryKriging)
   - [example](/docs#variogram-model-selection) code below for model selection, anecdotally . . . 
     - `hole-effect` works best for the current page's bounds, a relatively small region
	 - `gaussian` or `exponential` work best for the coordinate bounds listed in the example file, larger regions
 - **local_time**
   - specify a [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to convert from UTC
   - only needed when running on a repository, see code changes [required](/docs#required) for local use

## Local Use

AQI_Map code can be modified for local use. As mentioned above, environment variables should be specified in a `.env` file in the 
code's root directory and read with an additional package, [python-dotenv](https://github.com/theskumar/python-dotenv). A virtual 
environment, [`venv`](https://docs.python.org/3/library/venv.html), is recommended to install the requirements and run the code.

### Required Modifications

[data_collection.py](/scripts/data_collection.py)
 - Uncomment lines that import and use **python-dotenv** ([7](/data_collection.py#L7), [16](/data_collection.py#L16))
 - Remove timezone conversion of **data_time_stamp** (lines [41](/data_collection.py#L41)-[43](/data_collection.py#L43))
   - Replace with `retrieved = datetime.fromtimestamp(r.json()['data_time_stamp']).strftime('%x %X')`
   
### Recommended Modifications
 - store data retrieved from the [API call](https://api.purpleair.com/#api-sensors-get-sensors-data)
   - data processed into a dictionary as a JSON file (example below)
   - data processed into NumPy arrays using [`np.save`](https://numpy.org/doc/stable/reference/generated/numpy.save.html)
 - check modification time of stored data before making another API call
   - *AQI_Map code does not store data as a dictionary and uses NumPy arrays. These must be converted to lists to be JSON serializable*.
 - add/improve prints or logging to track API calls and failed requests
 - alter HTML [template](/templates/map_template.html) to your preferences

**API return to labelled JSON**

```python
import json
from pathlib import Path

# API call request stored as "r"
data = r.json()['data']

for sens in data:
	ind = sens[0] # ID
	sensors[ind] = {
		'PM2.5':sens[6], # measurement
		'name':sens[1], # name
		'rating':sens[2], # location rating
		'lat':sens[3], # latitude
		'lng':sens[4], # longitude
		'confident': True if sens[5]==100 else False, # measurement confidence
}
with open(Path('data','sensors.json'), 'w') as file:
	json.dump(sensors, file)
```

**File modified check**

```python
import datetime 
import json
from pathlib import Path

if Path('data','sensors.json').exists():
	last_load = datetime.datetime.fromtimestamp(Path('data','sensors.json').stat().st_mtime)
	time_since = datetime.datetime.now() - last_load

if not Path('data','sensors.json').exists() or time_since > datetime.timedelta(minutes=30):
	# stale data or first call
	print('making API call')
	sensors  = collect_data()
else:
	# recent data available
	print('loading sensor data from files')
	with open(Path('data','sensors.json'), 'r') as file:
		sensors = json.load(file)

# finish preparing data for template
```

## Web Page

Data and graphs are written into a static HTML [page](/index.html) using [Jinja2](https://jinja.palletsprojects.com/en/), 
see the map writing [script](/map_write.py) and the [template](/templates/map_template.html). The resulting 
web page is [hosted](https://nbpub.github.io/AQI_Map/) on the repository using [Github Pages](https://pages.github.com/) depolyment.

### LeafletJS

[LeafletJS](https://leafletjs.com/) is used to embed and extend [OpenStreetMap](https://www.openstreetmap.org/) tiles. 
The kriging interpolation is overlaid on the map tiles, sensor data is included as [circle markers](https://leafletjs.com/reference.html#circlemarker), 
an AQI [colorbar](https://raw.githubusercontent.com/NBPub/AQI_Map/refs/heads/main/static/colorbar.png) is provided, 
and a [plugin](https://github.com/ardhi/Leaflet.MousePosition) is used to display mouse position coordinates on the upper right corner.

### AQI History

 - buttons allow changing Kriging overlay and sensor markers from current to one of previous 9 images
   - indicated by timestamp on top of page
   - may add automatic changing for animation effect

## Kriging

Each sensor's PM2.5 concentration (30 minute average) is [converted](/scripts/aqi_calc.py) to an AQI value, 
and then kriging provides AQI interpolation over the geographical region specified. PyKrige is used for 
[Ordinary Kriging](https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/generated/pykrige.ok.OrdinaryKriging.html#pykrige.ok.OrdinaryKriging) 
calculation.

External Resources: [Wikipedia](https://en.wikipedia.org/wiki/Kriging) | [Columbia Public Health](https://www.publichealth.columbia.edu/research/population-health-methods/kriging-interpolation)

### Variogram Model Selection

Different variogram models are available for `OrdinaryKriging`, and the ideal selection depends 
on the sensor data and extent of the region. It may change as the data changes. The kriging fit can be visualized, 
`enable_plotting=True`, and statistics, `enable_statistics=True`, can be returned to evaluate various models.
It is also useful to compare their resulting [variance plots](https://raw.githubusercontent.com/NBPub/AQI_Map/refs/heads/main/data/kriging_variance.png). 
Example plotting results are shown for [Central Oregon](/docs#central-oregon-model-comparison)) and [Oregon](/docs#oregon-model-comparison)) below.


**Kriging model evaluation, example with statistics**

> ideally Q1 is close to zero, Q2 is close to 1, and cR is as small as possible

```python
# evaluate variogram model statistics

for vm in ['linear', 'power', 'gaussian', 'spherical', 'exponential', 'hole-effect']:
    OK = OrdinaryKriging(
            sensor_data['lng'], sensor_data['lat'], sensor_data['aqi'],
            variogram_model=vm, verbose=False, enable_statistics =True,
            coordinates_type='geographic', 
    )

    print('\t',vm)
    OK.print_statistics()
    print()
```

#### Central Oregon Model Comparison

*Results are not definitive and depend on the data's distribution at a given time*

| Variogram Model | Kriging Result | √ Variance |
|-----------------|----------------|----------|
| linear<br>`Q1 = 0.017, Q2 = 0.350, cR = 1174` | ![](/docs/variogram_model_images/co_linear.png) | ![](/docs/variogram_model_images/co_linear_sd.png) |
| power<br>`Q1 = 0.031, Q2 = 0.262, cR = 673` | ![](/docs/variogram_model_images/co_power.png) | ![](/docs/variogram_model_images/co_power_sd.png) |
| gaussian<br>`Q1 = 0.044, Q2 = 0.477, cR = 724` | ![](/docs/variogram_model_images/co_gaussian.png) | ![](/docs/variogram_model_images/co_gaussian_sd.png) |
| spherical<br>`Q1 = 0.055, Q2 = 0.474, cR = 547` | ![](/docs/variogram_model_images/co_spherical.png) | ![](/docs/variogram_model_images/co_spherical_sd.png) |
| exponential<br>`Q1 = 0.101, Q2 = 0.720, cR = 463` | ![](/docs/variogram_model_images/co_exponential.png) | ![](/docs/variogram_model_images/co_exponential_sd.png) |
|  hole-effect<br>`Q1 = 0.106, Q2 = 0.757, cR = 465` | ![](/docs/variogram_model_images/co_hole-effect.png) | ![](/docs/variogram_model_images/co_hole-effect_sd.png) |

#### Oregon Model Comparison

*Results are not definitive and depend on the data's distribution at a given time*

| Variogram Model | Kriging Result | √ Variance |
|-----------------|----------------|----------|
| linear<br>`Q1 = 0.196, Q2 = 2.95, cR = 3056` | ![](/docs/variogram_model_images/or_linear.png) | ![](/docs/variogram_model_images/or_linear_sd.png) |
| power<br>`Q1 = 0.125, Q2 = 1.60, cR = 1641` | ![](/docs/variogram_model_images/or_power.png) | ![](/docs/variogram_model_images/or_power_sd.png) |
| gaussian<br>`Q1 = 0.037 Q2 = 0.626, cR = 367` | ![](/docs/variogram_model_images/or_gaussian.png) | ![](/docs/variogram_model_images/or_gaussian_sd.png) |
| spherical<br>`Q1 = 0.056, Q2 = 0.825, cR = 415` | ![](/docs/variogram_model_images/or_spherical.png) | ![](/docs/variogram_model_images/or_spherical_sd.png) |
| exponential<br>`Q1 = 0.138, Q2 = 2.67, cR = 389` | ![](/docs/variogram_model_images/or_exponential.png) | ![](/docs/variogram_model_images/or_exponential_sd.png) |
|  hole-effect<br>`Q1 = 0.120, Q2 = 3.92, cR = 435` | ![](/docs/variogram_model_images/or_hole-effect.png) | ![](/docs/variogram_model_images/or_hole-effect_sd.png) |

