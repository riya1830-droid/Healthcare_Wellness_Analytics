import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Program Performance & Feedback Analysis",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📋 Program Performance & Feedback Analysis")

st.markdown(
    "Analyze program enrollments, completion, goal achievement, "
    "adherence, program duration, and customer feedback."
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
# 1. PROGRAM KPI OVERVIEW
# ============================================================

kpi_query = """
SELECT
    COUNT(DISTINCT Customer_ID) AS enrolled_customers,

    COUNT(CASE
        WHEN Program_Completed = 'Yes' THEN 1
    END) AS completed_programs,

    COUNT(CASE
        WHEN Goal_Achieved = 'Yes' THEN 1
    END) AS goals_achieved,

    ROUND(
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END)
        / COUNT(*) * 100,
        2
    ) AS completion_rate,

    ROUND(
        COUNT(CASE
            WHEN Goal_Achieved = 'Yes' THEN 1
        END)
        /
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END) * 100,
        2
    ) AS goal_achievement_rate,

    ROUND(
        AVG(Adherence_Percent),
        2
    ) AS average_adherence

FROM programs;
"""

kpi_df = pd.read_sql(
    kpi_query,
    conn
)

enrolled_customers = int(
    kpi_df.loc[0, "enrolled_customers"]
)

completed_programs = int(
    kpi_df.loc[0, "completed_programs"]
)

goals_achieved = int(
    kpi_df.loc[0, "goals_achieved"]
)

completion_rate = float(
    kpi_df.loc[0, "completion_rate"]
)

goal_achievement_rate = float(
    kpi_df.loc[0, "goal_achievement_rate"]
)

average_adherence = float(
    kpi_df.loc[0, "average_adherence"]
)


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Enrolled Customers",
        f"{enrolled_customers:,}"
    )

with col2:
    st.metric(
        "✅ Completed Programs",
        f"{completed_programs:,}"
    )

with col3:
    st.metric(
        "🎯 Goals Achieved",
        f"{goals_achieved:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "📈 Completion Rate",
        f"{completion_rate:.2f}%"
    )

with col5:
    st.metric(
        "🏆 Goal Achievement Rate",
        f"{goal_achievement_rate:.2f}%"
    )

with col6:
    st.metric(
        "📊 Average Adherence",
        f"{average_adherence:.2f}%"
    )


st.divider()


# ============================================================
# 2. PROGRAM-WISE PERFORMANCE
# ============================================================

st.subheader("📊 Program-wise Performance")

program_query = """
SELECT
    Program_Name,

    COUNT(*) AS program_enrollments,

    COUNT(CASE
        WHEN Program_Completed = 'Yes' THEN 1
    END) AS completed_programs,

    COUNT(CASE
        WHEN Goal_Achieved = 'Yes' THEN 1
    END) AS goals_achieved,

    ROUND(
        AVG(Adherence_Percent),
        2
    ) AS average_adherence,

    ROUND(
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END)
        / COUNT(*) * 100,
        2
    ) AS completion_rate,

    ROUND(
        COUNT(CASE
            WHEN Goal_Achieved = 'Yes' THEN 1
        END)
        /
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END) * 100,
        2
    ) AS goal_achievement_rate

FROM programs

GROUP BY Program_Name

ORDER BY completion_rate DESC;
"""

program_df = pd.read_sql(
    program_query,
    conn
)


# ------------------------------------------------------------
# PROGRAM PERFORMANCE TABLE
# ------------------------------------------------------------

