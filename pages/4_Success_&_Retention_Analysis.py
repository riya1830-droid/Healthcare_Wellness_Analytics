import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Success & Retention Analysis",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📈 Success & Retention Analysis")

st.markdown(
    "Analyze customer success after program enrollment, "
    "from program completion to goal achievement and subscription renewal."
)

st.divider()


# ============================================================
# MYSQL CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyNewPassword123!",
    database="patient_analysis"
)


# ============================================================
# 1. SUCCESS & RETENTION KPI OVERVIEW
# ============================================================

kpi_query = """
SELECT

    /* Completed customers */
    (
        SELECT COUNT(DISTINCT Customer_ID)
        FROM programs
        WHERE Program_Completed = 'Yes'
    ) AS completed_customers,

    /* Goal achieved customers */
    (
        SELECT COUNT(DISTINCT Customer_ID)
        FROM programs
        WHERE Goal_Achieved = 'Yes'
    ) AS goal_achieved_customers,

    /* Renewed customers */
    (
        SELECT COUNT(DISTINCT Customer_ID)
        FROM subscriptions
        WHERE Renewed = 'Renewed'
    ) AS renewed_customers,

    /* Completion → Goal */
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
    ) AS completion_to_goal_rate,

    /* Goal → Renewal */
    ROUND(
        (
            SELECT COUNT(DISTINCT p.Customer_ID)
            FROM programs p
            INNER JOIN subscriptions s
                ON p.Customer_ID = s.Customer_ID
            WHERE p.Goal_Achieved = 'Yes'
              AND s.Renewed = 'Renewed'
        )
        /
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
            WHERE Goal_Achieved = 'Yes'
        ) * 100,
        2
    ) AS goal_to_renewal_rate,

    /* Completion → Renewal */
    ROUND(
        (
            SELECT COUNT(DISTINCT p.Customer_ID)
            FROM programs p
            INNER JOIN subscriptions s
                ON p.Customer_ID = s.Customer_ID
            WHERE p.Program_Completed = 'Yes'
              AND s.Renewed = 'Renewed'
        )
        /
        (
            SELECT COUNT(DISTINCT Customer_ID)
            FROM programs
            WHERE Program_Completed = 'Yes'
        ) * 100,
        2
    ) AS completion_to_renewal_rate

FROM dual;
"""

kpi_df = pd.read_sql(kpi_query, conn)


completed_customers = int(
    kpi_df.loc[0, "completed_customers"]
)

goal_achieved_customers = int(
    kpi_df.loc[0, "goal_achieved_customers"]
)

renewed_customers = int(
    kpi_df.loc[0, "renewed_customers"]
)

completion_to_goal_rate = float(
    kpi_df.loc[0, "completion_to_goal_rate"]
)

goal_to_renewal_rate = float(
    kpi_df.loc[0, "goal_to_renewal_rate"]
)

completion_to_renewal_rate = float(
    kpi_df.loc[0, "completion_to_renewal_rate"]
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "✅ Completed Customers",
        f"{completed_customers:,}"
    )

with col2:
    st.metric(
        "🎯 Goal Achieved",
        f"{goal_achieved_customers:,}"
    )

with col3:
    st.metric(
        "🔄 Renewed Customers",
        f"{renewed_customers:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "📈 Completion → Goal",
        f"{completion_to_goal_rate:.2f}%"
    )

with col5:
    st.metric(
        "🔁 Goal → Renewal",
        f"{goal_to_renewal_rate:.2f}%"
    )

with col6:
    st.metric(
        "💎 Completion → Renewal",
        f"{completion_to_renewal_rate:.2f}%"
    )


st.divider()


# ============================================================
# 2. COMPLETION → GOAL ACHIEVEMENT
# ============================================================

st.subheader("🎯 Program Completion → Goal Achievement")

completion_goal_query = """
SELECT

    COUNT(DISTINCT CASE
        WHEN Program_Completed = 'Yes'
        THEN Customer_ID
    END) AS completed_customers,

    COUNT(DISTINCT CASE
        WHEN Program_Completed = 'Yes'
         AND Goal_Achieved = 'Yes'
        THEN Customer_ID
    END) AS goal_achieved_customers,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN Program_Completed = 'Yes'
             AND Goal_Achieved = 'Yes'
            THEN Customer_ID
        END)
        /
        COUNT(DISTINCT CASE
            WHEN Program_Completed = 'Yes'
            THEN Customer_ID
        END) * 100,
        2
    ) AS completion_to_goal_rate

FROM programs;
"""

