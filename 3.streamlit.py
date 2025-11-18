# IMPORTS
import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="🚓 Police Checkpost Logs Dashboard", layout="wide")

# NAVBAR
st.markdown("""
<style>
.navbar {
    background-color: #ffffff;
    padding: 12px 24px;
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 100;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}
.nav-link {
    color: #003366 !important;
    margin-right: 25px;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
}
.nav-link:hover { color: #007acc !important; }
section { padding-top: 80px; }
</style>

<div class="navbar">
  <a class="nav-link" href="#overview">🚓 Overview</a>
  <a class="nav-link" href="#insights">📊 Insights</a>
  <a class="nav-link" href="#advanced">💡 Advanced Insights</a>
  <a class="nav-link" href="#search">🔍 Search Explorer</a>
  <a class="nav-link" href="#predict">🤖 Predict Outcome</a>
  <a class="nav-link" href="#about">🧾 About</a>
</div>
""", unsafe_allow_html=True)

# DATABASE FUNCTIONS
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@007",   
        database="Police_checkpost"
    )

def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# OVERVIEW
st.markdown("<section id='overview'></section>", unsafe_allow_html=True)
st.title("🚓 Police Checkpost Logs: Police Traffic Stop Analytics Dashboard")

st.markdown("""
**Police Checkpost Logs** provides analytics on police traffic stops — including stop outcomes, demographics, and violations.  
It connects directly to your **MySQL database** and updates dynamically.
""")

# KPI CARDS
st.subheader("📈 Key Metrics")

kpi_query = """
SELECT 
    COUNT(*) AS total_stops,
    SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
    SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS total_searches,
    SUM(CASE WHEN violation = 'DUI' THEN 1 ELSE 0 END) AS drug_stops
FROM traffic_stops;
"""
df_kpi = run_query(kpi_query)

total_stops = int(df_kpi['total_stops'][0])
total_arrests = int(df_kpi['total_arrests'][0])
total_searches = int(df_kpi['total_searches'][0])
drug_stops = int(df_kpi['drug_stops'][0])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div style='background-color:#e3f2fd;padding:20px;border-radius:12px;text-align:center;'>"
                f"<h3 style='color:#0d47a1;'>🚔 Total Stops</h3><h2>{total_stops:,}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='background-color:#ffebee;padding:20px;border-radius:12px;text-align:center;'>"
                f"<h3 style='color:#b71c1c;'>🚨 Arrests</h3><h2>{total_arrests:,}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='background-color:#fff3e0;padding:20px;border-radius:12px;text-align:center;'>"
                f"<h3 style='color:#e65100;'>🔍 Searches</h3><h2>{total_searches:,}</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div style='background-color:#e8f5e9;padding:20px;border-radius:12px;text-align:center;'>"
                f"<h3 style='color:#1b5e20;'>💊 DUI </h3><h2>{drug_stops:,}</h2></div>", unsafe_allow_html=True)

st.divider()

# VISUAL INSIGHTS
st.markdown("<section id='insights'></section>", unsafe_allow_html=True)
st.header("📊 Visual Insights")

tab1, tab2, tab3 = st.tabs([
    "🚓 Stops by Violation",
    "🚻 Driver Gender Distribution",
    "⚖️ Stop Outcome Distribution"
])

# Tab 1: Stops by Violation
with tab1:
    vis_query = """
    SELECT violation AS Violation, COUNT(*) AS Count
    FROM traffic_stops
    GROUP BY violation
    ORDER BY Count DESC;
    """
    df_vis = run_query(vis_query)

    color_map = {
        "Speeding": "#1f77b4",     
        "Seatbelt": "#ffe70e",    
        "DUI": "#d62728",          
        "Other": "#2ca02c",      
        "Signal": "#ff7f0e"
    }

    fig1 = px.bar(
        df_vis,
        x="Violation",
        y="Count",
        color="Violation",
        color_discrete_map=color_map
    )

    fig1.update_layout(
        xaxis_title="Violation Type",
        yaxis_title="Count",
        showlegend=True
    )

    st.plotly_chart(fig1, use_container_width=True)

# Tab 2: Gender Distribution
with tab2:
    gen_query = """
        SELECT driver_gender AS Gender, COUNT(*) AS Count
        FROM traffic_stops
        GROUP BY driver_gender;
    """
    df_gen = run_query(gen_query)

    gender_colors = {
        "M": "#1f77b4",     
        "F": "#e377c2"    
    }

    fig2 = px.pie(
        df_gen,
        names="Gender",
        values="Count",
        color="Gender",
        color_discrete_map=gender_colors,
        hole=0.4
    )

    fig2.update_layout(
        showlegend=True
    )

    st.plotly_chart(fig2, use_container_width=True)