st.dataframe(
    program_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 3. PROGRAM COMPLETION RATE
# ============================================================

st.subheader("✅ Program Completion Rate")

fig_completion = px.bar(
    program_df,
    x="Program_Name",
    y="completion_rate",
    text="completion_rate",
    color="Program_Name",
    color_discrete_sequence=px.colors.qualitative.Bold,
    labels={
        "Program_Name": "Program",
        "completion_rate": "Completion Rate (%)"
    },
    title="Program Completion Rate"
)

fig_completion.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_completion.update_layout(
    showlegend=False,
    xaxis_tickangle=-30,
    height=500
)

st.plotly_chart(
    fig_completion,
    use_container_width=True
)


# ============================================================
# 4. GOAL ACHIEVEMENT BY PROGRAM
# ============================================================

st.subheader("🎯 Goal Achievement by Program")

fig_goal = px.bar(
    program_df,
    x="Program_Name",
    y="goal_achievement_rate",
    text="goal_achievement_rate",
    color="Program_Name",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={
        "Program_Name": "Program",
        "goal_achievement_rate": "Goal Achievement Rate (%)"
    },
    title="Goal Achievement Rate by Program"
)

fig_goal.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_goal.update_layout(
    showlegend=False,
    xaxis_tickangle=-30,
    height=500
)

st.plotly_chart(
    fig_goal,
    use_container_width=True
)


# ============================================================
# 5. ENROLLMENT VS COMPLETION
# ============================================================

st.subheader("👥 Enrollments vs Completed Programs")

enrollment_completion_df = program_df[
    [
        "Program_Name",
        "program_enrollments",
        "completed_programs"
    ]
].copy()

enrollment_completion_long = enrollment_completion_df.melt(
    id_vars="Program_Name",
    value_vars=[
        "program_enrollments",
        "completed_programs"
    ],
    var_name="Metric",
    value_name="Count"
)

enrollment_completion_long["Metric"] = (
    enrollment_completion_long["Metric"]
    .replace({
        "program_enrollments": "Enrollments",
        "completed_programs": "Completed"
    })
)

fig_enrollment = px.bar(
    enrollment_completion_long,
    x="Program_Name",
    y="Count",
    color="Metric",
    barmode="group",
    text="Count",
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={
        "Program_Name": "Program",
        "Count": "Number of Enrollments"
    },
    title="Program Enrollments vs Completed Programs"
)

fig_enrollment.update_traces(
    textposition="outside"
)

fig_enrollment.update_layout(
    xaxis_tickangle=-30,
    height=500
)

st.plotly_chart(
    fig_enrollment,
    use_container_width=True
)


# ============================================================
# 6. ADHERENCE ANALYSIS
# ============================================================

st.divider()

st.subheader("📈 Adherence & Program Success")

adherence_query = """
SELECT
    CASE
        WHEN Adherence_Percent < 40 THEN 'Low (<40%)'
        WHEN Adherence_Percent < 60 THEN 'Moderate (40-59%)'
        WHEN Adherence_Percent < 80 THEN 'Good (60-79%)'
        ELSE 'High (80%+)'
    END AS adherence_bucket,

    COUNT(*) AS total_program_enrollments,

    COUNT(CASE
        WHEN Program_Completed = 'Yes' THEN 1
    END) AS completed_programs,

    COUNT(CASE
        WHEN Goal_Achieved = 'Yes' THEN 1
    END) AS goals_achieved,

    ROUND(
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END)
        / COUNT(*) * 100,
        2
    ) AS completion_rate,

    ROUND(
        COUNT(CASE
            WHEN Goal_Achieved = 'Yes' THEN 1
        END)
        /
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END) * 100,
        2
    ) AS goal_achievement_rate

FROM programs

GROUP BY
    CASE
        WHEN Adherence_Percent < 40 THEN 'Low (<40%)'
        WHEN Adherence_Percent < 60 THEN 'Moderate (40-59%)'
        WHEN Adherence_Percent < 80 THEN 'Good (60-79%)'
        ELSE 'High (80%+)'
    END

ORDER BY
    MIN(Adherence_Percent);
"""

adherence_df = pd.read_sql(
    adherence_query,
    conn
)


# ------------------------------------------------------------
# ADHERENCE → COMPLETION
# ------------------------------------------------------------

fig_adherence_completion = px.bar(
    adherence_df,
    x="adherence_bucket",
    y="completion_rate",
    text="completion_rate",
    color="adherence_bucket",
    color_discrete_sequence=px.colors.qualitative.Bold,
    labels={
        "adherence_bucket": "Adherence Level",
        "completion_rate": "Completion Rate (%)"
    },
    title="Adherence Level vs Program Completion"
)

fig_adherence_completion.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_adherence_completion.update_layout(
    showlegend=False,
    height=500
)

st.plotly_chart(
    fig_adherence_completion,
    use_container_width=True
)


# ------------------------------------------------------------
# ADHERENCE → GOAL ACHIEVEMENT
# ------------------------------------------------------------

fig_adherence_goal = px.bar(
    adherence_df,
    x="adherence_bucket",
    y="goal_achievement_rate",
    text="goal_achievement_rate",
    color="adherence_bucket",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    labels={
        "adherence_bucket": "Adherence Level",
        "goal_achievement_rate": "Goal Achievement Rate (%)"
    },
    title="Adherence Level vs Goal Achievement"
)

fig_adherence_goal.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_adherence_goal.update_layout(
    showlegend=False,
    height=500
)

st.plotly_chart(
    fig_adherence_goal,
    use_container_width=True
)


# ============================================================
# 7. PROGRAM DURATION ANALYSIS
# ============================================================

st.divider()

st.subheader("⏳ Program Duration Analysis")

duration_query = """
SELECT
    Duration_Months,

    COUNT(*) AS total_enrollments,

    COUNT(CASE
        WHEN Program_Completed = 'Yes' THEN 1
    END) AS completed_programs,

    COUNT(CASE
        WHEN Goal_Achieved = 'Yes' THEN 1
    END) AS goals_achieved,

    ROUND(
        AVG(Adherence_Percent),
        2
    ) AS average_adherence,

    ROUND(
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END)
        / COUNT(*) * 100,
        2
    ) AS completion_rate,

    ROUND(
        COUNT(CASE
            WHEN Goal_Achieved = 'Yes' THEN 1
        END)
        /
        COUNT(CASE
            WHEN Program_Completed = 'Yes' THEN 1
        END) * 100,
        2
    ) AS goal_achievement_rate

FROM programs

GROUP BY Duration_Months

ORDER BY Duration_Months;
"""

duration_df = pd.read_sql(
    duration_query,
    conn
)


# ------------------------------------------------------------
# DURATION → COMPLETION
# ------------------------------------------------------------

fig_duration_completion = px.bar(
    duration_df,
    x="Duration_Months",
    y="completion_rate",
    text="completion_rate",
    color="Duration_Months",
    color_discrete_sequence=px.colors.qualitative.Set3,
    labels={
        "Duration_Months": "Program Duration (Months)",
        "completion_rate": "Completion Rate (%)"
    },
    title="Program Duration vs Completion Rate"
)

fig_duration_completion.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_duration_completion.update_layout(
    showlegend=False,
    height=500
)

st.plotly_chart(
    fig_duration_completion,
    use_container_width=True
)


# ------------------------------------------------------------
# DURATION → AVERAGE ADHERENCE
# ------------------------------------------------------------

fig_duration_adherence = px.line(
    duration_df,
    x="Duration_Months",
    y="average_adherence",
    markers=True,
    text="average_adherence",
    labels={
        "Duration_Months": "Program Duration (Months)",
        "average_adherence": "Average Adherence (%)"
    },
    title="Program Duration vs Average Adherence"
)

fig_duration_adherence.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="top center"
)

