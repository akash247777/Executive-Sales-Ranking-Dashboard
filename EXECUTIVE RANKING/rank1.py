import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
file_path = "EXECUTIVE RANKING.xlsx"
df = pd.read_excel(file_path)

# Clean column names
df.columns = df.columns.str.strip()

# Ranking metrics
ranking_metrics = {
    "Overall Sales Ach % Rank": "OVERALL SALES ACH % RANK",
    "Pharma Ach % Rank": "PHARMA ACH % RANK",
    "PL Ach % Rank": "PL ACH % RANK",
    "General Ach % Rank": "GEN ACH % RANK",
    "FMCG Ach % Rank": "FMCG ACH % RANK",
    "CP Growth % Rank": "CP GRT % RANK"
}

# Convert ranking columns to numeric for sorting
for column in ranking_metrics.values():
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Streamlit app setup
st.title("📊 Executive Sales Ranking Dashboard")

# Sidebar filters
category_options = df["CATEGORY"].unique()
dgm_options = df["DGM"].unique()

selected_category = st.sidebar.selectbox("🔍 Select Category:", category_options)
selected_dgm = st.sidebar.selectbox("🏢 Select DGM:", dgm_options)

# Filter data based on selection (Show all employees in the same category and DGM)
filtered_data = df[(df["CATEGORY"] == selected_category) & (df["DGM"] == selected_dgm)].copy()

# Sort by Overall Sales Ach % Rank
filtered_data = filtered_data.sort_values(by="OVERALL SALES ACH % RANK")

# Show rankings comparison table
st.write(f"🏅 **Performance Rankings for Employees in {selected_category} - {selected_dgm}** 🏅")
st.dataframe(filtered_data[["EMPLOYEE NAME", "CATEGORY"] + list(ranking_metrics.values())].reset_index(drop=True))

# Visualization: Compare rankings across employees
for metric_name, column in ranking_metrics.items():
    fig = px.bar(
        filtered_data, 
        x="EMPLOYEE NAME", 
        y=column, 
        title=f"{metric_name} Rankings Comparison",
        color="EMPLOYEE NAME",
        text_auto=True
    )
    st.plotly_chart(fig)

st.write("🎯 Select different filters in the sidebar to compare rankings across employees!")
