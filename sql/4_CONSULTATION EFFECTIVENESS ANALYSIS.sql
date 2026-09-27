use patient_analysis;
select * from consultations;
-- What percentage of consultations are successful, cancelled, pending, or unsuccessful?
-- KPI-- Consultation Success Rate, Consultation Cancellation Rate
SELECT Status, COUNT(*) AS total_consultations,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage_share
FROM consultations GROUP BY Status ORDER BY total_consultations DESC;


-- Which consultation type is used most frequently?
-- KPI -- Most Popular Consultation Type, Consultation Type Share

SELECT Consultation_type, COUNT(*) AS Total_Consultations, 
ROUND( COUNT(*) * 100.0 / SUM(COUNT(*)) over(), 2) AS Percentage_Share from consultations
group by consultation_type order by total_consultations desc;	


-- Which consultation mode is used more frequently?
-- KPI -- Online, OFFLINE Consultation %

select CASE 
 WHEN MODE IN ('ONLINE' , 'PHONE') THEN 'ONLINE' ELSE 'OFFLINE' END AS Consultation_mode,
count(*) as total_consultations, ROUND(count(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS Percentage_share
from consultations group by  CASE WHEN Mode IN ('Online', 'Phone') THEN 'Online' ELSE 'Offline' END;


-- How many customers required more than one consultation?

SELECT COUNT(*) AS customers_with_multiple_consultations FROM (
    SELECT Customer_ID FROM consultations GROUP BY Customer_ID HAVING COUNT(*) > 1) t;
    

-- Does consultation mode affect consultation success?
-- KPI -- SUCCESS RATE

SELECT
    CASE WHEN Mode IN ('Online', 'Phone') THEN 'Online' ELSE 'Offline' END AS consultation_mode, COUNT(*) AS total_consultations,
      SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END) AS successful_consultations,
      ROUND(
        SUM(CASE WHEN Status = 'Completed' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*), 2) AS success_rate FROM consultations GROUP BY consultation_mode;


-- Which customers had the highest number of consultations?
-- KPI -- Highest Consultation Frequency

SELECT Customer_ID, COUNT(*) AS consultation_count FROM consultations GROUP BY Customer_ID HAVING COUNT(*) > 1 ORDER BY consultation_count DESC LIMIT 10;

-- How many customers had 1 consultation, 2 consultations, 3 consultations, etc.? (not much imp)
SELECT consultation_count, COUNT(*) AS number_of_customers FROM 
(SELECT Customer_ID, COUNT(*) AS consultation_count FROM consultations GROUP BY Customer_ID) t GROUP BY consultation_count ORDER BY consultation_count;

        






