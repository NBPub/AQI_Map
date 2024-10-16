from pathlib import Path
import numpy as np
import json
from pykrige.ok import OrdinaryKriging
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def draw_kriging(sensor_data, geo_bbox, model, time_text):
    # darkmagenta (AQI>300) should technically be maroon
    aqi_cmap = LinearSegmentedColormap.from_list(
        name='aqi_cmap', 
        colors=['green','yellow','orange',
                'red','purple','darkmagenta'], 
                                                )

    # grid for Kriging, Kriging, plot and save image
    gx = np.linspace(geo_bbox[0], geo_bbox[1], 300)
    gy= np.linspace(geo_bbox[2], geo_bbox[3], 300)

    OK = OrdinaryKriging(
        sensor_data['lng'], sensor_data['lat'], sensor_data['aqi'],
        variogram_model=model, 
        coordinates_type='geographic', 
                        )
    zvalues, sigmasq = OK.execute('grid', gx, gy)
    
    plt.figure(figsize=(12,8), layout='tight')
    plt.imshow(zvalues, origin='lower', extent=geo_bbox,
               cmap=aqi_cmap, vmin=0, vmax=300)
    plt.gca().set_axis_off()
    
    plt.savefig(Path('data','kriging.png'), 
                bbox_inches='tight', transparent=True)
                
    # save kriging history for future functionality
    for img in Path('data','kriging_history').iterdir():
        if int(img.stem) == 5:
            img.unlink()
        else:
            new_name = f'{int(img.stem)+1}.png'
            img.rename(Path(img.parent, new_name))
  
    plt.savefig(Path('data','kriging_history','0.png'),
                bbox_inches='tight', transparent=True)
    
    # kriging image timestamps          
    if Path('data','kriging_timestamps.json').exists():
        with open(Path('data','kriging_timestamps.json'), 'r') as file:
            old_history = json.load(file)
        history = {int(key)+1:old_history[key] 
                   for key in old_history.keys() 
                   if int(key) < 5}
    else:
        history = {}
    history[0] = time_text
    with open(Path('data','kriging_timestamps.json'), 'w') as file:
        json.dump(history,file)

               
    # save variance plot, std dev --> np.sqrt(np.abs(sigmasq))
    plt.imshow(sigmasq, origin='lower', extent=geo_bbox)
    plt.title(f'Kriging: {model} model')
    plt.ylabel('Latitude')
    plt.xlabel('Longitude')
    plt.colorbar().set_label('σ²', weight='bold', size=16)
    plt.gca().set_axis_on()
    plt.grid(color='k', alpha=0.5)
    plt.savefig(Path('data', 'kriging_variance.png'),
                bbox_inches='tight', transparent=True)   
               
    # save colorbar if it doesn't exist
    if not Path('static', 'colorbar.png').exists():
        fig, ax = plt.subplots()
        krig = plt.imshow(zvalues, origin='lower', extent=geo_bbox,
                          cmap=aqi_cmap, vmin=0, vmax=300)

        plt.colorbar(krig, ax=ax, orientation='horizontal', aspect=40,
                     ).set_label('AQI', weight='bold', size=12)
        ax.remove()
        plt.savefig(Path('static','colorbar.png'), bbox_inches='tight', 
                    transparent=True)