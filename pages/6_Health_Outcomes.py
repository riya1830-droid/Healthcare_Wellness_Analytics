import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Health Outcomes",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ Health Outcomes Analysis")

st.markdown(
    "Analyze customer health measurements, weight changes, "
    "BMI improvements, and overall health outcomes."
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
# SECTION 6.1 — HEALTH OUTCOME KPI OVERVIEW
# =========================================================

st.subheader("❤️ Health Outcome KPI Overview")


kpi_query = """
WITH first_measurement AS (

    SELECT
        Customer_ID,
        Weight_kg AS initial_weight,
        BMI AS initial_bmi

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MIN(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
),

latest_measurement AS (

    SELECT
        Customer_ID,
        Weight_kg AS latest_weight,
        BMI AS latest_bmi

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MAX(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
)

SELECT

    COUNT(*) AS measured_customers,

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

FROM first_measurement f

JOIN latest_measurement l
    ON f.Customer_ID = l.Customer_ID;
"""


kpi_df = pd.read_sql(
    kpi_query,
    conn
)


# =========================================================
# DYNAMIC KPI VALUES
# =========================================================

measured_customers = int(
    kpi_df.loc[0, "measured_customers"]
)

avg_initial_weight = float(
    kpi_df.loc[0, "avg_initial_weight"]
)

avg_latest_weight = float(
    kpi_df.loc[0, "avg_latest_weight"]
)

avg_weight_change = float(
    kpi_df.loc[0, "avg_weight_change"]
)

avg_initial_bmi = float(
    kpi_df.loc[0, "avg_initial_bmi"]
)

avg_latest_bmi = float(
    kpi_df.loc[0, "avg_latest_bmi"]
)

avg_bmi_change = float(
    kpi_df.loc[0, "avg_bmi_change"]
)


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👥 Measured Customers",
        f"{measured_customers:,}"
    )


with col2:

    st.metric(
        "⚖️ Avg Initial Weight",
        f"{avg_initial_weight:.2f} kg"
    )


with col3:

    st.metric(
        "⚖️ Avg Latest Weight",
        f"{avg_latest_weight:.2f} kg"
    )


col4, col5, col6 = st.columns(3)


with col4:

    st.metric(
        "📉 Avg Weight Change",
        f"{avg_weight_change:.2f} kg"
    )


with col5:

    st.metric(
        "🧮 Avg Initial BMI",
        f"{avg_initial_bmi:.2f}"
    )


with col6:

    st.metric(
        "📊 Avg Latest BMI",
        f"{avg_latest_bmi:.2f}"
    )


st.divider()


# =========================================================
# SECTION 6.2 — WEIGHT & BMI ANALYSIS
# =========================================================

st.subheader("⚖️ Weight & BMI Analysis")


comparison_df = pd.DataFrame({
    "Metric": [
        "Average Weight",
        "Average BMI"
    ],
    "Initial": [
        avg_initial_weight,
        avg_initial_bmi
    ],
    "Latest": [
        avg_latest_weight,
        avg_latest_bmi
    ]
})


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# WEIGHT COMPARISON
# ---------------------------------------------------------

with col1:

    weight_comparison = pd.DataFrame({
        "Stage": [
            "Initial",
            "Latest"
        ],
        "Weight_kg": [
            avg_initial_weight,
            avg_latest_weight
        ]
    })

    fig_weight = px.bar(
        weight_comparison,
        x="Stage",
        y="Weight_kg",
        text="Weight_kg",
        title="Average Weight: Initial vs Latest",
        labels={
            "Weight_kg": "Weight (kg)"
        },
        color="Stage",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_weight.update_traces(
        texttemplate="%{text:.2f} kg",
        textposition="outside"
    )

    fig_weight.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_weight,
        use_container_width=True
    )


# ---------------------------------------------------------
# BMI COMPARISON
# ---------------------------------------------------------

with col2:

    bmi_comparison = pd.DataFrame({
        "Stage": [
            "Initial",
            "Latest"
        ],
        "BMI": [
            avg_initial_bmi,
            avg_latest_bmi
        ]
    })

    fig_bmi = px.bar(
        bmi_comparison,
        x="Stage",
        y="BMI",
        text="BMI",
        title="Average BMI: Initial vs Latest",
        labels={
            "BMI": "BMI"
        },
        color="Stage",
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig_bmi.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_bmi.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_bmi,
        use_container_width=True
    )


st.divider()


# =========================================================
# SECTION 6.3 — WEIGHT CHANGE DISTRIBUTION
# =========================================================

st.subheader("📉 Weight Change Distribution")