completion_goal_df = pd.read_sql(
    completion_goal_query,
    conn
)


# ------------------------------------------------------------
# DISPLAY METRICS
# ------------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Completed Customers",
        f"{int(completion_goal_df.loc[0, 'completed_customers']):,}"
    )

with col2:
    st.metric(
        "Goal Achieved",
        f"{int(completion_goal_df.loc[0, 'goal_achieved_customers']):,}"
    )

with col3:
    st.metric(
        "Completion → Goal",
        f"{float(completion_goal_df.loc[0, 'completion_to_goal_rate']):.2f}%"
    )


# ============================================================
# 3. GOAL ACHIEVEMENT → RENEWAL
# ============================================================

st.divider()

st.subheader("🔄 Goal Achievement → Subscription Renewal")

goal_renewal_query = """
SELECT

    COUNT(DISTINCT p.Customer_ID) AS goal_achieved_customers,

    COUNT(DISTINCT CASE
        WHEN s.Renewed = 'Renewed'
        THEN p.Customer_ID
    END) AS renewed_customers,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN s.Renewed = 'Renewed'
            THEN p.Customer_ID
        END)
        /
        COUNT(DISTINCT p.Customer_ID) * 100,
        2
    ) AS goal_to_renewal_rate

FROM programs p

INNER JOIN subscriptions s
    ON p.Customer_ID = s.Customer_ID

WHERE p.Goal_Achieved = 'Yes';
"""

goal_renewal_df = pd.read_sql(
    goal_renewal_query,
    conn
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎯 Goal Achieved",
        f"{int(goal_renewal_df.loc[0, 'goal_achieved_customers']):,}"
    )

with col2:
    st.metric(
        "🔄 Renewed",
        f"{int(goal_renewal_df.loc[0, 'renewed_customers']):,}"
    )

with col3:
    st.metric(
        "Goal → Renewal",
        f"{float(goal_renewal_df.loc[0, 'goal_to_renewal_rate']):.2f}%"
    )


# ============================================================
# 4. COMPLETION → RENEWAL
# ============================================================

st.divider()

st.subheader("💎 Program Completion → Subscription Renewal")

completion_renewal_query = """
SELECT

    COUNT(DISTINCT p.Customer_ID) AS completed_customers,

    COUNT(DISTINCT CASE
        WHEN s.Renewed = 'Renewed'
        THEN p.Customer_ID
    END) AS renewed_customers,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN s.Renewed = 'Renewed'
            THEN p.Customer_ID
        END)
        /
        COUNT(DISTINCT p.Customer_ID) * 100,
        2
    ) AS completion_to_renewal_rate

FROM programs p

INNER JOIN subscriptions s
    ON p.Customer_ID = s.Customer_ID

WHERE p.Program_Completed = 'Yes';
"""

completion_renewal_df = pd.read_sql(
    completion_renewal_query,
    conn
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "✅ Completed",
        f"{int(completion_renewal_df.loc[0, 'completed_customers']):,}"
    )

with col2:
    st.metric(
        "🔄 Renewed",
        f"{int(completion_renewal_df.loc[0, 'renewed_customers']):,}"
    )

with col3:
    st.metric(
        "Completion → Renewal",
        f"{float(completion_renewal_df.loc[0, 'completion_to_renewal_rate']):.2f}%"
    )


# ============================================================
# 5. SUCCESS & RETENTION FUNNEL
# ============================================================

st.divider()

st.subheader("📊 Success & Retention Funnel")


funnel_query = """
SELECT
    'Program Completion' AS stage,
    COUNT(DISTINCT Customer_ID) AS customers,
    1 AS stage_order
FROM programs
WHERE Program_Completed = 'Yes'

UNION ALL

SELECT
    'Goal Achievement' AS stage,
    COUNT(DISTINCT Customer_ID) AS customers,
    2 AS stage_order
FROM programs
WHERE Goal_Achieved = 'Yes'

UNION ALL

SELECT
    'Subscription Renewal' AS stage,
    COUNT(DISTINCT Customer_ID) AS customers,
    3 AS stage_order
FROM subscriptions
WHERE Renewed = 'Renewed'

ORDER BY stage_order;
"""

funnel_df = pd.read_sql(
    funnel_query,
    conn
)


fig_funnel = px.funnel(
    funnel_df,
    y="stage",
    x="customers",
    text="customers",
    color="stage",
    color_discrete_sequence=[
        "#00C853",
        "#FFD600",
        "#FF1744"
    ],
    title="Customer Success & Retention Journey"
)

