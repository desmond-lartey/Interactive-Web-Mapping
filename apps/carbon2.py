import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os

# Function for Climatiq API Integration
def calculate_transportation_emissions(api_key, start_location, end_location, vehicle_type, vehicle_weight):
    url = "https://beta4.api.climatiq.io/estimate"
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        "emission_factor": {
            "activity_id": "passenger_vehicle-vehicle_type_automobiles-fuel_source_na-engine_size_na-vehicle_age_na-vehicle_weight_na",
        },
        "parameters": {
            "distance": vehicle_weight,
            "distance_unit": "km"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to plot emissions data
def plot_emissions(data, chart_type="pie"):
    if chart_type == "bar":
        fig = px.bar(data, x="Category", y="Emissions", title="Your Carbon Emissions Breakdown")
    elif chart_type == "line":
        fig = px.line(data, x="Category", y="Emissions", title="Your Carbon Emissions Breakdown")
    else:
        fig = px.pie(data, names="Category", values="Emissions", title="Your Carbon Emissions Breakdown")
    return fig

def app():
    st.title("Global Carbon Calculator App")

    # Original Carbon Footprint Calculation
    st.header("Calculate Your Carbon Footprint")

    country = st.selectbox("Select Your Country", ["India"])
    col1, col2 = st.columns(2)

    with col1:
        distance = st.slider("🚗 Daily commute distance (in km)", 0.0, 100.0, key="distance_input")
        electricity = st.slider("💡 Monthly electricity consumption (in kWh)", 0.0, 1000.0, key="electricity_input")

    with col2:
        waste = st.slider("🗑️ Weekly waste generated (in kg)", 0.0, 100.0, key="waste_input")
        meals = st.number_input("🍽️ Daily number of meals", 0, key="meals_input")

    normalized_inputs = {
        "distance": distance * 365,
        "electricity": electricity * 12,
        "meals": meals * 365,
        "waste": waste * 52
    }

    EMISSION_FACTORS = {
        "India": {
            "Transportation": 0.14,
            "Electricity": 0.82,
            "Diet": 1.25,
            "Waste": 0.1
        }
    }

    if st.button("Calculate Personal CO2 Emissions"):
        factors = EMISSION_FACTORS[country]
        transportation_emissions = factors["Transportation"] * normalized_inputs["distance"]
        electricity_emissions = factors["Electricity"] * normalized_inputs["electricity"]
        diet_emissions = factors["Diet"] * normalized_inputs["meals"]
        waste_emissions = factors["Waste"] * normalized_inputs["waste"]

        total_emissions = round(sum([transportation_emissions, electricity_emissions, diet_emissions, waste_emissions]) / 1000, 2)
        st.subheader("Your Total Carbon Footprint")
        st.metric(label="Total Emissions", value=f"{total_emissions} tonnes CO2 per year")

        # Data for plot
        emissions_data = pd.DataFrame({
            "Category": ["Transportation", "Electricity", "Diet", "Waste"],
            "Emissions": [transportation_emissions, electricity_emissions, diet_emissions, waste_emissions]
        })
        chart_type = st.selectbox("Select Chart Type", ["pie", "bar", "line"], index=0)  # Default is 'pie'
        st.plotly_chart(plot_emissions(emissions_data, chart_type))

    # Climatiq API Integration for Transportation Emissions
    st.header("Calculate Transportation Emissions (Climatiq API)")

    start_location = st.text_input("Start Location (e.g., Hamburg)")
    end_location = st.text_input("End Location (e.g., Berlin)")
    vehicle_type = st.selectbox("Vehicle Type", ["van", "truck", "air", "sea"])
    vehicle_weight = st.number_input("Vehicle Weight (in tonnes)", min_value=0.1, step=0.1)

    API_KEY = os.environ.get("CLIMATIQ_API_KEY")

    if st.button("Calculate Transportation Emissions (API)"):
        emission_data = calculate_transportation_emissions(API_KEY, start_location, end_location, vehicle_type, vehicle_weight)
        
        if emission_data:
            st.write("Total CO2 Emissions for the trip:", emission_data.get('co2e', 0), "kg CO2e")
            st.write("Total distance traveled:", emission_data.get('distance_km', 0), "km")
        else:
            st.write("Unable to calculate emissions. Please check input values.")
