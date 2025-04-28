import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
file_path = "EXECUTIVE RANKING/EXECUTIVE RANKING.xlsx"
df = pd.read_excel(file_path)

# Clean column names and remove duplicate columns if any
df.columns = df.columns.str.strip()
df = df.loc[:, ~df.columns.duplicated()]

# Define the performance metrics to visualize.
# Values in the Excel are stored as decimals (e.g. 1.12677 means 112.68%)
performance_metrics = {
    "Overall Sales Achievement %": "OVERALL SALES ACH %",
    "Pharma Achievement %": "PHARMA ACH %",
    "PL Achievement %": "PL ACH %",
    "General Achievement %": "GEN ACH %",
    "FMCG Achievement %": "FMCG ACH %",
    "CP Growth %": "CP GRT %"
}

# Convert performance metric columns and NOB (Number of Branches) to numeric values
for col in performance_metrics.values():
    df[col] = pd.to_numeric(df[col], errors="coerce")
df["NOB"] = pd.to_numeric(df["NOB"], errors="coerce")

# Streamlit app title
st.title("📊 Executive Sales Performance Dashboard")

# Sidebar Filters with "All" options
category_options = ["All"] + list(df["CATEGORY"].unique())
dgm_options = ["All"] + list(df["DGM"].unique())
employee_options = ["All"] + list(df["EMPLOYEE NAME"].unique())

selected_category = st.sidebar.selectbox("🔍 Select Category:", category_options)
selected_dgm = st.sidebar.selectbox("🏢 Select DGM:", dgm_options)
selected_employee = st.sidebar.selectbox("👤 Select Employee Name:", employee_options)

# Filter data based on selections (if "All" is not selected, then filter)
filtered_data = df.copy()
if selected_category != "All":
    filtered_data = filtered_data[filtered_data["CATEGORY"] == selected_category]
if selected_dgm != "All":
    filtered_data = filtered_data[filtered_data["DGM"] == selected_dgm]
if selected_employee != "All":
    filtered_data = filtered_data[filtered_data["EMPLOYEE NAME"] == selected_employee]

# Sort data by Overall Sales Achievement % (highest first)
filtered_data = filtered_data.sort_values(by="OVERALL SALES ACH %", ascending=False)

# Display a table of key columns (including NOB and performance metrics)
table_columns = ["EMPLOYEE NAME", "CATEGORY", "DGM", "NOB"] + list(performance_metrics.values())
st.write(f"🏅 **Performance Metrics for {selected_category} - {selected_dgm} - {selected_employee}** 🏅")
st.dataframe(filtered_data[table_columns].reset_index(drop=True))

# For each performance metric, create a bar chart that displays the metric as a percentage
# and also shows the NOB value inside the bar's text label.
for metric_name, col in performance_metrics.items():
    # Create a text label that includes the performance percentage and the NOB.
    # For example, if the metric is 1.12677 and NOB is 9, the label becomes "112.68% (9)".
    text_vals = filtered_data.apply(
        lambda row: f"{row[col]*100:.2f}% ({int(row['NOB'])})" if pd.notnull(row[col]) and pd.notnull(row["NOB"]) else "",
        axis=1
    )
    fig = px.bar(
        filtered_data,
        x="EMPLOYEE NAME",
        y=col,
        title=f"{metric_name} Comparison",
        color="EMPLOYEE NAME",
        text=text_vals  # Display the combined text on the bars
    )
    # Format the y-axis tick labels as percentages
    fig.update_yaxes(tickformat=".2%")
    fig.update_layout(
        yaxis_title=metric_name,
        xaxis_title="Employee Name"
    )
    st.plotly_chart(fig)

st.write("🎯 Use the sidebar filters to compare performance metrics (displayed as percentages) along with the Number of Branches (NOB) across employees!")
        text_auto=True
    )
    st.plotly_chart(fig)

st.write("🎯 Select different filters in the sidebar to compare rankings across employees!")
