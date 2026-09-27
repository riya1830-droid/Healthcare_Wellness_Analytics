import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Revenue & Subscription",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Revenue & Subscription Analysis")

st.markdown(
    "Analyze subscription revenue, renewal behavior, subscription duration, "
    "and customer revenue performance."
)

st.divider()


# =========================================================
# MYSQL CONNECTION
# =========================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyNewPassword123!",
    database="patient_analysis"
)


# =========================================================
# SECTION 5.1 — REVENUE KPI OVERVIEW
# =========================================================

st.subheader("💰 Revenue KPI Overview")


kpi_query = """
SELECT

    COUNT(DISTINCT Customer_ID) AS total_subscribers,

    ROUND(
        SUM(Total_Revenue),
        2
    ) AS total_revenue,

    ROUND(
        SUM(Total_Revenue)
        / COUNT(DISTINCT Customer_ID),
        2
    ) AS avg_revenue_per_customer,

    COUNT(
        DISTINCT CASE
            WHEN Renewed = 'Renewed'
            THEN Customer_ID
        END
    ) AS renewed_customers,

    ROUND(
        COUNT(
            DISTINCT CASE
                WHEN Renewed = 'Renewed'
                THEN Customer_ID
            END
        )
        / COUNT(DISTINCT Customer_ID) * 100,
        2
    ) AS renewal_rate,

    ROUND(
        SUM(
            CASE
                WHEN Renewed = 'Renewed'
                THEN Total_Revenue
                ELSE 0
            END
        ),
        2
    ) AS renewal_revenue

FROM subscriptions;
"""


kpi_df = pd.read_sql(
    kpi_query,
    conn
)


# =========================================================
# DYNAMIC KPI VALUES
# =========================================================

total_subscribers = int(
    kpi_df.loc[0, "total_subscribers"]
)

total_revenue = float(
    kpi_df.loc[0, "total_revenue"]
)

avg_revenue = float(
    kpi_df.loc[0, "avg_revenue_per_customer"]
)

renewed_customers = int(
    kpi_df.loc[0, "renewed_customers"]
)

renewal_rate = float(
    kpi_df.loc[0, "renewal_rate"]
)

renewal_revenue = float(
    kpi_df.loc[0, "renewal_revenue"]
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👥 Total Subscribers",
        f"{total_subscribers:,}"
    )


with col2:

    st.metric(
        "💵 Total Revenue",
        f"₹{total_revenue:,.2f}"
    )


with col3:

    st.metric(
        "📊 Avg Revenue / Customer",
        f"₹{avg_revenue:,.2f}"
    )


col4, col5, col6 = st.columns(3)


with col4:

    st.metric(
        "🔄 Renewed Customers",
        f"{renewed_customers:,}"
    )


with col5:

    st.metric(
        "📈 Renewal Rate",
        f"{renewal_rate:.2f}%"
    )


with col6:

    st.metric(
        "💰 Renewal Revenue",
        f"₹{renewal_revenue:,.2f}"
    )


st.divider()


# =========================================================
# SECTION 5.2 — SUBSCRIPTION DURATION ANALYSIS
# =========================================================

st.subheader("⏳ Subscription Duration Analysis")


duration_query = """
SELECT

    Initial_Duration_Months,

    COUNT(DISTINCT Customer_ID) AS customers,

    ROUND(
        SUM(Total_Revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(Total_Revenue),
        2
    ) AS avg_revenue

FROM subscriptions

GROUP BY Initial_Duration_Months

ORDER BY Initial_Duration_Months;
"""


duration_df = pd.read_sql(
    duration_query,
    conn
)


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# CUSTOMERS BY INITIAL DURATION
# ---------------------------------------------------------

with col1:

    fig_duration_customers = px.bar(
        duration_df,
        x="Initial_Duration_Months",
        y="customers",
        text="customers",
        title="Customers by Initial Subscription Duration",
        labels={
            "Initial_Duration_Months": "Initial Duration (Months)",
            "customers": "Customers"
        },
        color="Initial_Duration_Months",
        color_continuous_scale="Turbo"
    )

    fig_duration_customers.update_traces(
        textposition="outside"
    )

    fig_duration_customers.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_duration_customers,
        use_container_width=True
    )


# ---------------------------------------------------------
# REVENUE BY INITIAL DURATION
# ---------------------------------------------------------

with col2:

    fig_duration_revenue = px.bar(
        duration_df,
        x="Initial_Duration_Months",
        y="revenue",
        text="revenue",
        title="Revenue by Initial Subscription Duration",
        labels={
            "Initial_Duration_Months": "Initial Duration (Months)",
            "revenue": "Revenue (₹)"
        },
        color="Initial_Duration_Months",
        color_continuous_scale="Viridis"
    )

    fig_duration_revenue.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig_duration_revenue.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_duration_revenue,
        use_container_width=True
    )


st.divider()


