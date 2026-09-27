import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📌",
    layout="wide"
)

st.title("📌 Executive Summary")

st.markdown(
    "A concise overview of key customer, program, retention, revenue, "
    "feedback, and health outcome insights from the Healthcare & Wellness Analytics project."
)

st.divider()

# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MyNewPassword123!",
    database="patient_analysis"
)

# ============================================================
# 1. EXECUTIVE KPI OVERVIEW
# ============================================================

kpi_query = """
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

    (SELECT ROUND(SUM(Total_Revenue), 2)
     FROM subscriptions) AS total_revenue,

    (SELECT ROUND(AVG(BMI), 2)
     FROM health_measurements) AS average_bmi
"""

kpi_df = pd.read_sql(kpi_query, conn)

total_customers = int(kpi_df.loc[0, "total_customers"])
consulted_customers = int(kpi_df.loc[0, "consulted_customers"])
enrolled_customers = int(kpi_df.loc[0, "enrolled_customers"])
completed_customers = int(kpi_df.loc[0, "completed_customers"])
goal_achieved_customers = int(kpi_df.loc[0, "goal_achieved_customers"])
renewed_customers = int(kpi_df.loc[0, "renewed_customers"])
total_revenue = float(kpi_df.loc[0, "total_revenue"])
average_bmi = float(kpi_df.loc[0, "average_bmi"])


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Customers", f"{total_customers:,}")

with col2:
    st.metric("📋 Consulted", f"{consulted_customers:,}")

with col3:
    st.metric("📚 Enrolled", f"{enrolled_customers:,}")

with col4:
    st.metric("✅ Completed", f"{completed_customers:,}")


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric("🎯 Goals Achieved", f"{goal_achieved_customers:,}")

with col6:
    st.metric("🔄 Renewed", f"{renewed_customers:,}")

with col7:
    st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")

with col8:
    st.metric("⭐ Avg BMI", f"{average_bmi:.2f}")

st.divider()


# ============================================================
# 2. CUSTOMER JOURNEY SUMMARY
# ============================================================

st.subheader("🚶 Customer Journey Summary")

journey_query = """
SELECT
    ROUND(
        COUNT(DISTINCT CASE
            WHEN Program_Completed = 'Yes'
            THEN Customer_ID
        END)
        /
        COUNT(DISTINCT Customer_ID) * 100,
        2
    ) AS completion_rate,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN Goal_Achieved = 'Yes'
            THEN Customer_ID
        END)
        /
        COUNT(DISTINCT CASE
            WHEN Program_Completed = 'Yes'
            THEN Customer_ID
        END) * 100,
        2
    ) AS goal_achievement_rate

FROM programs;
"""

journey_df = pd.read_sql(journey_query, conn)

completion_rate = float(
    journey_df.loc[0, "completion_rate"]
)

goal_achievement_rate = float(
    journey_df.loc[0, "goal_achievement_rate"]
)


renewal_query = """
SELECT
    ROUND(
        COUNT(DISTINCT CASE
            WHEN Renewed = 'Renewed'
            THEN Customer_ID
        END)
        /
        COUNT(DISTINCT Customer_ID) * 100,
        2
    ) AS renewal_rate
FROM subscriptions;
"""

renewal_df = pd.read_sql(renewal_query, conn)

renewal_rate = float(
    renewal_df.loc[0, "renewal_rate"]
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📈 Completion Rate",
        f"{completion_rate:.2f}%"
    )

with col2:
    st.metric(
        "🎯 Goal Achievement",
        f"{goal_achievement_rate:.2f}%"
    )

with col3:
    st.metric(
        "🔄 Renewal Rate",
        f"{renewal_rate:.2f}%"
    )

st.divider()


# ============================================================
# 3. CUSTOMER FEEDBACK SUMMARY
# ============================================================

st.subheader("⭐ Customer Feedback Summary")

