import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static

# Load dataframes
df_budget = pd.read_csv('./data/budget.csv')

# The main Climate Analysis app
def app():

    st.title("Climate Analysis")

    analysis_options = [
        "Select an analysis...",
        "Budget Analysis",
        "Adaptation Strategies",
        "Climate Trends",
        "Climate Classification",
        "Climate Projections",
        "Climate Vulnerabilities",
        "Dominant species"
        # ... add other analysis options here
    ]
    
    choice = st.selectbox("Choose an analysis:", analysis_options)

    df = None  # Initialize dataframe to None

    if choice == "Budget Analysis":
        df = display_budget_analysis(df_budget)
    elif choice == "Adaptation Strategies":
        df = display_adaptation_strategies()
    elif choice == "Climate Trends":
        df = display_climate_trends()
    elif choice == "Climate Classification":
        df = display_climate_classification()
    elif choice == "Climate Projections":
        df = display_climate_projections()
    elif choice == "Climate Vulnerabilities":
        df = display_vulnerabilities()
    elif choice == "Dominant species":
        df = display_dominant_species_analysis()
        
        
    # ... add other choices as needed

    # Visualization
    st.subheader("Visualizations")

    chart_options = [
        "Select a chart type...",
        "Line Chart",
        "Stacked Line Chart",
        "Bar Chart",
        "Stacked Bar Chart",
        "Pie Chart",
        # ... add other chart types as needed
    ]
    chart_choice = st.selectbox("Choose a Chart Type:", chart_options)

    if df is not None:  # Ensure we have a dataframe
        if chart_choice == "Line Chart":
            st.line_chart(df)
        elif chart_choice == "Stacked Line Chart":
            st.area_chart(df)
        elif chart_choice == "Bar Chart":
            st.bar_chart(df)  # If the dataframe doesn't have an index you want, you might need to set it
        elif chart_choice == "Stacked Bar Chart":
            # Stacked bar charts are a bit more complex and may need data reshaping
            st.warning("Stacked Bar Chart is not implemented for this dataset.")
        elif chart_choice == "Pie Chart":
            # For pie charts, we should consider only one numeric column
            st.warning("Pie Chart is not implemented for this dataset.")
        # ... add other charting options as needed
    
    # Default view
    if choice == analysis_options[0]:
        st.write("Please select an analysis from the dropdown above.")

# Budget Analysis Functions
def get_highest_budgets(df_budget, n=30):
    return df_budget.nlargest(n, 'Estimated_Budget')[['Country', 'Estimated_Budget']]

def get_lowest_budgets(df_budget, n=30):
    return df_budget.nsmallest(n, 'Estimated_Budget')[['Country', 'Estimated_Budget']]

def get_vulnerabilities_for_top_budgets(df_budget, n=30):
    top_countries = df_budget.nlargest(n, 'Estimated_Budget')['Country'].tolist()
    return df_budget[df_budget['Country'].isin(top_countries)][['Country', 'Climate_Vulnerabilities', 'Estimated_Budget']]

def display_budget_analysis(df_budget):
    st.subheader("Budget Analysis")
    
    st.write("Countries with the Highest Estimated Budgets for Adaptation:")
    highest_budgets = get_highest_budgets(df_budget)
    st.table(highest_budgets)
    
    st.write("Country with the Lowest Estimated Budget for Adaptation:")
    lowest_budgets = get_lowest_budgets(df_budget)
    st.table(lowest_budgets)
    
    st.write("Main Climate Vulnerabilities for Countries with Top 10 Highest Budgets:")
    top_vulnerabilities = get_vulnerabilities_for_top_budgets(df_budget)
    st.table(top_vulnerabilities)

