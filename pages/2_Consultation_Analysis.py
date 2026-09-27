import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Consultation Analysis",
    page_icon="🩺",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🩺 Consultation Analysis")
st.subheader("Consultation Performance & Customer Engagement")


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
# 1. CONSULTATION KPI ANALYSIS
# ============================================================

kpi_query = """
SELECT
    COUNT(*) AS total_consultations,

    COUNT(
        CASE
            WHEN Status = 'Completed' THEN 1
        END
    ) AS completed_consultations,

    COUNT(DISTINCT Customer_ID) AS consulted_customers,

    ROUND(
        COUNT(
            CASE
                WHEN Status = 'Completed' THEN 1
            END
        ) / COUNT(*) * 100,
        2
    ) AS completion_rate

FROM consultations;
"""

kpi = pd.read_sql(kpi_query, conn)


# ============================================================
# EXTRACT KPI VALUES
# ============================================================

total_consultations = int(
    kpi.iloc[0]["total_consultations"]
)

completed_consultations = int(
    kpi.iloc[0]["completed_consultations"]
)

consulted_customers = int(
    kpi.iloc[0]["consulted_customers"]
)

completion_rate = kpi.iloc[0]["completion_rate"]


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🩺 Total Consultations",
        f"{total_consultations:,}"
    )

with col2:
    st.metric(
        "✅ Completed Consultations",
        f"{completed_consultations:,}"
    )

with col3:
    st.metric(
        "👥 Customers Consulted",
        f"{consulted_customers:,}"
    )

with col4:
    st.metric(
        "📈 Completion Rate",
        f"{completion_rate:.2f}%"
    )


# ============================================================
# 2. CONSULTATION TYPE PERFORMANCE
# ============================================================

st.markdown("---")
st.subheader("📋 Consultation Type Performance")


type_query = """
SELECT
    Consultation_Type,

    COUNT(*) AS total_consultations,

    COUNT(
        CASE
            WHEN Status = 'Completed' THEN 1
        END
    ) AS completed_consultations,

    ROUND(
        COUNT(
            CASE
                WHEN Status = 'Completed' THEN 1
            END
        ) / COUNT(*) * 100,
        2
    ) AS completion_rate

FROM consultations

GROUP BY Consultation_Type

ORDER BY completion_rate DESC;
"""

type_data = pd.read_sql(
    type_query,
    conn
)


# ============================================================
# CONSULTATION TYPE TABLE
# ============================================================

