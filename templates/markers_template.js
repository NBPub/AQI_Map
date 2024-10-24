{% for id in sensor_data['id'] %}
  var circle = L.circleMarker([{{ sensor_data['lat'][loop.index0] }}, {{ sensor_data['lng'][loop.index0] }}], {{ '{' }}
	color: "{{ sensor_data['color'][loop.index0] }}", fillColor:"{{ sensor_data['color'][loop.index0] }}", 
	fillOpacity:"0.5", radius:5,
  {{ '}' }}).addTo(map).bindPopup("{{ sensor_data['name'][loop.index0] }} | <b>{{ sensor_data['aqi'][loop.index0]}}</b><br><a target='_blank' href='{{ base_map_link }}{{sensor_data['lat'][loop.index0] }}/{{ sensor_data['lng'][loop.index0] }}'>Purple Air {{ id }}</a> {{ time_text }}");
{% endfor %}