# Adaptation Strategies Function (Placeholder for now)
def display_adaptation_strategies():
    st.subheader("Adaptation Strategies")
    st.write("This section will display the analysis for Adaptation Strategies.")
    # Assuming the data is loaded from a CSV for now
    adaptation_data = pd.read_csv('./data/adaptation.csv')

    # 1. Which plant species are the most commonly recommended across countries?
    st.write("Most Commonly Recommended Plant Species:")
    plant_species_counts = adaptation_data['OrnamentalPlantSpecies'].value_counts().nlargest(5)
    st.write(plant_species_counts)

    # 2. Aggregate counts and list the countries for each species
    species_countries = adaptation_data.groupby('OrnamentalPlantSpecies')['Country'].apply(list).reset_index()
    st.write("Countries for Each Plant Species:")
    st.write(species_countries)

    # 3. List the common adaptation strategies for countries with specific vulnerabilities
    st.write("Adaptation Strategies for Countries with 'Water scarcity' Vulnerability:")
    water_scarcity_data = adaptation_data[adaptation_data['ClimateVulnerabilities'].str.contains('Water scarcity', case=False, na=False)]
    water_scarcity_strategies = water_scarcity_data['strategies'].value_counts().nlargest(30)
    st.write(water_scarcity_strategies)

    # 4. List countries with specific vulnerabilities and their adaptation strategies
    st.write("Countries with 'Water scarcity' Vulnerability and Their Adaptation Strategies:")
    water_scarcity_country_strategies = water_scarcity_data.groupby(['Country', 'strategies']).size().reset_index(name='Count')
    water_scarcity_country_strategies = water_scarcity_country_strategies.sort_values(by='Count', ascending=False)
    st.write(water_scarcity_country_strategies)

# Climate Trends Function (Placeholder for now)
def display_climate_trends():
    st.subheader("Climate Trends")
    st.write("This section will display the analysis for Climate Trends.")

    # Assuming the data is loaded from a CSV for now
    climate_data = pd.read_csv('./data/climate.csv')

    # 1. How many countries are experiencing a warming trend vs. a cooling trend?
    st.write("Number of countries experiencing a warming trend vs. a cooling trend:")
    
    # a. Warming trend
    warming_trend = climate_data[climate_data['Climate Trend'].str.contains('Warming', case=False, na=False)]
    st.write(f"Warming Trend: {len(warming_trend)} countries")

    # b. Cooling trend
    cooling_trend = climate_data[climate_data['Climate Trend'].str.contains('Cooling', case=False, na=False)]
    st.write(f"Cooling Trend: {len(cooling_trend)} countries")

    # 2. List countries experiencing a warming trend:
    st.write("Countries experiencing a warming trend:")
    st.write(warming_trend[['Country', 'Climate Trend']])
    
    # 3. List countries experiencing a cooling trend:
    st.write("Countries experiencing a cooling trend:")
    st.write(cooling_trend[['Country', 'Climate Trend']])

    # 4. Which countries have the most severe climate states currently?
    st.write("Countries with the most severe climate states (based on rainfall):")
    rainfall_data = climate_data[climate_data['Current Climate State'].str.contains('rainfall', case=False, na=False)]
    st.write(rainfall_data[['Country', 'Current Climate State']])

# ... add other analysis functions as needed

# Climate Classification Function
def display_climate_classification():
    st.subheader("Climate Classification")
    st.write("This section will display the analysis for Climate classification.")
    
    # Read the data
    df_classification = pd.read_csv('./data/climateclassification.csv')

    # 1. Which countries fall into specific winter hardiness zones?
    st.write("Countries in specific winter hardiness zones:")

    # Create a DataFrame for displaying the grouped results
    zone_data = []
    for zone, group in df_classification.groupby("Winter Hardiness Zone"):
        countries = ", ".join(group["Country"])
        zone_data.append({"Winter Hardiness Zone": zone, "Countries": countries})

    st.table(pd.DataFrame(zone_data))

    # 2. What are the most common plant species recommended for each climate classification?
    st.write("Most common plant species recommended for each climate classification:")

    # Create a DataFrame for displaying the grouped results
    classification_data = []
    for classification, group in df_classification.groupby("Classification"):
        common_species = group["Suitable Plant Species"].mode()[0]
        classification_data.append({"Classification": classification, "Recommended Plant Species": common_species})

    st.table(pd.DataFrame(classification_data))

