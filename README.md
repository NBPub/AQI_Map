# [AQI Map](https://nbpub.github.io/AQI_Map/)

**Page will stop updating when API credits are consumed, estimated date: `02 Jan 2025`**

This repository is used to host a demo page for an AQI Map, and for now, is continuously updated. 
It is currently set within [Central Oregon](https://en.wikipedia.org/wiki/Central_Oregon), 
but the code allows for any region to be specified by coordinate bounds.

Detailed deployment information is located on the [documentation](/docs#aqi-map-documentation) page.

 
## Motivation

Late summer typically brings in smoke and fine particulate matter from wildfires. 
The map was created to provide quickly interpretable, up-to-date visualization for particulate matter
concentration (**[PM2.5](https://www.epa.gov/pm-pollution/particulate-matter-pm-basics)**) 
and resulting air quality indices (**[AQI](https://www.airnow.gov/aqi/aqi-basics/)**).


## Overview

 - Purple Air [API](https://api.purpleair.com/) used to retrieve sensor PM2.5 data
   - AQI calculated using 60 min average, updated every 2 hours
   - Only sensors providing confident, recent data, with high location ratings used
   - API credits are limited and do not reset, see [usage report](#api-limitation) below.
 - Sensor data used to interpolate AQI over region by [Ordinary Kriging](https://en.wikipedia.org/wiki/Kriging)
   - Variance [plot](/data/kriging_variance.png) visualizes interpolation uncertainty over region
 - Kriging result overlaid over dynamic map on [web page](/index.html)
   - Mapping and tiles provided by [Leaflet](https://leafletjs.com/) and [OpenStreetMap](https://www.openstreetmap.org/)
   - [Hosted](https://nbpub.github.io/AQI_Map/) using [Github Pages](https://pages.github.com/)
 - Data and image overlays updated via [Github Actions](https://github.com/NBPub/AQI_Map)
   - webpage allows scrolling between current and previous 9 results
 
## API Limitation

As of 02 Nov 2024, a new API key has been obtained and the site will be updated until its points (1,000,000) are consumed. 

 - update every 2 hours for 12 total calls a day
 - approximately 1,378 points per call totaling to 16,530 points per day | `16528.4 ± 46.3, n=7`
   - points per call varies with amount of sensors, sensor data returned from `[get_sensors](https://api.purpleair.com/#api-sensors-get-sensors-data)` request
   - for this site's selected region, typically 180 to 200 sensors are queried
 - at this rate, points will be consumed in about 60.5 days
   - from 03 Nov 2024 start date to 02 Jan 2025
   
**approximates per call**
   
| Sensors | Data Used  | Points |
|---------|------------|--------|
| 180 to 200 | 12 to 12.25 kb | 1370 to 1380  |   


## Next Up 

 - Remove existing map markers when scrolling through sensor data timepoints and Kriging results
 - add button to automatically scroll through results
   
	 
