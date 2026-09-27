import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Advanced Customer Insights",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Advanced Customer Insights & Business Recommendations")
st.markdown(
    "Advanced SQL analysis of customer success, adherence, retention, and revenue."
)
st.divider()

# ---------------- DATABASE ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyNewPassword123!",
    database="patient_analysis"
)

# =========================================================
# 7.1 CUSTOMER SUCCESS SEGMENTATION
# =========================================================
st.subheader("7.1 🏆 Customer Success Segmentation")

query = """
WITH customer_outcomes AS (
    SELECT
        p.Customer_ID,
        MAX(CASE WHEN p.Program_Completed = 'Yes' THEN 1 ELSE 0 END) AS completed,
        MAX(CASE WHEN p.Goal_Achieved = 'Yes' THEN 1 ELSE 0 END) AS goal_achieved,
        MAX(CASE WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END) AS renewed
    FROM programs p
    LEFT JOIN subscriptions s
        ON p.Customer_ID = s.Customer_ID
    GROUP BY p.Customer_ID
)
SELECT
    CASE
        WHEN completed = 1 AND goal_achieved = 1 AND renewed = 1
            THEN 'Successful Journey'
        WHEN completed = 1 AND goal_achieved = 1 AND renewed = 0
            THEN 'Goal Achieved - Not Renewed'
        WHEN completed = 1 AND goal_achieved = 0
            THEN 'Completed - Goal Not Achieved'
        ELSE 'Program Not Completed'
    END AS customer_segment,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM customer_outcomes
GROUP BY customer_segment
ORDER BY customers DESC;
"""

success_df = pd.read_sql(query, conn)
st.dataframe(success_df, use_container_width=True, hide_index=True)

# =========================================================
# 7.2 HIGH-VALUE CUSTOMER RANKING
# =========================================================
st.subheader("7.2 📊 High-Value Customer Ranking")

query = """
WITH ranked_customers AS (
    SELECT
        Customer_ID,
        Total_Revenue,
        RANK() OVER (ORDER BY Total_Revenue DESC) AS revenue_rank
    FROM subscriptions
)
SELECT
    Customer_ID,
    Total_Revenue,
    revenue_rank
FROM ranked_customers
WHERE revenue_rank <= 10
ORDER BY revenue_rank;
"""

ranking_df = pd.read_sql(query, conn)
st.dataframe(ranking_df, use_container_width=True, hide_index=True)

# =========================================================
# 7.3 ADHERENCE VS BUSINESS OUTCOMES
# =========================================================
st.subheader("7.3 🎯 Adherence vs Business Outcomes")

query = """
SELECT
    CASE
        WHEN Adherence_Percent < 50 THEN 'Low (<50%)'
        WHEN Adherence_Percent < 75 THEN 'Moderate (50-74%)'
        WHEN Adherence_Percent < 90 THEN 'High (75-89%)'
        ELSE 'Very High (90%+)'
    END AS adherence_segment,

    COUNT(*) AS program_enrollments,
    ROUND(AVG(Adherence_Percent), 2) AS avg_adherence,

    ROUND(
        SUM(CASE WHEN Program_Completed = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS completion_rate,

    ROUND(
        SUM(CASE WHEN Goal_Achieved = 'Yes' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2
    ) AS goal_achievement_rate

FROM programs

GROUP BY adherence_segment
ORDER BY avg_adherence;
"""

adherence_df = pd.read_sql(query, conn)

st.dataframe(adherence_df, use_container_width=True, hide_index=True)