fig_duration_adherence.update_layout(
    height=500
)

st.plotly_chart(
    fig_duration_adherence,
    use_container_width=True
)


# ============================================================
# 8. CUSTOMER FEEDBACK ANALYSIS
# ============================================================

st.divider()

st.subheader("⭐ Customer Feedback Analysis")


# ------------------------------------------------------------
# FEEDBACK KPI OVERVIEW
# ------------------------------------------------------------

feedback_kpi_query = """
SELECT
    COUNT(*) AS total_feedback,

    ROUND(
        AVG(Rating),
        2
    ) AS average_rating,

    COUNT(CASE
        WHEN Rating >= 4 THEN 1
    END) AS positive_feedback,

    COUNT(CASE
        WHEN Rating <= 2 THEN 1
    END) AS negative_feedback,

    ROUND(
        COUNT(CASE
            WHEN Rating >= 4 THEN 1
        END)
        / COUNT(*) * 100,
        2
    ) AS positive_feedback_rate

FROM feedback;
"""

feedback_kpi_df = pd.read_sql(
    feedback_kpi_query,
    conn
)

total_feedback = int(
    feedback_kpi_df.loc[0, "total_feedback"]
)

average_rating = float(
    feedback_kpi_df.loc[0, "average_rating"]
)

positive_feedback = int(
    feedback_kpi_df.loc[0, "positive_feedback"]
)

positive_feedback_rate = float(
    feedback_kpi_df.loc[0, "positive_feedback_rate"]
)


# ------------------------------------------------------------
# FEEDBACK KPI CARDS
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# RATING DISTRIBUTION
# ------------------------------------------------------------

st.subheader("⭐ Rating Distribution")

feedback_rating_query = """
SELECT
    Rating,

    COUNT(*) AS feedback_count,

    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage

FROM feedback

GROUP BY Rating

ORDER BY Rating;
"""

feedback_rating_df = pd.read_sql(
    feedback_rating_query,
    conn
)

fig_feedback_rating = px.bar(
    feedback_rating_df,
    x="Rating",
    y="feedback_count",
    text="feedback_count",
    color="Rating",
    color_discrete_sequence=px.colors.qualitative.Bold,
    labels={
        "Rating": "Rating",
        "feedback_count": "Number of Feedback Records"
    },
    title="Customer Feedback Rating Distribution"
)

fig_feedback_rating.update_traces(
    textposition="outside"
)

fig_feedback_rating.update_layout(
    showlegend=False,
    height=500
)

st.plotly_chart(
    fig_feedback_rating,
    use_container_width=True
)


# ------------------------------------------------------------
# FEEDBACK VS RENEWAL
# ------------------------------------------------------------