#Climate Projections:
def display_climate_projections():
    st.subheader("Climate Projections")
    st.write("This section will display the analysis for Climate Projections.")
    
    # Read the data
    df_projections = pd.read_csv('./data/climateprojections.csv')

    # a. Which countries are projected to experience the most drastic changes in the next 30 years?
    drastic_changes = df_projections[df_projections["30-Year Projection"].str.contains("warming", case=False, na=False)]
    st.write("Countries projected to experience the most drastic changes in the next 30 years:")
    st.table(drastic_changes[["Country", "30-Year Projection"]])

    # b. Are there any trends in the 5-year, 10-year, and 30-year projections?
    st.write("Trends in 5-year projection:")
    st.table(df_projections["5-Year Projection"].value_counts().reset_index().rename(columns={"index": "5-Year Projection", "5-Year Projection": "Country Count"}))
    
    st.write("Trends in 10-year projection:")
    st.table(df_projections["10-Year Projection"].value_counts().reset_index().rename(columns={"index": "10-Year Projection", "10-Year Projection": "Country Count"}))
    
    st.write("Trends in 30-year projection:")
    st.table(df_projections["30-Year Projection"].value_counts().reset_index().rename(columns={"index": "30-Year Projection", "30-Year Projection": "Country Count"}))


#Vulnerabilities:
def display_vulnerabilities():
    st.subheader("Vulnerabilities Analysis")
    st.write("This section will display analysis related to vulnerabilities.")
    
    # Read the data
    df_vulnerabilities = pd.read_csv('./data/vulnerabilities.csv')

    # a. Which countries are projected to have the most significant vulnerabilities in the future?
    increased_vulnerabilities = df_vulnerabilities[df_vulnerabilities["futurevulnerabilities"].str.contains("increased", case=False, na=False)]
    st.write("Countries projected to have the most significant vulnerabilities in the future:")
    st.table(increased_vulnerabilities[["Country", "futurevulnerabilities"]])

    # b. What are the recommended plant species for countries with high risk future vulnerabilities?
    high_risk_countries = df_vulnerabilities[df_vulnerabilities["futurevulnerabilities"].str.contains("risk", case=False, na=False)]
    st.write("Recommended plant species for countries with high risk future vulnerabilities:")
    st.table(high_risk_countries[["Country", "recommendedplantspecies"]])


# Dominant Species Analysis function
def display_dominant_species_analysis():
    st.subheader("Dominant Species Analysis")
    st.write("This section will display dominant species in each country and the spaces they occupy.")

    # Read the shapefiles
    dominantspecies_gdf = gpd.read_file("./data/Geodatabasefiles/dominantspecies.shp")
    world_gdf = gpd.read_file("./data/Geodatabasefiles/world.shp")

    # Define a bounding box for Europe (minx, miny, maxx, maxy)
    europe_bbox = (-31.266, 27.6363, 39.8693, 81.5)

    # Clip the world_gdf to this bounding box
    world_gdf_clipped = world_gdf.cx[europe_bbox[0]:europe_bbox[2], europe_bbox[1]:europe_bbox[3]]

    # Buffer the geometries
    dominantspecies_gdf['buffered_geom'] = dominantspecies_gdf.geometry.buffer(0.0001)

    # Perform spatial join
    joined_gdf = gpd.sjoin(world_gdf_clipped, dominantspecies_gdf, how="inner", op='intersects')

    # Calculate intersection areas (assuming the CRS is in meters for area calculation)
    joined_gdf["IntersectionAreaInHectares"] = joined_gdf.apply(lambda row: row['geometry'].intersection(row['buffered_geom']).area / 10000, axis=1)

    # Filter by Country (for demonstration purposes)
    filtered_gdf = joined_gdf[joined_gdf["Country"] == "Latvia"]

    # Display the results
    columns_to_display = ["Country", "gridcode", "species", "IntersectionAreaInHectares"]
    st.table(filtered_gdf[columns_to_display])
    
    # Display the map (optional)
    st.write("Spatial distribution of dominant species in Latvia:")
    st.map(filtered_gdf)

