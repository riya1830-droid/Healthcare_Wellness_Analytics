import streamlit as st
import pandas as pd
import mysql.connector

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Healthcare & Wellness Analytics",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏥 Healthcare & Wellness Analytics")
st.subheader("Customer Journey & Business Overview")

# --------------------------------------------------
# MYSQL CONNECTION
# --------------------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyNewPassword123!",
    database="patient_analysis"
)

# --------------------------------------------------
# BUSINESS KPI QUERY
# --------------------------------------------------

query = """
SELECT
    (SELECT COUNT(*) FROM customers) AS total_customers,

    (SELECT COUNT(DISTINCT Customer_ID)
     FROM consultations) AS consulted_customers,

    (SELECT COUNT(DISTINCT Customer_ID)
     FROM programs) AS enrolled_customers,

    (SELECT COUNT(DISTINCT Customer_ID)
     FROM programs
     WHERE Program_Completed = 'Yes') AS completed_customers,

    (SELECT COUNT(DISTINCT Customer_ID)
     FROM programs
     WHERE Goal_Achieved = 'Yes') AS goal_achieved_customers,

    (SELECT COUNT(DISTINCT Customer_ID)
     FROM subscriptions
     WHERE Renewed = 'Renewed') AS renewed_customers,

    ROUND(
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
            WHERE Program_Completed = 'Yes'
        )
        /
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
        ) * 100,
        2
    ) AS completion_rate,

    ROUND(
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
            WHERE Goal_Achieved = 'Yes'
        )
        /
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
            WHERE Program_Completed = 'Yes'
        ) * 100,
        2
    ) AS goal_rate,

    ROUND(
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM subscriptions
            WHERE Renewed = 'Renewed'
        )
        /
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
            WHERE Goal_Achieved = 'Yes'
        ) * 100,
        2
    ) AS renewal_rate
"""

kpi = pd.read_sql(query, conn)

# --------------------------------------------------
# EXTRACT KPI VALUES
# --------------------------------------------------

# EXTRACT KPI VALUES
# --------------------------------------------------

total_customers = int(kpi.iloc[0]["total_customers"])
consulted_customers = int(kpi.iloc[0]["consulted_customers"])
enrolled_customers = int(kpi.iloc[0]["enrolled_customers"])
completed_customers = int(kpi.iloc[0]["completed_customers"])
goal_achieved_customers = int(kpi.iloc[0]["goal_achieved_customers"])
renewed_customers = int(kpi.iloc[0]["renewed_customers"])


completion_rate = kpi.iloc[0]["completion_rate"]
goal_rate = kpi.iloc[0]["goal_rate"]
renewal_rate = kpi.iloc[0]["renewal_rate"]

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "🩺 Consulted",
        f"{consulted_customers:,}"
    )

with col3:
    st.metric(
        "📋 Enrolled",
        f"{enrolled_customers:,}"
    )

with col4:
    st.metric(
        "✅ Completed",
        f"{completed_customers:,}"
    )

with col5:
    st.metric(
        "🎯 Goals Achieved",
        f"{goal_achieved_customers:,}"
    )

with col6:
    st.metric(
        "🔄 Renewed",
        f"{renewed_customers:,}"
    )

# --------------------------------------------------
# CUSTOMER JOURNEY FUNNEL
# --------------------------------------------------

import plotly.graph_objects as go

st.markdown("---")

st.subheader("🚶 Customer Journey Funnel")

funnel_data = {
    "Stage": [
        "Registration",
        "Consultation",
        "Enrollment",
        "Program Completion",
        "Goal Achievement",
        "Renewal"
    ],
    "Customers": [
        total_customers,
        consulted_customers,
        enrolled_customers,
        completed_customers,
        goal_achieved_customers,
        renewed_customers
    ]
}

fig = go.Figure(
    go.Funnel(
        y=funnel_data["Stage"],
        x=funnel_data["Customers"],

        # Show customer numbers
        textinfo="value",

        # Bright funnel colors
        marker=dict(
            color=[
                "#00C853",  # Registration
                "#00B0FF",  # Consultation
                "#7C4DFF",  # Enrollment
                "#FF9100",  # Completion
                "#FFD600",  # Goal Achievement
                "#FF1744"   # Renewal
            ]
        ),

        # Number styling
        textfont=dict(
            color="white",
            size=20,
            family="Arial Black"
        )
    )
)

fig.update_layout(
    title="Customer Journey",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# KEY JOURNEY INSIGHTS
# --------------------------------------------------

st.markdown("---")
st.subheader("🔎 Key Journey Insights")

col1, col2 = st.columns(2)

with col1:
    st.info(
        "🟢 **Strong Early Engagement**\n\n"
        f"{consulted_customers:,} of {total_customers:,} customers "
        "reached consultation and program enrollment."
    )

with col2:
    st.warning(
        "🟠 **Main Journey Drop-off**\n\n"
        f"{completed_customers:,} of {enrolled_customers:,} enrolled "
        f"customers completed their programs — **{completion_rate:.2f}%**."
    )

col3, col4 = st.columns(2)

with col3:
    st.success(
        "🎯 **Strong Goal Achievement**\n\n"
        f"{goal_achieved_customers:,} customers achieved their goals — "
        f"**{goal_rate:.2f}%** of completed customers."
    )

with col4:
    st.success(
        "🔄 **Renewal Performance**\n\n"
        f"{renewed_customers:,} customers renewed — "
        f"**{renewal_rate:.2f}%** of goal achievers."
    )

# --------------------------------------------------
# CLOSE CONNECTION
# --------------------------------------------------

conn.close()