st.subheader("🔄 Customer Feedback vs Renewal")

feedback_renewal_query = """
SELECT
    CASE
        WHEN f.Rating >= 4 THEN 'Positive (4-5)'
        WHEN f.Rating = 3 THEN 'Neutral (3)'
        ELSE 'Negative (1-2)'
    END AS feedback_segment,

    COUNT(DISTINCT f.Customer_ID) AS customers,

    COUNT(DISTINCT CASE
        WHEN s.Renewed = 'Renewed'
        THEN f.Customer_ID
    END) AS renewed_customers,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN s.Renewed = 'Renewed'
            THEN f.Customer_ID
        END)
        / COUNT(DISTINCT f.Customer_ID) * 100,
        2
    ) AS renewal_rate

FROM feedback f

LEFT JOIN subscriptions s
    ON f.Customer_ID = s.Customer_ID

GROUP BY
    CASE
        WHEN f.Rating >= 4 THEN 'Positive (4-5)'
        WHEN f.Rating = 3 THEN 'Neutral (3)'
        ELSE 'Negative (1-2)'
    END

ORDER BY renewal_rate DESC;
"""

feedback_renewal_df = pd.read_sql(
    feedback_renewal_query,
    conn
)


# ------------------------------------------------------------
# FEEDBACK VS RENEWAL TABLE
# ------------------------------------------------------------

st.dataframe(
    feedback_renewal_df,
    use_container_width=True,
    hide_index=True
)


# ------------------------------------------------------------
# FEEDBACK VS RENEWAL CHART
# ------------------------------------------------------------

fig_feedback_renewal = px.bar(
    feedback_renewal_df,
    x="feedback_segment",
    y="renewal_rate",
    text="renewal_rate",
    color="feedback_segment",
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={
        "feedback_segment": "Feedback Segment",
        "renewal_rate": "Renewal Rate (%)"
    },
    title="Customer Feedback vs Renewal Rate"
)

fig_feedback_renewal.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_feedback_renewal.update_layout(
    showlegend=False,
    height=500
)

st.plotly_chart(
    fig_feedback_renewal,
    use_container_width=True
)


# ------------------------------------------------------------
# DYNAMIC FEEDBACK INSIGHT
# ------------------------------------------------------------

highest_renewal_feedback = feedback_renewal_df.loc[
    feedback_renewal_df["renewal_rate"].idxmax()
]

st.info(
    f"""
    💡 **Feedback & Retention Insight**

    The **{highest_renewal_feedback['feedback_segment']}**
    feedback segment has the highest observed renewal rate
    of **{highest_renewal_feedback['renewal_rate']:.2f}%**.
    """
)


# ============================================================
# 9. DYNAMIC BUSINESS INSIGHTS
# ============================================================

st.divider()

st.subheader("💡 Key Program Insights")


# ------------------------------------------------------------
# HIGHEST COMPLETION PROGRAM
# ------------------------------------------------------------

best_completion_program = program_df.loc[
    program_df["completion_rate"].idxmax()
]


# ------------------------------------------------------------
# HIGHEST GOAL ACHIEVEMENT PROGRAM
# ------------------------------------------------------------

best_goal_program = program_df.loc[
    program_df["goal_achievement_rate"].idxmax()
]


# ------------------------------------------------------------
# STRONGEST ADHERENCE SEGMENT
# ------------------------------------------------------------

best_adherence_bucket = adherence_df.loc[
    adherence_df["completion_rate"].idxmax()
]


# ------------------------------------------------------------
# BEST DURATION BY COMPLETION
# ------------------------------------------------------------

best_duration = duration_df.loc[
    duration_df["completion_rate"].idxmax()
]


# ------------------------------------------------------------
# INSIGHT CARDS
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
        🏆 **Highest Program Completion:**

        {best_completion_program['Program_Name']}
        with **{best_completion_program['completion_rate']:.2f}%**
        completion.
        """
    )

    st.info(
        f"""
        🎯 **Highest Goal Achievement:**

        {best_goal_program['Program_Name']}
        with **{best_goal_program['goal_achievement_rate']:.2f}%**
        goal achievement among completed programs.
        """
    )


with col2:

    st.warning(
        f"""
        📈 **Strongest Adherence Segment:**

        {best_adherence_bucket['adherence_bucket']}
        with **{best_adherence_bucket['completion_rate']:.2f}%**
        completion.
        """
    )

    st.info(
        f"""
        ⏳ **Highest Completion by Duration:**

        {int(best_duration['Duration_Months'])} months
        with **{best_duration['completion_rate']:.2f}%**
        completion.
        """
    )


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

conn.close()

