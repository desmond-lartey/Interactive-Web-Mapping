import os
import streamlit as st
from streamlit_option_menu import option_menu
from apps import home, upload, vector, populations, worldbank, climate,carbon2, heatmap, climate  #urbangreen #import your app modules here


st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com


apps = [
    {"func": home.app, "title": "Home", "icon": "house"},
    {"func": heatmap.app, "title": "Heatmap", "icon": "map"},
    #{"func": upload.app, "title": "Upload", "icon": "cloud-upload"},
    #{"func": vector.app, "title": "Vector", "icon": "bounding-box"},
    #{"func": populations.app, "title": "Population & Capitals", "icon": "globe"},
    {"func": worldbank.app, "title": "Population Stats", "icon": "globe"},
    #{"func": urbangreen.app, "title": "Urbangreen Analysis", "icon": "globe"},
    {"func": climate.app, "title": "Climate Analysis", "icon": "globe"},
    {"func": carbon2.app, "title": "Carbon Footprint", "icon": "graph-down"}
]


titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

params = st.experimental_get_query_params()

if "page" in params:
    default_index = int(titles_lower.index(params["page"][0].lower()))
else:
    default_index = 0

with st.sidebar:
    selected = option_menu(
        "Main Menu",
        options=titles,
        icons=icons,
        menu_icon="cast",
        default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This web app is maintained by [Desmond Lartey](https://github.com/desmond-lartey). Contact for any mulfunction of the App:
            [GitHub](https://github.com/desmond-lartey) | [Twitter](https://twitter.com/Desmondlartey17) | [YouTube](https://www.youtube.com/watch?v=BZMSFcrSbwU) | [LinkedIn](https://www.linkedin.com/in/desmond-lartey/).
        
        -

        
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break

