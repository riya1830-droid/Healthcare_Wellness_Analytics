-- Which wellness programs have the highest customer enrollment?
-- KPI -- Total enrollments per program
SELECT Program_Name, COUNT(*) AS total_enrollments FROM programs GROUP BY Program_Name ORDER BY total_enrollments DESC LIMIT 1;


-- Which programs have the highest completion rates?
-- KPI-- Completion Rate= Completed Customers / Total Enrollments * 100
SELECT
    Program_Name, COUNT(*) AS total_enrollments, SUM( CASE WHEN Program_Completed = 'Yes' THEN 1 ELSE 0 END) AS completed_customers,
    ROUND( SUM( CASE WHEN Program_Completed = 'Yes' THEN 1 ELSE 0 END ) * 100.0 / COUNT(*), 2) AS completion_rate
FROM programs GROUP BY Program_Name ORDER BY completion_rate DESC;

-- Which programs are most successful in helping customers achieve their goals?
-- KPI-- Goal Achievement Rate (%)
SELECT
    Program_Name, COUNT(*) AS total_enrollments, SUM( CASE WHEN Goal_Achieved = 'Yes' THEN 1 ELSE 0 END) AS goals_achieved,
    ROUND( SUM( CASE WHEN Goal_Achieved = 'Yes' THEN 1 ELSE 0 END ) * 100.0 / COUNT(*), 2) AS goal_achievement_rate
FROM programs GROUP BY Program_Name ORDER BY goal_achievement_rate DESC;

-- Adherence refers to how closely a customer follows the recommended health program
-- Does higher adherence lead to better outcomes?
-- KPI-- Completion Rate, Goal Achievement Rate by Adherence Group
SELECT CASE
        WHEN Adherence_Percent < 50 THEN 'Low Adherence'
        WHEN Adherence_Percent BETWEEN 50 AND 79 THEN 'Medium Adherence'
        ELSE 'High Adherence' END AS adherence_group,
    COUNT(*) AS customers, ROUND( AVG(CASE
                WHEN Program_Completed = 'Yes' THEN 1 ELSE 0 END) * 100, 2) AS completion_rate, ROUND( AVG(CASE
                WHEN Goal_Achieved = 'Yes' THEN 1 ELSE 0 END) * 100, 2) AS goal_achievement_rate FROM programs GROUP BY CASE
        WHEN Adherence_Percent < 50 THEN 'Low Adherence'
        WHEN Adherence_Percent BETWEEN 50 AND 79 THEN 'Medium Adherence'
        ELSE 'High Adherence' END ORDER BY completion_rate DESC;
        
        
-- Which programs generate the most revenue?
-- KPI-- Total Revenue, Average Revenue per Customer
SELECT Program_Name,
    COUNT(*) AS subscribers,
    ROUND(SUM(Total_Revenue),2) AS total_revenue, ROUND(AVG(Total_Revenue),2) AS avg_revenue_per_customer
FROM subscriptions GROUP BY Program_Name ORDER BY total_revenue DESC;


-- Which programs perform best across enrollment, completion, goal achievement, and revenue?
SELECT p.Program_Name, COUNT(*) AS enrollments,
    ROUND( AVG(CASE
            WHEN p.Program_Completed = 'Yes' THEN 1
                ELSE 0
            END) * 100, 2) AS completion_rate,
ROUND(AVG(CASE
                WHEN p.Goal_Achieved = 'Yes' THEN 1
                ELSE 0 END ) * 100, 2) AS goal_achievement_rate, ROUND(SUM(s.Total_Revenue),2) AS total_revenue
FROM programs p JOIN subscriptions s ON p.Customer_ID = s.Customer_ID GROUP BY p.Program_Name ORDER BY total_revenue DESC;