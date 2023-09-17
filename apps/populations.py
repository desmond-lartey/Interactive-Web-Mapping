import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd  # <-- This was missing

def app():

    st.title("World Population and Capitals")

    # Using geopandas to fetch the datasets
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    capitals = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    # Plotting the map
    m = leafmap.Map(center=[20, 0], zoom=2)

    # Add the countries layer with population as popup
    m.add_gdf(world, layer_name="Countries", popup=["name", "pop_est"])

    # Add the capitals layer
    m.add_gdf(capitals, layer_name="Capitals", popup="name", marker_type="marker")

    m.to_streamlit(height=700)
