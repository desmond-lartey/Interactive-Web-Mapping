import streamlit as st
import pandas as pd
import altair as alt

# Assuming data has been preprocessed and saved as 'population_dynamics_long.csv'
# and 'population_estimates_long.csv'
dynamics_df = pd.read_csv('./data/population_dynamics_long_refined.csv')
estimates_df = pd.read_csv('./data/population_estimates_long_refined.csv')


def app():
    st.title("Population Dynamics & Estimates")

    # Combining both datasets for simplicity
    combined_df = pd.concat([dynamics_df, estimates_df])

    # Dropdown for country selection
    country = st.selectbox('Select Country', combined_df['Country Name'].unique())

    # Dropdown for metric selection
    metric = st.selectbox('Select Metric', combined_df['Series Name'].unique())

    # Dropdown for chart type selection
    chart_type = st.selectbox('Select Chart Type', ['Line', 'Bar', 'Area'])

    # Filter data based on selections
    filtered_data = combined_df[(combined_df['Country Name'] == country) & (combined_df['Series Name'] == metric)]

    # Base chart
    base = alt.Chart(filtered_data).encode(
        x='Year:O',
        y='Value:Q',
        tooltip=['Year', 'Value']
    )

    # Plotting the data based on chart type
    if chart_type == 'Line':
        chart = base.mark_line() + base.mark_circle()
    elif chart_type == 'Bar':
        chart = base.mark_bar()
    elif chart_type == 'Area':
        chart = base.mark_area()

    st.altair_chart(chart.properties(width=600, height=400), use_container_width=True)
