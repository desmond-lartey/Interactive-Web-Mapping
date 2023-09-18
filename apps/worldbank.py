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

    # Filter data based on selections
    filtered_data = combined_df[(combined_df['Country Name'] == country) & (combined_df['Series Name'] == metric)]

    # Plotting the data
    chart = alt.Chart(filtered_data).mark_line().encode(
        x='Year:O',
        y='Value:Q',
        tooltip=['Year', 'Value']
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