weight_change_query = """
WITH first_measurement AS (

    SELECT
        Customer_ID,
        Weight_kg AS initial_weight

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MIN(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
),

latest_measurement AS (

    SELECT
        Customer_ID,
        Weight_kg AS latest_weight

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MAX(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
)

SELECT

    CASE

        WHEN latest_weight - initial_weight < -10
            THEN 'Weight Loss > 10 kg'

        WHEN latest_weight - initial_weight < -5
            THEN 'Weight Loss 5–10 kg'

        WHEN latest_weight - initial_weight < 0
            THEN 'Weight Loss < 5 kg'

        WHEN latest_weight - initial_weight = 0
            THEN 'No Change'

        WHEN latest_weight - initial_weight <= 5
            THEN 'Weight Gain ≤ 5 kg'

        ELSE 'Weight Gain > 5 kg'

    END AS weight_change_category,

    COUNT(*) AS customers

FROM first_measurement f

JOIN latest_measurement l
    ON f.Customer_ID = l.Customer_ID

GROUP BY

    CASE

        WHEN latest_weight - initial_weight < -10
            THEN 'Weight Loss > 10 kg'

        WHEN latest_weight - initial_weight < -5
            THEN 'Weight Loss 5–10 kg'

        WHEN latest_weight - initial_weight < 0
            THEN 'Weight Loss < 5 kg'

        WHEN latest_weight - initial_weight = 0
            THEN 'No Change'

        WHEN latest_weight - initial_weight <= 5
            THEN 'Weight Gain ≤ 5 kg'

        ELSE 'Weight Gain > 5 kg'

    END

ORDER BY MIN(
    latest_weight - initial_weight
);
"""


weight_change_df = pd.read_sql(
    weight_change_query,
    conn
)


