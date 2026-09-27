use patient_analysis;

-- Find Missing values --
SELECT
    SUM(Customer_ID IS NULL) AS Missing_Customer_ID,
    SUM(Age IS NULL) AS Missing_Age,
    SUM(Gender IS NULL) AS Missing_Gender,
    SUM(City IS NULL) AS Missing_City,
    SUM(Height_cm IS NULL) AS Missing_Height,
    SUM(Initial_Weight_kg IS NULL) AS Missing_Weight,
    SUM(InitiaL_BMI IS NULL) AS Missing_BMI,
    SUM(Join_Date IS NULL) AS Missing_Join_Date
FROM customers;

SELECT
    SUM(Program_ID IS NULL) AS Missing_Program_ID,
    SUM(Customer_ID IS NULL) AS Missing_Customer_ID,
    SUM(Program_Name IS NULL) AS Missing_Program_Name,
    SUM(Enrollment_Date IS NULL) AS Missing_Enrollment_Date,
    SUM(Duration_Months IS NULL) AS Missing_Duration,
    SUM(Adherence_Percent IS NULL) AS Missing_Adherence,
    SUM(Program_Completed IS NULL) AS Missing_Completion,
    SUM(Goal_Achieved IS NULL) AS Missing_Goal
FROM programs;

SELECT
    SUM(Subscription_ID IS NULL) AS Missing_Subscription_ID,
    SUM(Customer_ID IS NULL) AS Missing_Customer_ID,
    SUM(Program_Name IS NULL) AS Missing_Program,
    SUM(Plan_Price IS NULL) AS Missing_Price,
    SUM(Initial_Duration_Months IS NULL) AS Missing_Duration,
    SUM(Renewed IS NULL) AS Missing_Renewed,
    SUM(Renewal_Months IS NULL) AS Missing_Renewal_Months,
    SUM(Total_Revenue IS NULL) AS Missing_Revenue
FROM subscriptions;

SELECT
    SUM(Feedback_ID IS NULL) AS Missing_Feedback_ID,
    SUM(Customer_ID IS NULL) AS Missing_Customer_ID,
    SUM(Feedback_Date IS NULL) AS Missing_Date,
    SUM(Rating IS NULL) AS Missing_Rating,
    SUM(Comment IS NULL) AS Missing_Comment
FROM feedback;

SELECT
    SUM(Measurement_ID IS NULL) AS Missing_Measurement_ID,
    SUM(Customer_ID IS NULL) AS Missing_Customer_ID,
    SUM(Measurement_Date IS NULL) AS Missing_Date,
    SUM(Weight_kg IS NULL) AS Missing_Weight,
    SUM(BMI IS NULL) AS Missing_BMI
FROM health_measurements;

-- Find Duplicate Records-- (checking primary keys)
 
select customer_id, count(*) as dup_count from customers group by customer_id having count(*)>1;
select program_id, count(*) as dup_count from programs group by program_id having count(*)>1; 
select subscription_id, count(*) as dup_count from subscriptions group by subscription_id having count(*)>1;
select consultation_id, count(*) as dup_count from consultations group by consultation_id having count(*)>1;
select feedback_id, count(*) as dup_count from feedback group by feedback_id having count(*)>1; 
select measurement_id, count(*) as dup_count from health_measurements group by measurement_id having count(*)>1; 

-- duplicate customers
SELECT sum(Duplicate_Count) as total from
  (select Program_Name,
    COUNT(*) AS Duplicate_Count
FROM programs
GROUP BY  Program_Name
HAVING COUNT(*) > 1)
as x;