# Tab 3: Stop Outcome Distribution
with tab3:
    out_query = """
        SELECT stop_outcome AS Outcome, COUNT(*) AS Count
        FROM traffic_stops
        GROUP BY stop_outcome;
    """
    df_out = run_query(out_query)

    outcome_colors = {
        "Arrest": "#d62728",    
        "Warning": "#ff7f0e",   
        "Ticket": "#1f77b4",  
    }

    fig3 = px.bar(
        df_out,
        x="Outcome",
        y="Count",
        color="Outcome",
        color_discrete_map=outcome_colors
    )

    fig3.update_layout(
        xaxis_title="Outcome",
        yaxis_title="Count",
        showlegend=True
    )

    st.plotly_chart(fig3, use_container_width=True)
    
st.divider()

# INSIGHTS
st.markdown("<section id='insights'></section>", unsafe_allow_html=True)
st.header("📊 Insights Dashboard")

option = st.selectbox(
    "Select a query to run:",
    [
        "Top 10 Vehicles in Drug-Related Stops",
        "Vehicles Most Frequently Searched",
        "Arrest Rate by Driver Age Group",
        "Gender Distribution by Country",
        "Race + Gender Combination with Highest Search Rate",
        "Traffic Stops by Hour of Day",
        "Average Stop Duration by Violation",
        "Are Night Stops More Likely to Lead to Arrests?",
        "Violations Associated with Highest Search Rate",
        "Most Common Violations Among Younger Drivers (<25)",
        "Violations That Rarely Result in Search or Arrest",
        "Countries with Highest DUI (Drug-Related) Stops",
        "Arrest Rate by Country and Violation",
        "Countries with Most Search-Conducted Stops"
    ]
)

