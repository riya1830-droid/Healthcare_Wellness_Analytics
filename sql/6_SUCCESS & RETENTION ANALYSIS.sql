-- Among customers who completed their programs, how many achieved their health goals?
-- KPI-- Completed Programs, Goals Achieved, Goal Achievement Rate
SELECT
    COUNT(CASE
    WHEN Program_Completed = 'Yes' THEN 1 END) AS completed_customers,
    COUNT(CASE
            WHEN Program_Completed = 'Yes' AND Goal_Achieved = 'Yes' THEN 1 END ) AS goal_achieved_customers,
    ROUND(
        COUNT(CASE
        WHEN Program_Completed = 'Yes' AND Goal_Achieved = 'Yes' THEN 1 END) * 100.0
        /
        COUNT(CASE
                WHEN Program_Completed = 'Yes' THEN 1 END), 2) AS goal_achievement_rate FROM programs;
                

-- Do customers who achieve goals continue using the platform?
-- KPI -- Goal Achieved Customers, Renewed Customers, Renewal Rate
SELECT
    COUNT(CASE
            WHEN p.Goal_Achieved = 'Yes' THEN 1 END) AS goal_achieved_customers,
    COUNT(CASE
            WHEN p.Goal_Achieved = 'Yes' AND s.Renewed = 'Renewed' THEN 1 END) AS renewed_customers,
    ROUND(
        COUNT(CASE
                WHEN p.Goal_Achieved = 'Yes' AND s.Renewed = 'Renewed' THEN 1 END) * 100.0
        /
        COUNT(CASE
                WHEN p.Goal_Achieved = 'Yes' THEN 1 END),2) AS renewal_rate
FROM programs p JOIN subscriptions s ON p.Customer_ID = s.Customer_ID;


-- Does completing a program increase the likelihood of renewal?
SELECT Program_Completed,
COUNT(*) AS customers,
SUM(CASE
		WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END) AS renewed_customers,
    ROUND(AVG(
         CASE
			WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END) * 100, 2) AS renewal_rate
FROM programs p JOIN subscriptions s ON p.Customer_ID = s.Customer_ID GROUP BY Program_Completed;


-- Do highly engaged(HIGH ADHERENCE) customers renew more often?
SELECT
    CASE
        WHEN Adherence_Percent < 50 THEN 'Low Adherence'
        WHEN Adherence_Percent BETWEEN 50 AND 79 THEN 'Medium Adherence'
        ELSE 'High Adherence' END AS adherence_group,
    COUNT(*) AS customers,
    SUM(CASE
            WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END) AS renewed_customers,
    ROUND(AVG(CASE
                WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END ) * 100, 2) AS renewal_rate
     FROM programs p JOIN subscriptions s ON p.Customer_ID = s.Customer_ID GROUP BY adherence_group ORDER BY renewal_rate DESC;
     
     
-- Which wellness programs retain customers most effectively?
SELECT
    p.Program_Name,
    COUNT(*) AS customers, SUM(CASE 
          WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END ) AS renewed_customers,
ROUND(
        AVG(CASE
                WHEN s.Renewed = 'Renewed' THEN 1 ELSE 0 END ) * 100, 2 ) AS renewal_rate
FROM programs p JOIN subscriptions s ON p.Customer_ID = s.Customer_ID GROUP BY p.Program_Name ORDER BY renewal_rate DESC;