# =========================================================
# SECTION 5.3 — RENEWAL ANALYSIS
# =========================================================

st.subheader("🔄 Renewal Analysis")


renewal_query = """
SELECT

    Renewed AS renewal_status,

    COUNT(DISTINCT Customer_ID) AS customers,

    ROUND(
        SUM(Total_Revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(Total_Revenue),
        2
    ) AS avg_revenue

FROM subscriptions

GROUP BY Renewed

ORDER BY customers DESC;
"""


renewal_df = pd.read_sql(
    renewal_query,
    conn
)


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# CUSTOMER RENEWAL STATUS
# ---------------------------------------------------------

with col1:

    fig_renewal_customers = px.pie(
        renewal_df,
        names="renewal_status",
        values="customers",
        hole=0.55,
        title="Customer Renewal Status",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_renewal_customers.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_renewal_customers,
        use_container_width=True
    )


# ---------------------------------------------------------
# REVENUE BY RENEWAL STATUS
# ---------------------------------------------------------

with col2:

    fig_renewal_revenue = px.bar(
        renewal_df,
        x="renewal_status",
        y="revenue",
        text="revenue",
        title="Revenue by Renewal Status",
        labels={
            "renewal_status": "Renewal Status",
            "revenue": "Revenue (₹)"
        },
        color="renewal_status",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig_renewal_revenue.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig_renewal_revenue,
        use_container_width=True
    )


st.divider()


# =========================================================
# SECTION 5.4 — RENEWAL DURATION ANALYSIS
# =========================================================

st.subheader("📅 Renewal Duration Analysis")


renewal_duration_query = """
SELECT

    Renewal_Months,

    COUNT(DISTINCT Customer_ID) AS renewed_customers,

    ROUND(
        SUM(Total_Revenue),
        2
    ) AS revenue,

    ROUND(
        AVG(Total_Revenue),
        2
    ) AS avg_revenue

FROM subscriptions

WHERE Renewed = 'Renewed'

GROUP BY Renewal_Months

ORDER BY Renewal_Months;
"""


renewal_duration_df = pd.read_sql(
    renewal_duration_query,
    conn
)


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# RENEWED CUSTOMERS BY RENEWAL DURATION
# ---------------------------------------------------------

with col1:

    fig_renewal_duration = px.bar(
        renewal_duration_df,
        x="Renewal_Months",
        y="renewed_customers",
        text="renewed_customers",
        title="Renewed Customers by Renewal Duration",
        labels={
            "Renewal_Months": "Renewal Duration (Months)",
            "renewed_customers": "Renewed Customers"
        },
        color="Renewal_Months",
        color_continuous_scale="Plasma"
    )

    fig_renewal_duration.update_traces(
        textposition="outside"
    )

    fig_renewal_duration.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_renewal_duration,
        use_container_width=True
    )


# ---------------------------------------------------------
# REVENUE BY RENEWAL DURATION
# ---------------------------------------------------------

with col2:

    fig_renewal_duration_revenue = px.bar(
        renewal_duration_df,
        x="Renewal_Months",
        y="revenue",
        text="revenue",
        title="Revenue by Renewal Duration",
        labels={
            "Renewal_Months": "Renewal Duration (Months)",
            "revenue": "Revenue (₹)"
        },
        color="Renewal_Months",
        color_continuous_scale="Cividis"
    )

    fig_renewal_duration_revenue.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside"
    )

    fig_renewal_duration_revenue.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_renewal_duration_revenue,
        use_container_width=True
    )


st.divider()


# =========================================================
# SECTION 5.5 — REVENUE DISTRIBUTION
# =========================================================

st.subheader("📊 Revenue Distribution")


revenue_distribution_query = """
SELECT

    CASE

        WHEN Total_Revenue < 5000
            THEN 'Below ₹5K'

        WHEN Total_Revenue < 10000
            THEN '₹5K - ₹10K'

        WHEN Total_Revenue < 20000
            THEN '₹10K - ₹20K'

        ELSE '₹20K+'

    END AS revenue_bucket,

    COUNT(DISTINCT Customer_ID) AS customers,

    ROUND(
        SUM(Total_Revenue),
        2
    ) AS revenue

FROM subscriptions

GROUP BY

    CASE

        WHEN Total_Revenue < 5000
            THEN 'Below ₹5K'

        WHEN Total_Revenue < 10000
            THEN '₹5K - ₹10K'

        WHEN Total_Revenue < 20000
            THEN '₹10K - ₹20K'

        ELSE '₹20K+'

    END

ORDER BY MIN(Total_Revenue);
"""


revenue_distribution_df = pd.read_sql(
    revenue_distribution_query,
    conn
)


fig_revenue_distribution = px.bar(
    revenue_distribution_df,
    x="revenue_bucket",
    y="customers",
    text="customers",
    title="Customers by Revenue Contribution",
    labels={
        "revenue_bucket": "Revenue Range",
        "customers": "Customers"
    },
    color="revenue_bucket",
    color_discrete_sequence=px.colors.qualitative.Safe
)

