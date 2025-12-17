import streamlit as st
import pandas as pd

st.set_page_config(page_title="Macro Dashboard", layout="wide")
cutoff_date = pd.to_datetime('2009-01-01')

monthly = pd.read_excel("Monthly Economic Data.xlsx")

most_recent_dt = monthly['date'].iloc[-1]

Unemployment = pd.read_excel("Unemployment Claims.xlsx")

monthly['date'] = pd.to_datetime(monthly['date'])
monthly = monthly.loc[monthly['date'] >= cutoff_date]

Unemployment['date'] = pd.to_datetime(Unemployment['date'])
Unemployment = Unemployment.loc[Unemployment['date'] >= cutoff_date]

inflation = monthly[['date', 'CPI', 'PPI', 'CPI Inflation Rate', 'PPI Inflation Rate']]
imports = monthly[['date', 'Imports', 'Exports', 'Imports % Change', 'Exports % Change']]


# ================== HEADER ==================
st.title("Economy Tracker: 2009 - Present")

st.markdown("---")

# ================== INFLATION ==================
st.subheader("Inflation")

most_recent = inflation['CPI Inflation Rate'].iloc[-1]
most_recent = most_recent * 100
most_recent = f"{most_recent:.2f}"
most_recent = str(most_recent) + "%"

most_recent2 = inflation['PPI Inflation Rate'].iloc[-1]
most_recent2 = most_recent2 * 100
most_recent2 = f"{most_recent2:.2f}"
most_recent2 = str(most_recent2) + "%"

inflation_left, inflation_right = st.columns([2, 1])

with inflation_left:
    st.line_chart(inflation, x='date', y=['CPI Inflation Rate', 'PPI Inflation Rate'], x_label='Date', y_label='Inflation Rate')

with inflation_right:
    # Top row: CPI & PPI metrics
    m1, m2 = st.columns(2)

    with m1:
        st.metric(label="CPI Inflation Rate", value=most_recent, border=True)

    with m2:
        st.metric(label="PPI Inflation Rate", value=most_recent2, border=True)

    st.write("")  # small vertical spacer

    # Description box
    st.write("""
    Inflation is the change in prices over time. The inflation rate is calculated by comparing the prices of items now against the same time from the prior year.
    For example, the Inflation rate for October 2025 is calculated by seeing the change in prices from October 24th. to October 25th. Prices are calculated via the CPI or PPI metric.

    The Consumer Price Index (CPI) and the Producer Price Index (PPI) are both key indicators of inflation, but they measure price changes from different perspectives in the economy. 
    The CPI focuses on the prices consumers pay, while the PPI tracks the prices producers receive for their goods and services at earlier stages of production.
    """)

st.markdown("---")

st.subheader("Job Creation")


# ================== UNEMPLOYMENT ==================
st.subheader("Unemployment")

jc = monthly[['date', 'Total Employment', 'Jobs Added']]

jc_row_left, jc_row_right = st.columns([2, 1], gap="large")

with jc_row_left:
    st.line_chart(jc, x='date', y='Jobs Added', x_label='Date', y_label='Jobs Added')

with jc_row_right:
    jobs_added = jc['Jobs Added'].iloc[-1]
    st.metric(label="Jobs Added: " + most_recent_dt, value=jobs_added, border=True)


unemployment = monthly[['date', 'Unemployment Rate', 'U6 Unemployment Rate']]
unemployment_by_race = monthly[
    ['date', 'White Unemployment Rate', 'Black Unemployment Rate', 'Hispanic Unemployment Rate',
     'Asian Unemployment Rate']]

# Row 1: Unemployment & U6 line graphs / metrics + explanation
u_row1_left, u_row1_right = st.columns([2, 1], gap="large")

with u_row1_left:
    st.line_chart(unemployment, x='date', y=['Unemployment Rate', 'U6 Unemployment Rate'], x_label='Date', y_label='Unemployment Rate')

white_un = str(unemployment_by_race['White Unemployment Rate'].iloc[-1]) + "%"
black_un = str(unemployment_by_race['Black Unemployment Rate'].iloc[-1]) + "%"
hispanic_un = str(unemployment_by_race['Hispanic Unemployment Rate'].iloc[-1]) + "%"
asian_un = str(unemployment_by_race['Asian Unemployment Rate'].iloc[-1]) + "%"

