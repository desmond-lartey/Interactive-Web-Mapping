import streamlit as st
import pandas as pd

# Load budget dataframe from 'budget.csv'
df_budget = pd.read_csv('./data/budget.csv')

# Data retrieval functions for Budget Analysis
def get_highest_budgets(df_budget, n=15):
    return df_budget.nlargest(n, 'Estimated_Budget')[['Country', 'Estimated_Budget']]

def get_lowest_budgets(df_budget, n=1):
    return df_budget.nsmallest(n, 'Estimated_Budget')[['Country', 'Estimated_Budget']]

def get_vulnerabilities_for_top_budgets(df_budget, n=5):
    top_countries = df_budget.nlargest(n, 'Estimated_Budget')['Country'].tolist()
    return df_budget[df_budget['Country'].isin(top_countries)][['Country', 'Climate_Vulnerabilities', 'Estimated_Budget']]

# Streamlit function to display Budget Analysis
def display_budget_analysis(df_budget):
    st.title("Budget Analysis")
    
    st.header("Countries with Highest Estimated Budgets for Adaptation")
    highest_budgets = get_highest_budgets(df_budget)
    st.table(highest_budgets)
    
    st.header("Country with Lowest Estimated Budget for Adaptation")
    lowest_budgets = get_lowest_budgets(df_budget)
    st.table(lowest_budgets)
    
    st.header("Main Climate Vulnerabilities for Countries with Top 5 Highest Budgets")
    top_vulnerabilities = get_vulnerabilities_for_top_budgets(df_budget)
    st.table(top_vulnerabilities)

# Main app function
def app():
    display_budget_analysis(df_budget)