if st.button("Run Insight Query"):
     # ---------------- VEHICLE-BASED ----------------
    if option == "Top 10 Vehicles in Drug-Related Stops":
        q = """
            SELECT vehicle_number, COUNT(*) AS total_dui_stops
            FROM traffic_stops
            WHERE violation = 'DUI'
            GROUP BY vehicle_number
            ORDER BY total_dui_stops DESC
            LIMIT 10;
        """

    elif option == "Vehicles Most Frequently Searched":
        q = """
            SELECT vehicle_number, COUNT(*) AS search_count
            FROM traffic_stops
            WHERE search_conducted = TRUE
            GROUP BY vehicle_number
            ORDER BY search_count DESC
            LIMIT 10;
        """

    # ---------------- DEMOGRAPHIC-BASED ----------------
    elif option == "Arrest Rate by Driver Age Group":
        q = """
            SELECT 
                CASE 
                    WHEN driver_age < 18 THEN 'Under 18'
                    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
                    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+' END AS age_group,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
                ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY age_group
            ORDER BY arrest_rate DESC;
        """

    elif option == "Gender Distribution by Country":
        q = """
            SELECT country_name, driver_gender, COUNT(*) AS total
            FROM traffic_stops
            GROUP BY country_name, driver_gender
            ORDER BY country_name, total DESC;
        """

    elif option == "Race + Gender Combination with Highest Search Rate":
        q = """
            SELECT driver_race, driver_gender,
                   COUNT(*) AS total_stops,
                   SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS searches,
                   ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS search_rate
            FROM traffic_stops
            GROUP BY driver_race, driver_gender
            ORDER BY search_rate DESC
            LIMIT 10;
        """

    # ---------------- TIME-BASED ----------------
    elif option == "Traffic Stops by Hour of Day":
        q = """
            SELECT HOUR(stop_time) AS hour_of_day, COUNT(*) AS num_stops
            FROM traffic_stops
            GROUP BY hour_of_day
            ORDER BY hour_of_day;
        """

    elif option == "Average Stop Duration by Violation":
        q = """
            SELECT violation, AVG(stop_duration) AS avg_duration
            FROM traffic_stops
            GROUP BY violation
            ORDER BY avg_duration DESC;
        """

    elif option == "Are Night Stops More Likely to Lead to Arrests?":
        q = """
            SELECT 
                CASE 
                    WHEN HOUR(stop_time) BETWEEN 18 AND 23 THEN 'Night'
                    WHEN HOUR(stop_time) BETWEEN 0 AND 5 THEN 'Late Night'
                    ELSE 'Daytime'
                END AS time_period,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN stop_outcome='Arrest' THEN 1 ELSE 0 END) AS arrests,
                ROUND(SUM(CASE WHEN stop_outcome='Arrest' THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate
            FROM traffic_stops
            GROUP BY time_period
            ORDER BY arrest_rate DESC;
        """

    # ---------------- VIOLATION-BASED ----------------
    elif option == "Violations Associated with Highest Search Rate":
        q = """
            SELECT violation,
                   COUNT(*) AS total_stops,
                   SUM(CASE WHEN search_conducted=TRUE THEN 1 ELSE 0 END) AS searches,
                   ROUND(SUM(CASE WHEN search_conducted=TRUE THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS search_rate
            FROM traffic_stops
            GROUP BY violation
            ORDER BY search_rate DESC;
        """

    elif option == "Most Common Violations Among Younger Drivers (<25)":
        q = """
            SELECT violation, COUNT(*) AS total
            FROM traffic_stops
            WHERE driver_age < 25
            GROUP BY violation
            ORDER BY total DESC;
        """

    elif option == "Violations That Rarely Result in Search or Arrest":
        q = """
            SELECT violation,
                   COUNT(*) AS total_stops,
                   SUM(CASE WHEN search_conducted=TRUE THEN 1 ELSE 0 END) AS searches,
                   SUM(CASE WHEN stop_outcome='Arrest' THEN 1 ELSE 0 END) AS arrests
            FROM traffic_stops
            GROUP BY violation
            ORDER BY searches ASC, arrests ASC;
        """

    # ---------------- LOCATION-BASED ----------------
    elif option == "Countries with Highest DUI (Drug-Related) Stops":
        q = """
            SELECT country_name, COUNT(*) AS dui_stops
            FROM traffic_stops
            WHERE violation='DUI'
            GROUP BY country_name
            ORDER BY dui_stops DESC;
        """

    elif option == "Arrest Rate by Country and Violation":
        q = """
            SELECT country_name, violation,
                   COUNT(*) AS total_stops,
                   SUM(CASE WHEN stop_outcome='Arrest' THEN 1 ELSE 0 END) AS arrests,
                   ROUND(SUM(CASE WHEN stop_outcome='Arrest' THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate
            FROM traffic_stops
            GROUP BY country_name, violation
            ORDER BY arrest_rate DESC;
        """

    elif option == "Countries with Most Search-Conducted Stops":
        q = """
            SELECT country_name, COUNT(*) AS searches
            FROM traffic_stops
            WHERE search_conducted=TRUE
            GROUP BY country_name
            ORDER BY searches DESC;
        """

    df = run_query(q)
    st.dataframe(df, use_container_width=True)

st.divider()

# ------------------ ADVANCED INSIGHTS ------------------
st.markdown("<section id='advanced'></section>", unsafe_allow_html=True)
st.header("💡 Advanced Insights")

adv_query = st.selectbox(
    "Select advanced analysis:",
    [
        "Yearly Breakdown: Stops & Arrests by Country",
        "Driver Violation Trends by Age and Race",
        "Time Period Analysis (Year, Month, Hour)",
        "Violations with High Search & Arrest Rates",
        "Driver Demographics by Country",
        "Top 5 Violations with Highest Arrest Rates"
    ]
)