st.dataframe(
    type_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CONSULTATION TYPE COLORFUL CHART
# ============================================================

fig_type = px.bar(
    type_data,
    x="Consultation_Type",
    y="completion_rate",
    text="completion_rate",
    title="Consultation Completion Rate by Type",
    color="Consultation_Type",
    color_discrete_sequence=px.colors.qualitative.Bold
)

fig_type.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_type.update_layout(
    yaxis_title="Completion Rate (%)",
    xaxis_title="Consultation Type",
    height=450,
    showlegend=False
)

st.plotly_chart(
    fig_type,
    use_container_width=True
)


# ============================================================
# 3. CONSULTATION MODE PERFORMANCE
# ============================================================

st.markdown("---")
st.subheader("💻 Consultation Mode Performance")


mode_query = """
SELECT
    CASE
        WHEN Mode IN ('Online', 'Phone')
            THEN 'Remote / Online'

        WHEN Mode = 'In-Person'
            THEN 'In-Person'

        ELSE Mode
    END AS consultation_mode,

    COUNT(*) AS total_consultations,

    COUNT(
        CASE
            WHEN Status = 'Completed' THEN 1
        END
    ) AS completed_consultations,

    ROUND(
        COUNT(
            CASE
                WHEN Status = 'Completed' THEN 1
            END
        ) / COUNT(*) * 100,
        2
    ) AS completion_rate

FROM consultations

GROUP BY
    CASE
        WHEN Mode IN ('Online', 'Phone')
            THEN 'Remote / Online'

        WHEN Mode = 'In-Person'
            THEN 'In-Person'

        ELSE Mode
    END

ORDER BY completion_rate DESC;
"""

mode_data = pd.read_sql(
    mode_query,
    conn
)


# ============================================================
# CONSULTATION MODE TABLE
# ============================================================

st.dataframe(
    mode_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# CONSULTATION MODE COLORFUL CHART
# ============================================================

fig_mode = px.bar(
    mode_data,
    x="consultation_mode",
    y="completion_rate",
    text="completion_rate",
    title="Consultation Completion Rate: Remote vs In-Person",
    color="consultation_mode",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_mode.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_mode.update_layout(
    yaxis_title="Completion Rate (%)",
    xaxis_title="Consultation Mode",
    height=450,
    showlegend=False
)

st.plotly_chart(
    fig_mode,
    use_container_width=True
)


# ============================================================
# 4. TOTAL VS COMPLETED CONSULTATIONS
# ============================================================

st.markdown("---")
st.subheader("📊 Total vs Completed Consultations")


mode_comparison = mode_data.melt(
    id_vars=["consultation_mode"],

    value_vars=[
        "total_consultations",
        "completed_consultations"
    ],

    var_name="consultation_status",

    value_name="consultations"
)


mode_comparison["consultation_status"] = (
    mode_comparison["consultation_status"]
    .replace({
        "total_consultations": "Total",
        "completed_consultations": "Completed"
    })
)


# ============================================================
# TOTAL VS COMPLETED COLORFUL CHART
# ============================================================

fig_comparison = px.bar(
    mode_comparison,
    x="consultation_mode",
    y="consultations",
    color="consultation_status",
    barmode="group",
    text="consultations",
    title="Total vs Completed Consultations by Mode",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_comparison.update_traces(
    textposition="outside"
)

fig_comparison.update_layout(
    yaxis_title="Number of Consultations",
    xaxis_title="Consultation Mode",
    height=450
)

st.plotly_chart(
    fig_comparison,
    use_container_width=True
)


# ============================================================
# 5. CONSULTATION MODE DISTRIBUTION
# ============================================================

st.markdown("---")
st.subheader("🌐 Consultation Mode Distribution")


mode_share_query = """
SELECT
    CASE
        WHEN Mode IN ('Online', 'Phone')
            THEN 'Remote / Online'

        WHEN Mode = 'In-Person'
            THEN 'In-Person'

        ELSE Mode
    END AS consultation_mode,

    COUNT(*) AS total_consultations

FROM consultations

GROUP BY
    CASE
        WHEN Mode IN ('Online', 'Phone')
            THEN 'Remote / Online'

        WHEN Mode = 'In-Person'
            THEN 'In-Person'

        ELSE Mode
    END;
"""

mode_share = pd.read_sql(
    mode_share_query,
    conn
)


# ============================================================
# COLORFUL DONUT CHART
# ============================================================

fig_share = px.pie(
    mode_share,
    names="consultation_mode",
    values="total_consultations",
    hole=0.45,
    title="Consultation Distribution by Mode",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_share.update_traces(
    textinfo="label+percent",
    textposition="outside"
)

st.plotly_chart(
    fig_share,
    use_container_width=True
)


# ============================================================
# 6. DYNAMIC KEY CONSULTATION INSIGHTS
# ============================================================

st.markdown("---")
st.subheader("🔎 Key Consultation Insights")


# ============================================================
# HIGHEST-PERFORMING CONSULTATION TYPE
# ============================================================

best_type_row = type_data.iloc[0]

best_type = best_type_row["Consultation_Type"]

best_type_rate = best_type_row["completion_rate"]


# ============================================================
# HIGHEST-PERFORMING CONSULTATION MODE
# ============================================================

best_mode_row = mode_data.iloc[0]

best_mode = best_mode_row["consultation_mode"]

best_mode_rate = best_mode_row["completion_rate"]


# ============================================================
# REMOTE CONSULTATION COUNT
# ============================================================

remote_count = int(
    mode_data.loc[
        mode_data["consultation_mode"] == "Remote / Online",
        "total_consultations"
    ].iloc[0]
)


# ============================================================
# IN-PERSON CONSULTATION COUNT
# ============================================================

in_person_count = int(
    mode_data.loc[
        mode_data["consultation_mode"] == "In-Person",
        "total_consultations"
    ].iloc[0]
)


# ============================================================
# REMOTE CONSULTATION SHARE
# ============================================================

remote_percentage = (
    remote_count /
    (remote_count + in_person_count)
) * 100


# ============================================================
# DYNAMIC INSIGHT CARDS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.info(
        "🩺 **Overall Consultation Performance**\n\n"
        f"{completed_consultations:,} out of "
        f"{total_consultations:,} consultations were completed, "
        f"resulting in an overall completion rate of "
        f"**{completion_rate:.2f}%**."
    )


with col2:

    st.success(
        "📋 **Highest Completion by Consultation Type**\n\n"
        f"**{best_type}** recorded the highest completion rate "
        f"at **{best_type_rate:.2f}%**."
    )


col3, col4 = st.columns(2)


with col3:

    st.success(
        "💻 **Highest Completion by Mode**\n\n"
        f"**{best_mode}** recorded the highest consultation "
        f"completion rate at **{best_mode_rate:.2f}%**."
    )


with col4:

    st.info(
        "🌐 **Remote Consultation Usage**\n\n"
        f"Remote / Online consultations accounted for "
        f"**{remote_percentage:.2f}%** of all consultations."
    )


# ============================================================
# CLOSE MYSQL CONNECTION
# ============================================================

conn.close()
