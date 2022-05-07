import pandas as pd
import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt

eda = pd.read_csv('airlines_with_locations.csv', index_col='Unnamed: 0')

a = eda[eda['airline'] == 'American Airlines']
d = eda[eda['airline'] == 'Delta Air Lines']
u = eda[eda['airline'] == 'United Airlines']

a = a.dropna()
d = d.dropna()
u = u.dropna()

m = folium.Map()

UAFG = folium.FeatureGroup(name='United Airlines')
AAFG = folium.FeatureGroup(name='American Airlines')
DAFG = folium.FeatureGroup(name='Delta Airlines')

a.apply(lambda row:folium.CircleMarker(location=[row["dst_lat"], 
                                                  row["dst_lon"]], color='black', radius=2).add_to(m),
         axis=1)
a.apply(lambda row:folium.CircleMarker(location=[row["src_lat"], 
                                                  row["src_lon"]], color='black', radius=2).add_to(m), axis=1)
          
a.apply(lambda row: folium.PolyLine([[row['src_lat'], row['src_lon']], [row['dst_lat'], row['dst_lon']]], weight=15*row['pct'], color='red').add_to(AAFG),
         axis=1)

d.apply(lambda row:folium.CircleMarker(location=[row["dst_lat"], 
                                                  row["dst_lon"]], color='black', radius=2).add_to(m),
         axis=1)
d.apply(lambda row:folium.CircleMarker(location=[row["src_lat"], 
                                                  row["src_lon"]], color='black', radius=2).add_to(m), axis=1)
          
d.apply(lambda row: folium.PolyLine([[row['src_lat'], row['src_lon']], [row['dst_lat'], row['dst_lon']]], weight=15*row['pct'], color='green').add_to(DAFG),
         axis=1)

u.apply(lambda row:folium.CircleMarker(location=[row["dst_lat"], 
                                                  row["dst_lon"]], color='black', radius=2).add_to(m),
         axis=1)
u.apply(lambda row:folium.CircleMarker(location=[row["src_lat"], 
                                                  row["src_lon"]], color='black', radius=2).add_to(m), axis=1)
          
u.apply(lambda row: folium.PolyLine([[row['src_lat'], row['src_lon']], [row['dst_lat'], row['dst_lon']]], weight=15*row['pct'], color='blue').add_to(UAFG),
         axis=1)

UAFG.add_to(m)
AAFG.add_to(m)
DAFG.add_to(m)

folium.LayerControl().add_to(m)


st.title("Density of Flights by Airlines")

folium_static(m)

option = st.selectbox('Select an Airline to View', ('American Airlines', 'Delta Airlines', 'United Airlines'))

if option == 'American Airlines':
    selected = a.groupby('src_port')['dst_port'].count()
if option == 'Delta Airlines':
    selected = d.groupby('src_port')['dst_port'].count()
if option == 'United Airlines':
    selected = u.groupby('src_port')['dst_port'].count()

sizes = selected.values.tolist()
labels = selected.index.tolist()

  
plt.figure(figsize=(10,10))    
    
# explosion
explode = len(sizes)*[0.05]
  
# Pie Chart
plt.pie(sizes, labels=labels,
        autopct='%1.1f%%', pctdistance=0.85,
        explode=explode)
  
# draw circle
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
  
# Adding Circle in Pie chart
fig.gca().add_artist(centre_circle)
  
# Adding Title of chart
plt.title('Breakdown of Departure Airports for {}'.format(option))
  
# Add Legends
plt.legend(labels, loc="upper right", title="Departure Airports")

st.pyplot(plt)