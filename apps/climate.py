import streamlit as st
import pandas as pd

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
        # ... add other analysis options here
    ]

    choice = st.selectbox("Choose an analysis:", analysis_options)

    if choice == "Budget Analysis":
        display_budget_analysis(df_budget)
    elif choice == "Adaptation Strategies":
        display_adaptation_strategies()
    elif choice == "Climate Trends":
        display_climate_trends()
    # ... add other choices as needed

    # Default view
    if choice == analysis_options[0]:
        st.write("Please select an analysis from the dropdown above.")

# Budget Analysis Functions
def get_highest_budgets(df_budget, n=15):
    return df_budget.nlargest(n, 'Estimated_Budget')[['Country', 'Estimated_Budget']]

def get_lowest_budgets(df_budget, n=1):
    return df_budget.nsmallest(n, 'Estimated_Budget')[['Country', 'Estimated_Budget']]

def get_vulnerabilities_for_top_budgets(df_budget, n=10):
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
    water_scarcity_strategies = water_scarcity_data['strategies'].value_counts().nlargest(5)
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

    # Assuming the data is loaded from a CSV for now
    classification_data = pd.read_csv('./data/climateclassification.csv')

    # 1. Which countries fall into specific winter hardiness zones?
    st.write("Countries in specific winter hardiness zones:")

    grouped_zones = classification_data.groupby("Winter Hardiness Zone")
    for zone, group in grouped_zones:
        st.write(f"Zone: {zone}")
        countries = ", ".join(group["Country"])
        st.write(countries)

    # 2. What are the most common plant species recommended for each climate classification?
    st.write("Most common plant species recommended for each climate classification:")

    grouped_classification = classification_data.groupby("Classification")
    for classification, group in grouped_classification:
        st.write(f"Classification: {classification}")
        common_species = group["Suitable Plant Species"].mode()[0]  # Most common plant species
        st.write(f"Recommended Plant Species: {common_species}")