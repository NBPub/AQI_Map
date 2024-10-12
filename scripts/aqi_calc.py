# Bounding points for AQI ranges used to fit slope and y-intercept
# https://forum.airnowtech.org/t/the-aqi-equation-2024-valid-beginning-may-6th-2024/453
# PM2.5 concentration (µg/m³) to AQI


def aqi_calc(conc):
    if conc <= 9:
        p1 = 0,0
        p2 = 9,50
        c = '#008000' # 0-50: green
    elif conc <= 35.4:
        p1 = 9.1,51
        p2 = 35.4,100
        c = '#FFFF00' # 51:100: yellow
    elif conc <= 55.4:
        p1 = 35.5,101
        p2 = 55.4,150
        c = '#ff8c00' # 101-150: darkorange, orange #ffa500
    elif conc <= 125.4:
        p1 = 55.5,151
        p2 = 125.4,200
        c = '#FF0000' # 151-200: red
    elif conc <= 225.4:
        p1 = 125.5,201
        p2 = 225.4,300
        c = '#800080' # 201-300: purple
    elif conc <= 325.4:
        p1 = 225.5,301
        p2 = 325.4,500
        c = '#800000' # >300: maroon, darkmagenta used for map coloring #8b008b
    else:
        # cap AQI at 501
        return 501, '#800000'
    
    m = (p2[1]-p1[1])/(p2[0]-p1[0])
    b = p1[1]-m*p1[0]
    return round(conc*m+b), c