feedback_query = """
SELECT
    COUNT(*) AS total_feedback,

    ROUND(
        AVG(Rating),
        2
    ) AS average_rating,

    COUNT(
        CASE
            WHEN Rating >= 4 THEN 1
        END
    ) AS positive_feedback,

    ROUND(
        COUNT(
            CASE
                WHEN Rating >= 4 THEN 1
            END
        )
        / COUNT(*) * 100,
        2
    ) AS positive_feedback_rate

FROM feedback;
"""

feedback_df = pd.read_sql(feedback_query, conn)

total_feedback = int(
    feedback_df.loc[0, "total_feedback"]
)

average_rating = float(
    feedback_df.loc[0, "average_rating"]
)

positive_feedback = int(
    feedback_df.loc[0, "positive_feedback"]
)

positive_feedback_rate = float(
    feedback_df.loc[0, "positive_feedback_rate"]
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💬 Total Feedback",
        f"{total_feedback:,}"
    )

with col2:
    st.metric(
        "⭐ Average Rating",
        f"{average_rating:.2f}/5"
    )

with col3:
    st.metric(
        "👍 Positive Feedback",
        f"{positive_feedback:,}"
    )

with col4:
    st.metric(
        "📈 Positive Feedback Rate",
        f"{positive_feedback_rate:.2f}%"
    )


st.info(
    f"""
    💡 **Feedback Insight**

    Customers provided an average rating of **{average_rating:.2f}/5**,
    with **{positive_feedback_rate:.2f}%** of feedback records receiving
    a rating of 4 or 5.
    """
)

st.divider()


# ============================================================
# 4. HEALTH OUTCOME SUMMARY
# ============================================================

st.subheader("⚖️ Health Outcome Summary")

health_query = """
WITH ranked_measurements AS (

    SELECT
        Customer_ID,
        Weight_kg,
        BMI,
        Measurement_Date,

        ROW_NUMBER() OVER (
            PARTITION BY Customer_ID
            ORDER BY Measurement_Date, Measurement_ID
        ) AS first_rank,

        ROW_NUMBER() OVER (
            PARTITION BY Customer_ID
            ORDER BY Measurement_Date DESC, Measurement_ID DESC
        ) AS latest_rank

    FROM health_measurements
),

customer_outcomes AS (

    SELECT
        Customer_ID,

        MAX(
            CASE
                WHEN first_rank = 1
                THEN Weight_kg
            END
        ) AS initial_weight,

        MAX(
            CASE
                WHEN latest_rank = 1
                THEN Weight_kg
            END
        ) AS latest_weight,

        MAX(
            CASE
                WHEN first_rank = 1
                THEN BMI
            END
        ) AS initial_bmi,

        MAX(
            CASE
                WHEN latest_rank = 1
                THEN BMI
            END
        ) AS latest_bmi

    FROM ranked_measurements

    GROUP BY Customer_ID
)

SELECT

    ROUND(
        AVG(initial_weight),
        2
    ) AS avg_initial_weight,

    ROUND(
        AVG(latest_weight),
        2
    ) AS avg_latest_weight,

    ROUND(
        AVG(latest_weight - initial_weight),
        2
    ) AS avg_weight_change,

    ROUND(
        AVG(initial_bmi),
        2
    ) AS avg_initial_bmi,

    ROUND(
        AVG(latest_bmi),
        2
    ) AS avg_latest_bmi,

    ROUND(
        AVG(latest_bmi - initial_bmi),
        2
    ) AS avg_bmi_change

FROM customer_outcomes;
"""

health_df = pd.read_sql(
    health_query,
    conn
)

avg_initial_weight = float(
    health_df.loc[0, "avg_initial_weight"]
)

avg_latest_weight = float(
    health_df.loc[0, "avg_latest_weight"]
)

avg_weight_change = float(
    health_df.loc[0, "avg_weight_change"]
)

avg_initial_bmi = float(
    health_df.loc[0, "avg_initial_bmi"]
)

avg_latest_bmi = float(
    health_df.loc[0, "avg_latest_bmi"]
)

