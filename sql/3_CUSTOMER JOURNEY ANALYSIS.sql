use patient_analysis;

-- Key insight:
-- The largest patient drop-off occurs from Enrollment to Completion,
-- where 6,285 customers are lost (31.43% drop-off).
-- The second-largest drop-off is from Goal Achievement to Renewal,
-- where 2,567 customers are lost (20.73% drop-off).

-- CUSTOMER JOURNEY FUNNEL --

SELECT COUNT(DISTINCT Customer_ID) AS TOTAL_CUSTOMERS FROM CUSTOMERS;
-- TOTAL CONSULTATIONS BY CUSTOMERS-- (68578) 
SELECT COUNT( DISTINCT CUSTOMER_ID) AS CUSTOMERS_CONSULTED FROM CONSULTATIONS;
-- CUSTOMERS CONSULTED-- (20000)
SELECT COUNT(DISTINCT CUSTOMER_ID) AS TOTAL_CUSTOMERS_CONSULTED FROM CONSULTATIONS; 
-- CUSTOMERS ENROLLED--
SELECT COUNT(DISTINCT Customer_ID) AS Customers_Enrolled FROM programs;
-- CUSTOMERS COMPLETED PROGRAM-- 
SELECT COUNT(DISTINCT Customer_ID) AS CUSTOMERS_COMPLETED_PROGRAMS FROM programs WHERE Program_Completed = 'Yes';
-- CUSTOMERS WHO ACHIEVE THEIR GOALS--
SELECT COUNT(DISTINCT Customer_ID) AS CUSTOMERS_ACHIEVED_GOAL FROM programs WHERE Goal_Achieved = 'Yes';
-- CUSTOMERS WHO RENEW THEIR SUBSCRIPTIONS--
SELECT COUNT(DISTINCT Customer_ID) AS CUSTOMER_RENEWED FROM subscriptions WHERE Renewed = 'RENEWED';

-- CONVERSION RATE BETWEEN EACH STAGE OF CUSTOMER JOURNEY-((Current Stage / Previous Stage) × 100)
-- DROPOFF RATE - (100 - Conversion Rate) 

-- 1. Registration → Consultation
-- 2. Enrollment → Program Completion
-- 3. Completion → Goal Achievement
-- 4. Goal Achievement → Renewal
WITH funnel AS (
    SELECT
        (SELECT COUNT(DISTINCT Customer_ID)
         FROM customers) AS registered_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM consultations) AS consulted_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM programs) AS enrolled_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM programs
         WHERE Program_Completed = 'YES') AS completed_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM programs
         WHERE Goal_Achieved = 'YES') AS goal_achieved_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM subscriptions
         WHERE Renewed = 'RENEWED') AS renewed_customers
)

SELECT
    'Registration → Consultation' AS stage_transition,
    registered_customers AS previous_stage,
    consulted_customers AS current_stage,

    ROUND(
        consulted_customers * 100.0 / registered_customers,
        2
    ) AS conversion_rate,

    ROUND(
        100 - (consulted_customers * 100.0 / registered_customers),
        2
    ) AS dropoff_rate,

    registered_customers - consulted_customers AS lost_customers

FROM funnel

UNION ALL

SELECT
    'Consultation → Enrollment',
    consulted_customers,
    enrolled_customers,

    ROUND(
        enrolled_customers * 100.0 / consulted_customers,
        2
    ),

    ROUND(
        100 - (enrolled_customers * 100.0 / consulted_customers),
        2
    ),

    consulted_customers - enrolled_customers

FROM funnel

UNION ALL

SELECT
    'Enrollment → Completion',
    enrolled_customers,
    completed_customers,

    ROUND(
        completed_customers * 100.0 / enrolled_customers,
        2
    ),

    ROUND(
        100 - (completed_customers * 100.0 / enrolled_customers),
        2
    ),

    enrolled_customers - completed_customers

FROM funnel

UNION ALL

SELECT
    'Completion → Goal Achievement',
    completed_customers,
    goal_achieved_customers,

    ROUND(
        goal_achieved_customers * 100.0 / completed_customers,
        2
    ),

    ROUND(
        100 - (goal_achieved_customers * 100.0 / completed_customers),
        2
    ),

    completed_customers - goal_achieved_customers

FROM funnel

UNION ALL

SELECT
    'Goal Achievement → Renewal',
    goal_achieved_customers,
    renewed_customers,

    ROUND(
        renewed_customers * 100.0 / goal_achieved_customers,
        2
    ),

    ROUND(
        100 - (renewed_customers * 100.0 / goal_achieved_customers),
        2
    ),

    goal_achieved_customers - renewed_customers

FROM funnel;

WITH funnel AS (
    SELECT
        (SELECT COUNT(DISTINCT Customer_ID) FROM customers) AS registered_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM consultations) AS consulted_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM programs) AS enrolled_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM programs
         WHERE Program_Completed = 'YES') AS completed_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM programs
         WHERE Goal_Achieved = 'YES') AS goal_achieved_customers,

        (SELECT COUNT(DISTINCT Customer_ID)
         FROM subscriptions
         WHERE Renewed = 'RENEWED') AS renewed_customers
)

SELECT
    Stage,
    Customer_Count,
    Conversion_Rate,
    Dropoff_Rate,
    Lost_Customers
FROM (
    SELECT
        1 AS stage_order,
        'Total Registered Customers' AS Stage,
        registered_customers AS Customer_Count,
       0 AS Conversion_Rate,
        0 AS Dropoff_Rate,
        0 AS Lost_Customers
    FROM funnel

    UNION ALL

    SELECT
        2,
        'Customers Consulted',
        consulted_customers,
        ROUND(consulted_customers * 100.0 / registered_customers, 2),
        ROUND(100 - (consulted_customers * 100.0 / registered_customers), 2),
        registered_customers - consulted_customers
    FROM funnel

    UNION ALL

    SELECT
        3,
        'Customers Enrolled',
        enrolled_customers,
        ROUND(enrolled_customers * 100.0 / consulted_customers, 2),
        ROUND(100 - (enrolled_customers * 100.0 / consulted_customers), 2),
        consulted_customers - enrolled_customers
    FROM funnel

    UNION ALL

    SELECT
        4,
        'Program Completed',
        completed_customers,
        ROUND(completed_customers * 100.0 / enrolled_customers, 2),
        ROUND(100 - (completed_customers * 100.0 / enrolled_customers), 2),
        enrolled_customers - completed_customers
    FROM funnel

    UNION ALL

    SELECT
        5,
        'Goal Achieved',
        goal_achieved_customers,
        ROUND(goal_achieved_customers * 100.0 / completed_customers, 2),
        ROUND(100 - (goal_achieved_customers * 100.0 / completed_customers), 2),
        completed_customers - goal_achieved_customers
    FROM funnel

    UNION ALL

    SELECT
        6,
        'Subscription Renewed',
        renewed_customers,
        ROUND(renewed_customers * 100.0 / goal_achieved_customers, 2),
        ROUND(100 - (renewed_customers * 100.0 / goal_achieved_customers), 2),
        goal_achieved_customers - renewed_customers
    FROM funnel
) AS funnel_results
ORDER BY stage_order;

