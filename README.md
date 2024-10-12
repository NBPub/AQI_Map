# AQI Map

*to be populated . . . for now:*

**Basics**
 - geographic region specified via bounding box
 - Purple Air API used to retrieve sensor PM2.5 data
   - AQI calculated using 30 min average
 - Sensor data used to interpolate AQI over region by OrdinaryKriging
 - Kriging result overlaid over dynamic map on web page
   - Mapping and tiles provided by Leaflet and OpenStreetMap
 - beta version of page will be hosted on this repository and updated via Github actions
   - ***switch parameters specified by environmental variables to repository secrets***
   - necessary elements for web page left empty, will test run code and see if everything works
     - data (kriging graphs), colorbar image, etc . . . 