avg_bmi_change = float(
    health_df.loc[0, "avg_bmi_change"]
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⚖️ Avg Initial Weight",
        f"{avg_initial_weight:.2f} kg"
    )

with col2:
    st.metric(
        "⚖️ Avg Latest Weight",
        f"{avg_latest_weight:.2f} kg"
    )

with col3:
    st.metric(
        "📉 Avg Weight Change",
        f"{avg_weight_change:.2f} kg"
    )


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🧮 Avg Initial BMI",
        f"{avg_initial_bmi:.2f}"
    )

with col2:
    st.metric(
        "🧮 Avg Latest BMI",
        f"{avg_latest_bmi:.2f}"
    )

with col3:
    st.metric(
        "📉 Avg BMI Change",
        f"{avg_bmi_change:.2f}"
    )

st.divider()


# ============================================================
# 5. KEY BUSINESS INSIGHTS
# ============================================================

st.subheader("💡 Key Business Insights")

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
        🚶 **Customer Journey**

        **{completion_rate:.2f}%** of enrolled customers completed
        their programs, while **{goal_achievement_rate:.2f}%**
        of completed customers achieved their goals.
        """
    )

    st.info(
        f"""
        🔄 **Customer Retention**

        The overall subscription renewal rate is
        **{renewal_rate:.2f}%**, representing the proportion
        of customers who renewed their subscriptions.
        """
    )


with col2:

    st.warning(
        f"""
        ⚖️ **Health Outcomes**

        Customers showed an average weight change of
        **{avg_weight_change:.2f} kg** and an average BMI change
        of **{avg_bmi_change:.2f} points** between their initial
        and latest recorded measurements.
        """
    )

    st.info(
        f"""
        ⭐ **Customer Feedback**

        The dataset contains **{total_feedback:,} feedback records**
        with an average rating of **{average_rating:.2f}/5**.
        **{positive_feedback_rate:.2f}%** received ratings of 4 or 5.
        """
    )

st.divider()


# ============================================================
# 6. BUSINESS RECOMMENDATIONS
# ============================================================

st.subheader("🎯 Business Recommendations")

col1, col2 = st.columns(2)

with col1:

    st.success(
        """
        📈 **Improve Program Completion**

        Focus on reducing drop-offs during the program journey
        through regular progress tracking, timely follow-ups,
        and personalized customer support.
        """
    )

    st.info(
        """
        🔄 **Strengthen Customer Retention**

        Engage customers before subscription expiry and use
        goal-achievement and program-progress signals to support
        timely renewal communication.
        """
    )

    st.warning(
        """
        🏆 **Focus on High-Performing Programs**

        Identify programs with stronger completion and goal
        achievement rates and study their characteristics
        for potential improvement of lower-performing programs.
        """
    )

with col2:

    st.info(
        """
        📊 **Use Adherence Tracking**

        Monitor customer adherence throughout the program and
        identify customers showing lower engagement so that
        support can be provided earlier.
        """
    )

    st.success(
        """
        ⭐ **Use Customer Feedback**

        Track customer ratings and feedback to identify areas
        affecting customer experience and support service
        improvement.
        """
    )

    st.warning(
        """
        ⚖️ **Monitor Health Outcomes**

        Track changes in weight and BMI alongside program
        engagement, completion, and retention metrics to obtain
        a broader view of customer outcomes.
        """
    )

st.divider()


# ============================================================
# 7. PROJECT SUMMARY
# ============================================================

st.subheader("📌 Project Summary")

st.markdown(
    """
    This project analyzes a synthetic healthcare and wellness
    customer journey using **MySQL, Python, Pandas, Plotly,
    and Streamlit**.

    The analysis covers:

    - Customer journey and funnel performance
    - Consultation effectiveness
    - Program performance
    - Customer feedback
    - Program completion and goal achievement
    - Customer retention and subscription renewal
    - Revenue and subscription behavior
    - Health outcomes
    - Advanced customer segmentation and SQL insights

    The dashboard uses SQL-driven calculations to provide
    dynamic business metrics, insights, and recommendations.
    """
)

conn.close()