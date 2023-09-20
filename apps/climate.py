import streamlit as st
import pandas as pd

# The main Climate Analysis app
def app():

    st.title("Climate Analysis")

    analysis_options = [
        "Select an analysis...",
        "Budget Analysis",
        "Adaptation Strategies",
        "Climate Trends",
        # ... add other analysis options here
    ]

    choice = st.selectbox("Choose an analysis:", analysis_options)

    if choice == "Budget Analysis":
        display_budget_analysis()
    elif choice == "Adaptation Strategies":
        display_adaptation_strategies()
    elif choice == "Climate Trends":
        display_climate_trends()
    # ... add other choices as needed

    # Default view
    if choice == analysis_options[0]:
        st.write("Please select an analysis from the dropdown above.")


# Budget Analysis Function
def display_budget_analysis():
    
    # Assuming the data is loaded from a CSV for now
    budget_data = pd.read_csv('./data/budget.csv')

    st.subheader("Budget Analysis")

    # 1.a: Which countries have the highest and lowest estimated budgets for adaptation?
    st.write("Countries with the Highest Estimated Budgets for Adaptation:")
    highest_budget = budget_data.nlargest(15, 'Estimated_Budget')[['Country', 'Estimated_Budget']]
    st.write(highest_budget)

    st.write("Country with the Lowest Estimated Budget for Adaptation:")
    lowest_budget = budget_data.nsmallest(1, 'Estimated_Budget')[['Country', 'Estimated_Budget']]
    st.write(lowest_budget)

    # ... continue with other queries related to budget analysis


# Adaptation Strategies Function (Placeholder for now)
def display_adaptation_strategies():
    st.subheader("Adaptation Strategies")
    st.write("This section will display the analysis for Adaptation Strategies.")


# Climate Trends Function (Placeholder for now)
def display_climate_trends():
    st.subheader("Climate Trends")
    st.write("This section will display the analysis for Climate Trends.")


# ... add other analysis functions as needed
