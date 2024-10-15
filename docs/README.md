# AQI Map Documentation

**Contents**
 - [Usage](/docs#usage)
   - [Workflow](/docs#workflow)
   - [Requirements](/docs#python-requirements)
   - [Environment Variables](/docs#environment-variables)
 - [Run Locally](/docs#local-use)
 - [Kriging](/docs#kriging)
   - [Variogram Models](/docs#variogram-model-selection)
 - [Web Page](/docs#web-page)
   - [LeafletJS](/docs#leafletjs)
   
   
## Usage

Fork this repository and set repository [variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables) 
to create your own AQI map. [Secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) 
should be used to store your API key. A Github [workflow](/.github/workflows/main.yml) runs the [main script(/map_write.py) 
at a [specified interval](https://en.wikipedia.org/wiki/Cron) to update the data and webpage.

The code can also be downloaded and run [locally](/docs#local-use), although some changes are 
[required](/docs#required-modifications) and [recommended](/docs#recommended-modifications). 

### Workflow

[Actions YAML file](/.github/workflows/main.yml) 
 - checks out repository
 - runs [`map_write`](/map_write.py) with Python 3.12
   - installs requirements, loads environment variables
     - Python package installation can specify packages listed below or use a [requirements.txt](/requirements.txt) file
   - `map_write` calls each script located in the [scripts](/scripts) subdirectory
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

The example [.env](/example.env) file also contains information about the required environment variables. 
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
   - how to select a model [example](/docs#variogram-model-selection), anecdotally . . . 
     - `hole-effect` works best for the current page's bounds `-121.74, -120.78, 43.63, 44.42`, smaller region
	 - `gaussian` or `exponential` work best for the coordinate bounds listed in the example file, larger region
 - ****local_time**
   - specify a [timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to convert from UTC
   - only needed when running on a repository, code changes [required](/docs#required) for local use

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
 - store data retrieved from the API call, 
   - returned data as JSON or 
   - processed data using [`np.save`](https://numpy.org/doc/stable/reference/generated/numpy.save.html)
 - check modification time of data before making another API call, and alternatively use stored data
   - *AQI_Map code does not store data as a dictionary and uses NumPy arrays. These must be converted to lists to be JSON serializable*.
 - add/improve print statements or logging to track API calls or failed requests
 - alter HTML [template](/templates/map_template.html) to your preferences, add more helpful information

**API return to JSON**

```python
# API call request stored as "r"
data = r.json()['data']

for sens in data:
	ind = sens[0]
	sensors[ind] = {
		'PM2.5':sens[6],
		'name':sens[1],
		'rating':sens[2],
		'lat':sens[3],
		'lng':sens[4],
		'confident': True if sens[5]==100 else False,
}
with open(Path('data','sensors.json'), 'w') as file:
	json.dump(sensors, file)
```

**File modified check**

```python
if Path('data','sensors.json').exists():
	last_load = datetime.datetime.fromtimestamp(Path('data','sensors.json').stat().st_mtime)
	time_since = datetime.datetime.now() - last_load

if not Path('data','sensors.json').exists() or time_since > datetime.timedelta(minutes=30):
	# stale data or first call, replace "_" with items returned from data collection code
	print('making API call')
	sensors  = collect_data()
else:
	print('loading sensor data from files')
	with open(Path('data','sensors.json'), 'r') as file:
		sensors = json.load(file)

# finish preparing data for template
```

## Kriging

Each sensor's PM2.5 concentration (30 minute average) is [converted](/scripts/aqi_calc.py) to an AQI value, 
and then Kriging provides AQI interpolation over the geographical region specified. PyKrige is used for 
[Ordinary Kriging](https://geostat-framework.readthedocs.io/projects/pykrige/en/stable/generated/pykrige.ok.OrdinaryKriging.html#pykrige.ok.OrdinaryKriging) 
calculation.

Resources: [Wikipedia](https://en.wikipedia.org/wiki/Kriging) | [Columbia Public Health](https://www.publichealth.columbia.edu/research/population-health-methods/kriging-interpolation)

### Variogram Model Selection

Many different variogram models are available for `OrdinaryKriging`, and the ideal selection depends 
on the sensor data and extent of the region. It may change as the data changes. The fit can be visualized, 
`enable_plotting=True`, and statistics, `enable_statistics=True`, can be returned to evaluate various models.
It can also be useful to compare the resulting variance plots.


**Kriging model evaluation, example with statistics**

```python
# evaluate variogram model statistics, per docs:
# "ideally Q1 is close to zero, Q2 is close to 1, and cR is as small as possible"

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



## [Web Page](https://nbpub.github.io/AQI_Map/)

Data and graphs are written into a static HTML page using [Jinja2](https://jinja.palletsprojects.com/en/), 
see the map writing [script](/map_write.py) and the [template](/templates/map_template.html). The resulting 
web page is hosted on the repository using [Github Pages](https://pages.github.com/) depolyment.

### LeafletJS

[LeafletJS](https://leafletjs.com/) is used to embed and extend [OpenStreetMap](https://www.openstreetmap.org/) tiles. 
The kriging interpolation is overlaid on the map tiles, sensor data is included as 
[circle markers](https://leafletjs.com/reference.html#circlemarker), an AQI colorbar is provided, 
and a [plugin](https://github.com/ardhi/Leaflet.MousePosition) is used to display mouse position coordinates 
on the upper right corner.