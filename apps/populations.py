import folium
from streamlit_folium import folium_static
import streamlit as st
import geopandas as gpd

def app():
    st.title("World Population and Capitals")

    # Using geopandas to fetch the datasets
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    capitals = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

    # Performing a spatial join between the world and capitals datasets
    capitals_with_country_data = gpd.sjoin(capitals, world, how="left", op="within")

    m = folium.Map(location=[20, 0], zoom_start=2)

    # Add the countries layer with population as popup
    folium.GeoJson(world, name="Countries", popup=folium.GeoJsonTooltip(fields=["name", "pop_est"])).add_to(m)

    # Add the capitals layer with country's population as popup
    popup_content = capitals_with_country_data.apply(lambda row: f"{row['name_left']} (Country: {row['name_right']}, Population: {row['pop_est']})", axis=1)
    for idx, row in capitals_with_country_data.iterrows():
        folium.Marker([row['geometry'].y, row['geometry'].x], popup=popup_content.iloc[idx]).add_to(m)

    folium.LayerControl().add_to(m)

    # Display the map in Streamlit
    folium_static(m)