if st.button("Run Advanced Query"):
    if adv_query == "Yearly Breakdown: Stops & Arrests by Country":
        q = """
            SELECT 
                country_name,
                YEAR(stop_date) AS year,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS total_arrests,
                ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY country_name, year
            ORDER BY country_name, year;
        """
    elif adv_query == "Driver Violation Trends by Age and Race":
        q = """
            SELECT v.driver_race,
                   v.age_group,
                   v.violation,
                   COUNT(*) AS total_stops
            FROM (
                SELECT 
                    driver_race,
                    violation,
                    CASE 
                        WHEN driver_age < 18 THEN 'Under 18'
                        WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                        WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
                        WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                        ELSE '60+' 
                    END AS age_group
                FROM traffic_stops
            ) v
            GROUP BY v.driver_race, v.age_group, v.violation
            ORDER BY v.driver_race, v.age_group, total_stops DESC;
        """
    elif adv_query == "Time Period Analysis (Year, Month, Hour)":
        q = """
            SELECT 
                YEAR(stop_date) AS year,
                MONTH(stop_date) AS month,
                HOUR(stop_time) AS hour,
                COUNT(*) AS total_stops
            FROM traffic_stops
            GROUP BY year, month, hour
            ORDER BY year, month, hour;
        """
    elif adv_query == "Violations with High Search & Arrest Rates":
        q = """
            SELECT 
                violation,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS searches,
                SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrests,
                ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS search_rate,
                ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            ORDER BY arrest_rate DESC;
        """
    elif adv_query == "Driver Demographics by Country":
        q = """
            SELECT 
                country_name,
                driver_gender,
                driver_race,
                CASE 
                    WHEN driver_age < 18 THEN 'Under 18'
                    WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN driver_age BETWEEN 26 AND 40 THEN '26-40'
                    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+' END AS age_group,
                COUNT(*) AS total
            FROM traffic_stops
            GROUP BY country_name, driver_gender, driver_race, age_group
            ORDER BY country_name, total DESC;
        """
    elif adv_query == "Top 5 Violations with Highest Arrest Rates":
        q = """
            SELECT 
                violation,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) AS arrests,
                ROUND(SUM(CASE WHEN stop_outcome = 'Arrest' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate
            FROM traffic_stops
            GROUP BY violation
            ORDER BY arrest_rate DESC
            LIMIT 5;
        """



    df = run_query(q)
    st.dataframe(df, use_container_width=True)

st.divider()


# SEARCH EXPLORER

st.markdown("<section id='search'></section>", unsafe_allow_html=True)
st.header("🔍 Vehicle Search")

vehicle_input = st.text_input("Enter Vehicle Number:")
if vehicle_input:
    q = f"SELECT * FROM traffic_stops WHERE vehicle_number LIKE '%{vehicle_input}%';"
    df_vehicle = run_query(q)
    if df_vehicle.empty:
        st.warning("No records found for that vehicle number.")
    else:
        st.success(f"Found {len(df_vehicle)} record(s)")
        st.dataframe(df_vehicle, use_container_width=True)

st.divider()

# PREDICT OUTCOME

st.markdown("<section id='predict'></section>", unsafe_allow_html=True)
st.header("🤖 Predict Stop Outcome & Violation")

col1, col2 = st.columns(2)
with col1:
    driver_age = st.number_input("Driver Age", min_value=16, max_value=90, value=30)
    driver_gender = st.selectbox("Driver Gender", ["male", "female"])
    stop_date = st.date_input("Stop Date", datetime.today().date())
    stop_time = st.time_input("Stop Time", datetime.now().time())
    country = st.text_input("Country Name")
with col2:
    search_conducted = st.selectbox("Was Search Conducted?", [0, 1])
    drugs_related = st.selectbox("Was it Drug Related?", [0, 1])
    stop_duration = st.selectbox("Stop Duration", ["0-15 Min", "16-30 Min", "30+ Min"])
    vehicle_number = st.text_input("Vehicle Number")

if st.button("Predict Stop Outcome & Violation"):
    import random
    violation = random.choice(["Speeding", "Seatbelt", "Expired License", "Signal Jump"])
    outcome = random.choice(["Warning", "Arrest", "Citation"])

    st.markdown("### 🚓 Prediction Summary")
    st.markdown(f"""
    
    🧾 A {driver_age}-year-old {driver_gender} driver from **{country or 'Unknown'}**  
    was stopped at **{stop_time.strftime('%H:%M')}** on **{stop_date.strftime('%Y-%m-%d')}**.  
    {'A search was conducted,' if search_conducted else 'No search was conducted,'}  
    and the stop {'was drug-related.' if drugs_related else 'was not drug-related.'}  
    Stop duration: **{stop_duration}**. 
    **Stop Violation:** {violation}  
    **Stop Outcome:** {outcome}  
    Vehicle Number: **{vehicle_number or '****'}**.
    """)

st.divider()


# ABOUT
st.markdown("<section id='about'></section>", unsafe_allow_html=True)
st.header("🧾 About / Project Info")

st.markdown("""
**Police Checkpost Logs** is a data-driven dashboard built using **Streamlit**, **Python**, and **MySQL**.  
It provides insight into police traffic stop patterns, violations, and demographics.

**Tools Used:**
- Python (pandas, plotly, mysql.connector)
- MySQL (data storage & queries)
- Streamlit (interactive web app)

**Created by:** Yogaprabhu Ramesh Kanna
""")