fig_weight_change = px.bar(
    weight_change_df,
    x="weight_change_category",
    y="customers",
    text="customers",
    title="Customers by Weight Change",
    labels={
        "weight_change_category": "Weight Change",
        "customers": "Customers"
    },
    color="weight_change_category",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_weight_change.update_traces(
    textposition="outside"
)

fig_weight_change.update_layout(
    showlegend=False
)

st.plotly_chart(
    fig_weight_change,
    use_container_width=True
)


st.divider()


# =========================================================
# SECTION 6.4 — BMI IMPROVEMENT ANALYSIS
# =========================================================

st.subheader("🧮 BMI Improvement Analysis")


bmi_change_query = """
WITH first_measurement AS (

    SELECT
        Customer_ID,
        BMI AS initial_bmi

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MIN(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
),

latest_measurement AS (

    SELECT
        Customer_ID,
        BMI AS latest_bmi

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MAX(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
)

SELECT

    CASE

        WHEN latest_bmi < initial_bmi
            THEN 'BMI Improved'

        WHEN latest_bmi = initial_bmi
            THEN 'No BMI Change'

        ELSE 'BMI Increased'

    END AS bmi_outcome,

    COUNT(*) AS customers

FROM first_measurement f

JOIN latest_measurement l
    ON f.Customer_ID = l.Customer_ID

GROUP BY

    CASE

        WHEN latest_bmi < initial_bmi
            THEN 'BMI Improved'

        WHEN latest_bmi = initial_bmi
            THEN 'No BMI Change'

        ELSE 'BMI Increased'

    END

ORDER BY customers DESC;
"""


bmi_change_df = pd.read_sql(
    bmi_change_query,
    conn
)


col1, col2 = st.columns(2)


# ---------------------------------------------------------
# BMI OUTCOME DISTRIBUTION
# ---------------------------------------------------------

with col1:

    fig_bmi_outcome = px.pie(
        bmi_change_df,
        names="bmi_outcome",
        values="customers",
        hole=0.55,
        title="BMI Outcome Distribution",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_bmi_outcome.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_bmi_outcome,
        use_container_width=True
    )


# ---------------------------------------------------------
# BMI OUTCOME BAR
# ---------------------------------------------------------

with col2:

    fig_bmi_outcome_bar = px.bar(
        bmi_change_df,
        x="bmi_outcome",
        y="customers",
        text="customers",
        title="Customers by BMI Outcome",
        labels={
            "bmi_outcome": "BMI Outcome",
            "customers": "Customers"
        },
        color="bmi_outcome",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig_bmi_outcome_bar.update_traces(
        textposition="outside"
    )

    fig_bmi_outcome_bar.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_bmi_outcome_bar,
        use_container_width=True
    )


st.divider()


# =========================================================
# SECTION 6.5 — HEALTH OUTCOME SEGMENTATION
# =========================================================

st.subheader("🎯 Health Outcome Segmentation")


health_segment_query = """
WITH first_measurement AS (

    SELECT
        Customer_ID,
        Weight_kg AS initial_weight,
        BMI AS initial_bmi

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MIN(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
),

latest_measurement AS (

    SELECT
        Customer_ID,
        Weight_kg AS latest_weight,
        BMI AS latest_bmi

    FROM health_measurements

    WHERE Measurement_Date = (
        SELECT MAX(h2.Measurement_Date)
        FROM health_measurements h2
        WHERE h2.Customer_ID = health_measurements.Customer_ID
    )
)

SELECT

    CASE

        WHEN latest_weight < initial_weight
             AND latest_bmi < initial_bmi
            THEN 'Weight & BMI Improved'

        WHEN latest_weight < initial_weight
            THEN 'Weight Improved Only'

        WHEN latest_bmi < initial_bmi
            THEN 'BMI Improved Only'

        WHEN latest_weight = initial_weight
             AND latest_bmi = initial_bmi
            THEN 'No Change'

        ELSE 'Weight & BMI Increased'

    END AS health_outcome,

    COUNT(*) AS customers

FROM first_measurement f

JOIN latest_measurement l
    ON f.Customer_ID = l.Customer_ID

GROUP BY

    CASE

        WHEN latest_weight < initial_weight
             AND latest_bmi < initial_bmi
            THEN 'Weight & BMI Improved'

        WHEN latest_weight < initial_weight
            THEN 'Weight Improved Only'

        WHEN latest_bmi < initial_bmi
            THEN 'BMI Improved Only'

        WHEN latest_weight = initial_weight
             AND latest_bmi = initial_bmi
            THEN 'No Change'

        ELSE 'Weight & BMI Increased'

    END

ORDER BY customers DESC;
"""


health_segment_df = pd.read_sql(
    health_segment_query,
    conn
)


fig_health_segment = px.bar(
    health_segment_df,
    x="health_outcome",
    y="customers",
    text="customers",
    title="Customer Health Outcome Segments",
    labels={
        "health_outcome": "Health Outcome",
        "customers": "Customers"
    },
    color="health_outcome",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_health_segment.update_traces(
    textposition="outside"
)

fig_health_segment.update_layout(
    showlegend=False
)

st.plotly_chart(
    fig_health_segment,
    use_container_width=True
)


st.divider()


# =========================================================
# SECTION 6.6 — HEALTH OUTCOMES INSIGHTS
# =========================================================

st.subheader("💡 Health Outcomes Insights")


# ---------------------------------------------------------
# INSIGHT 1 — AVERAGE WEIGHT CHANGE
# ---------------------------------------------------------

if avg_weight_change < 0:

    weight_message = (
        f"Average customer weight decreased by "
        f"{abs(avg_weight_change):.2f} kg."
    )

elif avg_weight_change > 0:

    weight_message = (
        f"Average customer weight increased by "
        f"{avg_weight_change:.2f} kg."
    )

else:

    weight_message = (
        "Average customer weight remained unchanged."
    )


# ---------------------------------------------------------
# INSIGHT 2 — AVERAGE BMI CHANGE
# ---------------------------------------------------------

if avg_bmi_change < 0:

    bmi_message = (
        f"Average BMI decreased by "
        f"{abs(avg_bmi_change):.2f} points."
    )

elif avg_bmi_change > 0:

    bmi_message = (
        f"Average BMI increased by "
        f"{avg_bmi_change:.2f} points."
    )

else:

    bmi_message = (
        "Average BMI remained unchanged."
    )


# ---------------------------------------------------------
# INSIGHT 3 — LARGEST HEALTH SEGMENT
# ---------------------------------------------------------

largest_segment = str(
    health_segment_df.loc[
        health_segment_df["customers"].idxmax(),
        "health_outcome"
    ]
)

largest_segment_customers = int(
    health_segment_df["customers"].max()
)


# ---------------------------------------------------------
# INSIGHT CARDS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.info(
        f"""
        ⚖️ **Weight Outcome**

        {weight_message}
        """
    )


with col2:

    st.info(
        f"""
        🧮 **BMI Outcome**

        {bmi_message}
        """
    )


with col3:

    st.info(
        f"""
        🎯 **Largest Outcome Segment**

        **{largest_segment}** represents the largest
        customer health outcome segment with
        **{largest_segment_customers:,} customers**.
        """
    )


st.divider()


# =========================================================
# FINAL BUSINESS SUMMARY
# =========================================================

st.subheader("📌 Business Summary")


st.success(
    f"""
    **Health measurements were available for
    {measured_customers:,} customers.**

    Average weight changed from **{avg_initial_weight:.2f} kg**
    initially to **{avg_latest_weight:.2f} kg** in the latest
    recorded measurement.

    Average BMI changed from **{avg_initial_bmi:.2f}**
    to **{avg_latest_bmi:.2f}**.

    These before-and-after health measurements help evaluate
    measurable customer outcomes and provide an additional
    perspective on program effectiveness beyond completion,
    goal achievement, and subscription renewal.
    """
)


# =========================================================
# CLOSE MYSQL CONNECTION
# =========================================================

conn.close()