#pip install folium

import pandas as pd
data = pd.read_csv("4.1 Volcanoes.txt.txt")
data[data["ELEV"] < 1000]

import folium
import pandas as pd

data = pd.read_csv("4.1 Volcanoes.txt.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
elev = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1500:
        return 'green'
    elif 1500<= elevation <3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[38.58, -99.0], zoom_start = 6, tiles = "Stamen Terrain")

fg_volcano = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(lat, lon, elev):
    fg_volcano.add_child(folium.CircleMarker(location=[lt, ln], radius = 8, popup = str(el) + "m", fill_color=color_producer(el), color = "grey", fill_opacity = 0.7))

fg_pop = folium.FeatureGroup(name="Population")    
    
fg_pop.add_child(folium.GeoJson(data=open("13.1 world.json.json", 'r', encoding='UTF-8-sig').read(),
                           style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
                                                     else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                    else 'red'}))
    
map.add_child(fg_volcano)
map.add_child(fg_pop)
map.add_child(folium.LayerControl())

map.save("Map1.html")