import streamlit as st
import pandas as pd

# Data

monthly = pd.read_excel("Monthly Economic Data.xlsx")

inflation = monthly[['date', 'CPI', 'PPI', 'CPI Inflation Rate', 'PPI Inflation Rate']]
imports = monthly[['date', 'Imports', 'Exports', 'Imports % Change', 'Exports % Change']]

Unemployment = pd.read_excel("Unemployment Claims.xlsx")

# Page Configuration
st.set_page_config(layout="wide")

st.title("Trump Economy Tracker")

col1, col2 = st.columns(2)

with col1:
    most_recent = inflation['CPI Inflation Rate'].iloc[-1]
    most_recent = most_recent * 100
    most_recent = f"{most_recent:.2f}"
    most_recent = str(most_recent) + "%"

    most_recent2 = inflation['PPI Inflation Rate'].iloc[-1]
    most_recent2 = most_recent2 * 100
    most_recent2 = f"{most_recent2:.2f}"
    most_recent2 = str(most_recent2) + "%"

    st.header("Inflation\n", divider="gray")
    st.write("""
    Inflation is the change in prices over time. The inflation rate is calculated by comparing the prices of items now against the same time from the prior year.
    For example, the Inflation rate for October 2025 is calculated by seeing the change in prices from October 24th. to October 25th. Prices are calculated via the CPI or PPI metric.

    The Consumer Price Index (CPI) and the Producer Price Index (PPI) are both key indicators of inflation, but they measure price changes from different perspectives in the economy. 
    The CPI focuses on the prices consumers pay, while the PPI tracks the prices producers receive for their goods and services at earlier stages of production.
    """)

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)

    with metric_col_1:
        st.metric(label="CPI Inflation Rate (as of " + inflation['date'].iloc[-1] + ")", value=most_recent, border=True)

    with metric_col_2:
        st.metric(label="PPI Inflation Rate (as of " + inflation['date'].iloc[-1] + ")", value=most_recent2,
                  border=True)

    st.line_chart(inflation, x='date', y=['CPI Inflation Rate', 'PPI Inflation Rate'], x_label='Date',
                  y_label='Inflation Rate')

with col2:
    most_recent = imports['Imports % Change'].iloc[-2]
    most_recent = most_recent * 100
    most_recent = f"{most_recent:.2f}"
    most_recent = str(most_recent) + "%"

    most_recent2 = imports['Exports % Change'].iloc[-2]
    most_recent2 = most_recent2 * 100
    most_recent2 = f"{most_recent2:.2f}"
    most_recent2 = str(most_recent2) + "%"

    st.header("Imports & Exports\n", divider="gray")

    st.write("""
   The Import and Export Price Indexes indicators track the price changes of goods and services traded between the United States and other countries, excluding military items. 
   The Import Price Index measures the average change in the prices paid by U.S. residents for foreign products. Conversely, the Export Price Index tracks the average change in prices received by U.S. producers for products sold abroad. 

   These indexes are typically presented as a year over year percent change. A positive Y/Y change indicates that prices for those traded goods are higher. A negative Y/Y change shows that prices have decreased. By monitoring this Y/Y metric, analysts can assess the recent momentum and underlying trend of inflation or deflation stemming from international commerce.
   """)

    metric_col_4, metric_col_5, metric_col_6 = st.columns(3)

    with metric_col_4:
        st.metric(label="Import % Change (as of " + imports['date'].iloc[-2] + ")", value=most_recent, border=True)

    with metric_col_5:
        st.metric(label="Export % Change (as of " + imports['date'].iloc[-2] + ")", value=most_recent2,
                  border=True)

    st.line_chart(imports, x='date', y=['Imports % Change', 'Exports % Change'], x_label='Date', y_label='% Change')

col3, col4 = st.columns(2)

unemployment = monthly[['date', 'Unemployment Rate', 'U6 Unemployment Rate']]
unemployment_by_race = monthly[
    ['date', 'White Unemployment Rate', 'Black Unemployment Rate', 'Hispanic Unemployment Rate',
     'Asian Unemployment Rate']]

with col3:
    st.header("Total Unemployment Rate\n", divider="gray")
    st.line_chart(unemployment, x='date', y=['Unemployment Rate', 'U6 Unemployment Rate'], x_label='Date',
                  y_label='Unemployment Rate')

with col4:
    st.header("Unemployment Rate by Race\n", divider="gray")
    st.line_chart(unemployment_by_race, x='date',
                  y=['White Unemployment Rate', 'Black Unemployment Rate', 'Hispanic Unemployment Rate',
                     'Asian Unemployment Rate'], x_label='Date', y_label='Unemployment Rate')
