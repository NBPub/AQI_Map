# [AQI Map](https://nbpub.github.io/AQI_Map/)

This repository is used to host a demo page for an AQI Map, and for now, is continuously updated. 
It is currently set within [Central Oregon](https://en.wikipedia.org/wiki/Central_Oregon), 
but the code allows for any region to be specified by coordinate bounds.

Detailed information is located in the [documentation](/docs#aqi-map-documentation) page.

 - [Motivation](/#motivation)
 - [Overview](/#overview)
 
## Motivation

Late summer typically brings in smoke, and fine particulate matter from wildfires. 
The map was created for an easy way to visualize up-to-date particulate matter 
concentration (**[PM2.5](https://www.epa.gov/pm-pollution/particulate-matter-pm-basics)**) 
and resulting air quality indices (**[AQI](https://www.airnow.gov/aqi/aqi-basics/)**).


## Overview

 - Purple Air [API](https://api.purpleair.com/) used to retrieve sensor PM2.5 data
   - AQI calculated using 30 min average
   - Only sensors providing confident, recent data and with high location ratings used
 - Sensor data used to interpolate AQI over region by [OrdinaryKriging](https://en.wikipedia.org/wiki/Kriging)
   - Variance [plot](/data/kriging_variance.png) visualizes interpolation uncertainty over region
 - Kriging result overlaid over dynamic map on [web page](https://nbpub.github.io/AQI_Map/)
   - Mapping and tiles provided by [Leaflet](https://leafletjs.com/) and [OpenStreetMap](https://www.openstreetmap.org/)
   - page hosted by [Github Pages](https://pages.github.com/)
 - Data and image overlays updated via [Github Actions](https://github.com/NBPub/AQI_Map)
   - currently every hour, may stop or change in the future
	 
