import streamlit as st
import psycopg2
import pandas as pd

def fetch_data_from_db(query):
    # Establish the connection
    conn = psycopg2.connect(
        dbname="urbisgreen",
        user="postgres",
        password="agronl",
        host="localhost",
        port="5432"
    )
    
    # Fetch data
    df = pd.read_sql_query(query, conn)
    
    # Close the connection
    conn.close()
    
    return df

def app():
    query = "SELECT * FROM budget LIMIT 10;"
    df = fetch_data_from_db(query)
    st.write(df)
