-- Average weight loss and BMI improvement during their wellness journey?
SELECT
    ROUND(AVG(c.Initial_Weight_kg - h.Weight_kg), 2) AS avg_weight_loss_kg,
    ROUND(AVG(c.Initial_BMI - h.BMI), 2) AS avg_bmi_improvement
FROM customers c
JOIN (
    SELECT Customer_ID, Weight_kg, BMI,
           ROW_NUMBER() OVER(
               PARTITION BY Customer_ID
               ORDER BY Measurement_Date DESC
           ) AS rn
    FROM health_measurements
) h
ON c.Customer_ID = h.Customer_ID
WHERE h.rn = 1;


-- Which programs show greater average weight improvement?
SELECT
    p.Program_Name,
    ROUND(AVG(c.Initial_Weight_kg - h.Weight_kg), 2) AS avg_weight_loss
FROM customers c
JOIN programs p ON c.Customer_ID = p.Customer_ID
JOIN (
    SELECT Customer_ID, Weight_kg,
           ROW_NUMBER() OVER(
               PARTITION BY Customer_ID
               ORDER BY Measurement_Date DESC
           ) AS rn
    FROM health_measurements
) h
ON c.Customer_ID = h.Customer_ID
WHERE h.rn = 1
GROUP BY p.Program_Name
ORDER BY avg_weight_loss DESC;


-- Do customers who achieve their goals lose more weight?
-- Does higher program adherence lead to better results?
-- Whether higher program adherence is associated with better weight outcomes.
SELECT
    CASE
        WHEN p.Adherence_Percent < 50 THEN 'Low Adherence'
        WHEN p.Adherence_Percent < 80 THEN 'Medium Adherence'
        ELSE 'High Adherence'
    END AS adherence_group,

    COUNT(*) AS customers,

    ROUND(
        AVG(c.Initial_Weight_kg - h.Weight_kg), 2
    ) AS avg_weight_loss
FROM customers c
JOIN programs p ON c.Customer_ID = p.Customer_ID
JOIN (
    SELECT Customer_ID, Weight_kg,
           ROW_NUMBER() OVER(
               PARTITION BY Customer_ID
               ORDER BY Measurement_Date DESC
           ) AS rn
    FROM health_measurements
) h
ON c.Customer_ID = h.Customer_ID
WHERE h.rn = 1
GROUP BY adherence_group
ORDER BY avg_weight_loss DESC;