fig = px.bar(
    adherence_df,
    x="adherence_segment",
    y=["completion_rate", "goal_achievement_rate"],
    barmode="group",
    title="Adherence vs Completion & Goal Achievement",
    labels={
        "value": "Rate (%)",
        "adherence_segment": "Adherence Segment",
        "variable": "Metric"
    },
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 7.4 HIGH-VALUE CUSTOMER ANALYSIS
# =========================================================
st.subheader("7.4 💰 High-Value Customer Analysis")

query = """
WITH customer_outcomes AS (
    SELECT
        Customer_ID,
        MAX(CASE WHEN Program_Completed = 'Yes' THEN 1 ELSE 0 END) AS completed,
        MAX(CASE WHEN Goal_Achieved = 'Yes' THEN 1 ELSE 0 END) AS goal_achieved
    FROM programs
    GROUP BY Customer_ID
)

SELECT
    CASE
        WHEN s.Total_Revenue >= 20000 THEN '₹20K+'
        WHEN s.Total_Revenue >= 10000 THEN '₹10K - ₹20K'
        WHEN s.Total_Revenue >= 5000 THEN '₹5K - ₹10K'
        ELSE 'Below ₹5K'
    END AS revenue_segment,

    COUNT(*) AS customers,
    ROUND(AVG(s.Total_Revenue), 2) AS avg_revenue,

    ROUND(
        SUM(COALESCE(o.completed, 0)) * 100.0 / COUNT(*), 2
    ) AS completion_rate,

    ROUND(
        SUM(COALESCE(o.goal_achieved, 0)) * 100.0 / COUNT(*), 2
    ) AS goal_achievement_rate

FROM subscriptions s

LEFT JOIN customer_outcomes o
    ON s.Customer_ID = o.Customer_ID

GROUP BY revenue_segment
ORDER BY avg_revenue DESC;
"""

value_df = pd.read_sql(query, conn)
st.dataframe(value_df, use_container_width=True, hide_index=True)

# =========================================================
# 7.5 ADHERENCE → COMPLETION → GOAL → RENEWAL
# =========================================================
st.subheader("7.5 🔎 Customer Journey Relationship")

query = """
WITH customer_journey AS (
    SELECT
        p.Customer_ID,

        MAX(CASE WHEN p.Program_Completed = 'Yes' THEN 1 ELSE 0 END)
            AS completed,

        MAX(CASE WHEN p.Goal_Achieved = 'Yes' THEN 1 ELSE 0 END)
            AS goal_achieved,

        MAX(CASE WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END)
            AS renewed,

        MAX(p.Adherence_Percent) AS adherence

    FROM programs p

    LEFT JOIN subscriptions s
        ON p.Customer_ID = s.Customer_ID

    GROUP BY p.Customer_ID
)

SELECT
    CASE
        WHEN adherence >= 90 THEN '90%+'
        WHEN adherence >= 75 THEN '75-89%'
        WHEN adherence >= 50 THEN '50-74%'
        ELSE '<50%'
    END AS adherence_group,

    COUNT(*) AS customers,

    ROUND(SUM(completed) * 100.0 / COUNT(*), 2)
        AS completion_rate,

    ROUND(SUM(goal_achieved) * 100.0 / COUNT(*), 2)
        AS goal_rate,

    ROUND(SUM(renewed) * 100.0 / COUNT(*), 2)
        AS renewal_rate

FROM customer_journey

GROUP BY adherence_group
ORDER BY MIN(adherence);
"""

journey_df = pd.read_sql(query, conn)

st.dataframe(journey_df, use_container_width=True, hide_index=True)

fig = px.line(
    journey_df,
    x="adherence_group",
    y=["completion_rate", "goal_rate", "renewal_rate"],
    markers=True,
    title="Adherence Across the Customer Journey",
    labels={
        "value": "Rate (%)",
        "adherence_group": "Adherence Group",
        "variable": "Metric"
    }
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# 7.6 DYNAMIC BUSINESS INSIGHTS
# =========================================================
st.subheader("7.6 💡 Dynamic Business Insights")

largest_segment = success_df.loc[
    success_df["customers"].idxmax(), "customer_segment"
]

best_completion_segment = adherence_df.loc[
    adherence_df["completion_rate"].idxmax(), "adherence_segment"
]

highest_value_segment = value_df.loc[
    value_df["avg_revenue"].idxmax(), "revenue_segment"
]

best_renewal_group = journey_df.loc[
    journey_df["renewal_rate"].idxmax(), "adherence_group"
]

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"🏆 **Largest Customer Segment:** {largest_segment}"
    )

with col2:
    st.success(
        f"🎯 **Highest Completion Segment:** {best_completion_segment}"
    )

col3, col4 = st.columns(2)

with col3:
    st.info(
        f"💰 **Highest-Value Segment:** {highest_value_segment}"
    )

with col4:
    st.success(
        f"🔄 **Highest Renewal Group:** {best_renewal_group}"
    )

# =========================================================
# BUSINESS SUMMARY
# =========================================================
st.subheader("📌 Business Summary")

st.success(
    """
    Advanced SQL analysis connects customer adherence,
    program outcomes, retention, and revenue to identify
    important customer segments and business opportunities.
    """
)

conn.close()