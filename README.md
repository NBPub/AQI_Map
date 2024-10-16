# [AQI Map](https://nbpub.github.io/AQI_Map/)

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
   - AQI calculated using 30 min average
   - Only sensors providing confident, recent data, with high location ratings used
 - Sensor data used to interpolate AQI over region by [Ordinary Kriging](https://en.wikipedia.org/wiki/Kriging)
   - Variance [plot](/data/kriging_variance.png) visualizes interpolation uncertainty over region
 - Kriging result overlaid over dynamic map on [web page](/index.html)
   - Mapping and tiles provided by [Leaflet](https://leafletjs.com/) and [OpenStreetMap](https://www.openstreetmap.org/)
   - [Hosted](https://nbpub.github.io/AQI_Map/) using [Github Pages](https://pages.github.com/)
 - Data and image overlays updated via [Github Actions](https://github.com/NBPub/AQI_Map)
   - Currently every half hour, may stop or change in the future
	 
