import folium
from streamlit_folium import folium_static
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd  # <-- This was missing



def app():
    st.title("World Population and Capitals")

    # Using geopandas to fetch the datasets
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    capitals = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add the countries layer with population as popup
    folium.GeoJson(world, name="Countries", popup=folium.GeoJsonTooltip(fields=["name", "pop_est"])).add_to(m)

    # Add the capitals layer
    folium.GeoJson(capitals, name="Capitals", popup=folium.GeoJsonTooltip(fields=["name"])).add_to(m)

    folium.LayerControl().add_to(m)

    # Display the map in Streamlit
    folium_static(m)