un_rate = str(unemployment['Unemployment Rate'].iloc[-1]) + "%"
u6_rate = str(unemployment['U6 Unemployment Rate'].iloc[-1]) + "%"

with u_row1_right:
    ur_m1, ur_m2 = st.columns(2)

    with ur_m1:
        st.metric(label="Unemployment Rate", value=un_rate, border=True)

    with ur_m2:
        st.metric(label="U6 Unemployment Rate", value=u6_rate, border=True)

    st.write("""
    The Unemployment Rate (U-3) is the narrow, official number you hear most often, and it only counts people who are jobless but actively searching for work right now. It provides a good measure of the current tightness in the labor market. 
    
    In contrast, the U6 Rate is the broadest and most comprehensive measure, capturing the full extent of job market slack. It includes everyone counted in the U-3, plus two crucial groups: people who are underemployed (working part-time but desperately want a full-time job), and marginally attached/discouraged workers (people who want a job but have given up searching).
    """)

# Row 2: Unemployment by race / gender
u_row2_left, u_row2_right = st.columns(2, gap="large")

with u_row2_left:
    st.line_chart(unemployment_by_race, x='date',
                 y=['White Unemployment Rate', 'Black Unemployment Rate', 'Hispanic Unemployment Rate',
                    'Asian Unemployment Rate'], x_label='Date', y_label='Unemployment Rate')



with u_row2_right:
    um1, um2 = st.columns(2)
    with um1:
        st.metric(label="White Unemployment", value=white_un, border=True)
    with um2:
        st.metric(label="Black Unemployment", value=black_un, border=True)

    um3, um4 = st.columns(2)
    with um3:
        st.metric(label="Hispanic Unemployment", value=hispanic_un, border=True)
    with um4:
        st.metric(label="Asian Unemployment", value=asian_un, border=True)
    st.write("")

# Row 3: Weekly & continued claims

st.subheader("Weekly & Continued Unemployment Claims")

unemployment_claims = pd.read_excel("Unemployment Claims.xlsx")
unemployment_claims['date'] = pd.to_datetime(unemployment_claims['date'])
unemployment_claims = unemployment_claims.loc[unemployment_claims['date'] >= cutoff_date]
unemployment_claims['Total Claims'] = unemployment_claims['Initial Claims'] + unemployment_claims['Continued Claims']

u_row3_left, u_row3_right = st.columns(2, gap="large")

with u_row3_left:
    st.line_chart(unemployment_claims, x='date',
                  y=['Initial Claims', 'Continued Claims'], x_label='Date', y_label='Initial Claims')

with u_row3_right:

    i_claims = unemployment_claims['Initial Claims'].iloc[-1]
    c_claims = unemployment_claims['Continued Claims'].iloc[-1]
    t_claims = unemployment_claims['Total Claims'].iloc[-1]

    u_claim_left, u_claim_center, u_claim_right = st.columns(3, gap="large")

    with u_claim_left:
        st.metric(label="Initial Claims", value=i_claims, border=True)

    with u_claim_center:
        st.metric(label="Continued Claims", value=c_claims, border=True)

    with u_claim_right:
        st.metric(label="Total Claims", value=t_claims, border=True)

    st.write("""
    Initial Claims are filed by individuals for the first time after losing their job, acting as a powerful leading indicator of the job market. A sudden jump in initial claims signals that layoffs are increasing and job market conditions are rapidly worsening. 
    
    Continued Claims (also called Insured Unemployment) are filed by people who have already submitted their initial claim and are filing for ongoing benefits for a subsequent week. This is a measure of the total number of people who remain unemployed and are still receiving aid. This indicator reflects the difficulty of finding a new job; if initial claims are low but continued claims are rising, it means people are losing their jobs at a slow rate but are taking longer to find new work.
    """)

st.markdown("---")

# ================== LABOR FORCE PARTICIPATION ==================
st.subheader("Labor Force Participation Rate")

# You can mirror the same pattern as above with boxes/columns
#lfp_left, lfp_right = st.columns([2, 1], gap="large")

#with lfp_left:


#with lfp_right:
