import folium
import pandas as pd

data = pd.read_csv("Volcanoes.txt")
lat= list(data["LAT"])
lon= list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'



map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")
#feature group volcanoes

for lt,ln,el,name in zip(lat,lon,elev,name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6,popup=folium.Popup(iframe), fill_color=color_producer(el), color='grey',fill=True, fill_opacity=0.7))
    
fgp = folium.FeatureGroup(name="Population")
# feature group population

# popup=folium.Popup(str(el)+"m",parse_html=True)))
# marker allows to show imformation
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())


map.save("map_html_popup_simple.html")