fig_revenue_distribution.update_traces(
    textposition="outside"
)

fig_revenue_distribution.update_layout(
    showlegend=False
)

st.plotly_chart(
    fig_revenue_distribution,
    use_container_width=True
)


st.divider()


# =========================================================
# SECTION 5.6 — TOP CUSTOMER REVENUE ANALYSIS
# =========================================================

st.subheader("👤 Top Customer Revenue Analysis")


customer_revenue_query = """
SELECT

    Customer_ID,

    Initial_Duration_Months,

    Renewal_Months,

    Renewed,

    ROUND(
        Total_Revenue,
        2
    ) AS Total_Revenue

FROM subscriptions

ORDER BY Total_Revenue DESC

LIMIT 10;
"""


customer_revenue_df = pd.read_sql(
    customer_revenue_query,
    conn
)


st.dataframe(
    customer_revenue_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# SECTION 5.7 — REVENUE & SUBSCRIPTION INSIGHTS
# =========================================================

st.subheader("💡 Revenue & Subscription Insights")


# ---------------------------------------------------------
# INSIGHT 1 — MOST POPULAR INITIAL DURATION
# ---------------------------------------------------------

highest_duration_query = """
SELECT
    Initial_Duration_Months,
    COUNT(DISTINCT Customer_ID) AS customers
FROM subscriptions
GROUP BY Initial_Duration_Months
ORDER BY customers DESC
LIMIT 1;
"""

highest_duration_df = pd.read_sql(
    highest_duration_query,
    conn
)

highest_duration = int(
    highest_duration_df.loc[0, "Initial_Duration_Months"]
)


# ---------------------------------------------------------
# INSIGHT 2 — HIGHEST REVENUE INITIAL DURATION
# ---------------------------------------------------------

highest_revenue_duration_query = """
SELECT
    Initial_Duration_Months,
    SUM(Total_Revenue) AS revenue
FROM subscriptions
GROUP BY Initial_Duration_Months
ORDER BY revenue DESC
LIMIT 1;
"""

highest_revenue_duration_df = pd.read_sql(
    highest_revenue_duration_query,
    conn
)

highest_revenue_duration = int(
    highest_revenue_duration_df.loc[
        0,
        "Initial_Duration_Months"
    ]
)


# ---------------------------------------------------------
# INSIGHT 3 — HIGHEST REVENUE CUSTOMER SEGMENT
# ---------------------------------------------------------

highest_revenue_bucket_query = """
SELECT
    CASE
        WHEN Total_Revenue < 5000
            THEN 'Below ₹5K'

        WHEN Total_Revenue < 10000
            THEN '₹5K - ₹10K'

        WHEN Total_Revenue < 20000
            THEN '₹10K - ₹20K'

        ELSE '₹20K+'
    END AS revenue_bucket,

    SUM(Total_Revenue) AS revenue

FROM subscriptions

GROUP BY
    CASE
        WHEN Total_Revenue < 5000
            THEN 'Below ₹5K'

        WHEN Total_Revenue < 10000
            THEN '₹5K - ₹10K'

        WHEN Total_Revenue < 20000
            THEN '₹10K - ₹20K'

        ELSE '₹20K+'
    END

ORDER BY revenue DESC

LIMIT 1;
"""

highest_revenue_bucket_df = pd.read_sql(
    highest_revenue_bucket_query,
    conn
)

highest_revenue_bucket = str(
    highest_revenue_bucket_df.loc[
        0,
        "revenue_bucket"
    ]
)


# =========================================================
# DISPLAY INSIGHTS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.info(
        f"""
        📅 **Popular Subscription Duration**

        The **{highest_duration}-month** subscription duration
        has the highest number of customers.
        """
    )


with col2:

    st.info(
        f"""
        💰 **Revenue Leader**

        The **{highest_revenue_duration}-month** initial duration
        generates the highest total revenue.
        """
    )


with col3:

    st.info(
        f"""
        💵 **Revenue Contribution**

        The **{highest_revenue_bucket}** customer segment
        contributes the highest total revenue.
        """
    )


st.divider()


# =========================================================
# BUSINESS SUMMARY
# =========================================================

st.subheader("📌 Business Summary")


st.success(
    f"""
    **The platform generated a total revenue of ₹{total_revenue:,.2f}
    across {total_subscribers:,} subscribers.**

    The average revenue per customer is **₹{avg_revenue:,.2f}**,
    while **{renewed_customers:,} customers** renewed their
    subscriptions, resulting in a renewal rate of
    **{renewal_rate:.2f}%**.

    Subscription duration and renewal behavior can be used
    to identify customer segments contributing more strongly
    to recurring revenue.
    """
)


# =========================================================
# CLOSE MYSQL CONNECTION
# =========================================================

conn.close()