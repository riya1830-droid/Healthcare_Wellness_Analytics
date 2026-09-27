-- Uses a CTE to combine key customer journey metrics into one analysis.

WITH journey AS (
    SELECT
        p.Customer_ID,
        p.Adherence_Percent,
        p.Program_Completed,
        p.Goal_Achieved,
        s.Renewed
    FROM programs p
    JOIN subscriptions s
        ON p.Customer_ID = s.Customer_ID
)
SELECT
    COUNT(*) AS total_customers,
    SUM(Program_Completed = 'Yes') AS program_completed_customers,
    SUM(Goal_Achieved = 'Yes') AS goal_achieved_customers,
    SUM(Renewed = 'Renewed') AS renewed_customers
FROM journey;


-- Uses RANK() to identify the revenue position of each program.
SELECT
    Program_Name,
    SUM(Total_Revenue) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(Total_Revenue) DESC
    ) AS revenue_rank
FROM subscriptions
GROUP BY Program_Name;


-- Examines whether customer engagement is associated with retention.
SELECT
    CASE
        WHEN Adherence_Percent < 50 THEN 'Low'
        WHEN Adherence_Percent < 80 THEN 'Medium'
        ELSE 'High'
    END AS adherence_group,

    COUNT(*) AS customers,

    SUM(Renewed = 'Renewed') AS renewed_customers,

    ROUND(
        SUM(Renewed = 'Renewed') * 100.0 / COUNT(*),
        2
    ) AS renewal_rate
FROM programs p
JOIN subscriptions s
    ON p.Customer_ID = s.Customer_ID
GROUP BY adherence_group
ORDER BY renewal_rate DESC;


/* 9.4 Final Business Insights

Based on the analyses, summarize your project findings around these areas:

📌 Customer Journey
Identify where the largest customer drop-off occurs.
Monitor completion and goal-achievement rates.
📌 Retention
Analyze the relationship between goal achievement and subscription renewal.
Monitor program completion → renewal.
📌 Revenue
Identify programs generating higher revenue.
Track renewal revenue and average customer value.
📌 Health Outcomes
Monitor weight and BMI improvement.
Compare outcomes across programs and adherence groups.
💡 Business Recommendations
Improve program completion by identifying customers who disengage before completion.
Increase retention by engaging customers after goal achievement and before subscription expiry.
Focus on high-performing programs while investigating why other programs have weaker outcomes.
Use adherence tracking to identify customers who may need additional support.
Monitor health outcomes and revenue together to understand which programs create both customer value and business value. */
