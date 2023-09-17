import streamlit as st
import leafmap.foliumap as leafmap


def app():

    st.title("vector")

    m = leafmap.Map(center=[0, 0], zoom=2)

    in_geojson = 'https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/cable_geo.geojson'
    m.add_geojson(in_geojson, layer_name="Cable lines")


    m.to_streamlit(height=700)
    m.to_streamlit(height=700)