fig_funnel.update_traces(
    textinfo="value",
    textfont=dict(
        color="white",
        size=20,
        family="Arial Black"
    )
)

fig_funnel.update_layout(
    height=550,
    showlegend=False
)

st.plotly_chart(
    fig_funnel,
    use_container_width=True
)


# ============================================================
# 6. RETENTION CONVERSION COMPARISON
# ============================================================

st.subheader("📈 Retention Conversion Rates")


retention_rates_df = pd.DataFrame({
    "Stage": [
        "Completion → Goal",
        "Goal → Renewal",
        "Completion → Renewal"
    ],
    "Conversion Rate": [
        completion_to_goal_rate,
        goal_to_renewal_rate,
        completion_to_renewal_rate
    ]
})


fig_retention = px.bar(
    retention_rates_df,
    x="Stage",
    y="Conversion Rate",
    text="Conversion Rate",
    color="Stage",
    color_discrete_sequence=px.colors.qualitative.Bold,
    title="Success & Retention Conversion Rates",
    labels={
        "Conversion Rate": "Conversion Rate (%)"
    }
)

fig_retention.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_retention.update_layout(
    showlegend=False,
    height=500,
    yaxis=dict(
        range=[
            0,
            min(100, max(retention_rates_df["Conversion Rate"]) + 15)
        ]
    )
)

st.plotly_chart(
    fig_retention,
    use_container_width=True
)


# ============================================================
# 7. SUCCESS STATUS BREAKDOWN
# ============================================================

st.divider()

st.subheader("👥 Customer Success Status")


success_status_query = """
SELECT
    status,
    COUNT(DISTINCT Customer_ID) AS customers

FROM
(
    SELECT
        Customer_ID,

        CASE

            WHEN Program_Completed = 'Yes'
             AND Goal_Achieved = 'Yes'
            THEN 'Goal Achieved'

            WHEN Program_Completed = 'Yes'
             AND Goal_Achieved = 'No'
            THEN 'Completed - Goal Not Achieved'

            WHEN Program_Completed = 'No'
            THEN 'Not Completed'

            ELSE 'Other'

        END AS status

    FROM programs
) AS customer_status

GROUP BY status

ORDER BY customers DESC;
"""

success_status_df = pd.read_sql(
    success_status_query,
    conn
)


fig_success = px.pie(
    success_status_df,
    names="status",
    values="customers",
    hole=0.55,
    color="status",
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Customer Program Success Status"
)

fig_success.update_traces(
    textinfo="label+percent",
    textposition="outside"
)

fig_success.update_layout(
    height=500
)

st.plotly_chart(
    fig_success,
    use_container_width=True
)


# ============================================================
# 8. DYNAMIC BUSINESS INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Success & Retention Insights")


# ------------------------------------------------------------
# Dynamic values
# ------------------------------------------------------------

completion_to_goal = completion_to_goal_rate
goal_to_renewal = goal_to_renewal_rate
completion_to_renewal = completion_to_renewal_rate


# ------------------------------------------------------------
# Calculate drop-offs dynamically
# ------------------------------------------------------------

goal_dropoff = completed_customers - goal_achieved_customers

renewal_dropoff = goal_achieved_customers - renewed_customers

completion_renewal_dropoff = (
    completed_customers - renewed_customers
)


col1, col2 = st.columns(2)


with col1:

    st.info(
        f"🎯 **Completion → Goal:** "
        f"{completion_to_goal:.2f}% of completed customers "
        f"achieved their goal."
    )

    st.warning(
        f"📉 **Goal Achievement Gap:** "
        f"{goal_dropoff:,} completed customers "
        f"did not achieve their goal."
    )

    st.success(
        f"🔄 **Goal → Renewal:** "
        f"{goal_to_renewal:.2f}% of goal-achieving customers "
        f"renewed their subscription."
    )


with col2:

    st.info(
        f"💎 **Completion → Renewal:** "
        f"{completion_to_renewal:.2f}% of completed customers "
        f"renewed their subscription."
    )

    st.warning(
        f"📉 **Renewal Gap After Completion:** "
        f"{completion_renewal_dropoff:,} completed customers "
        f"did not renew."
    )

    st.success(
        f"📊 **Renewed Customers:** "
        f"{renewed_customers:,} customers "
        f"continued their subscription."
    )


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

conn.close()