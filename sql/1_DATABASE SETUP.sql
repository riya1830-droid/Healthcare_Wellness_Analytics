use patient_analysis;
select distinct count(*) from customers;

-- --- CUSTOMERS TABLE ---
ALTER TABLE customers MODIFY COLUMN Customer_ID VARCHAR(50) NOT NULL;
ALTER TABLE customers ADD PRIMARY KEY (Customer_ID);

-- --- CONSULTATIONS TABLE ---
ALTER TABLE consultations MODIFY COLUMN Consultation_ID VARCHAR(50) NOT NULL;
ALTER TABLE consultations MODIFY COLUMN Customer_ID VARCHAR(50) NOT NULL;
ALTER TABLE consultations ADD PRIMARY KEY (Consultation_ID);

-- --- PROGRAMS TABLE ---
ALTER TABLE programs MODIFY COLUMN Program_ID VARCHAR(50) NOT NULL;
ALTER TABLE programs MODIFY COLUMN Customer_ID VARCHAR(50) NOT NULL;
ALTER TABLE programs ADD PRIMARY KEY (Program_ID);

-- --- HEALTH_MEASUREMENTS TABLE ---
ALTER TABLE health_measurements MODIFY COLUMN Measurement_ID VARCHAR(50) NOT NULL;
ALTER TABLE health_measurements MODIFY COLUMN Customer_ID VARCHAR(50) NOT NULL;
ALTER TABLE health_measurements MODIFY COLUMN measurement_date date NOT NULL;
ALTER TABLE health_measurements ADD PRIMARY KEY (Measurement_ID);

-- --- SUBSCRIPTIONS TABLE ---
ALTER TABLE subscriptions MODIFY COLUMN Subscription_ID VARCHAR(50) NOT NULL;
ALTER TABLE subscriptions MODIFY COLUMN Customer_ID VARCHAR(50) NOT NULL;
ALTER TABLE subscriptions ADD PRIMARY KEY (Subscription_ID);

-- --- FEEDBACK TABLE ---
ALTER TABLE feedback MODIFY COLUMN Feedback_ID VARCHAR(50) NOT NULL;
ALTER TABLE feedback MODIFY COLUMN Customer_ID VARCHAR(50) NOT NULL;
ALTER TABLE feedback ADD PRIMARY KEY (Feedback_ID);

-- --- FOREIGN KEYS ---
ALTER TABLE consultations ADD CONSTRAINT fk_consultations_customer FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE;
ALTER TABLE programs ADD CONSTRAINT fk_programs_customer FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE;
ALTER TABLE health_measurements ADD CONSTRAINT fk_measurements_customer FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE;
ALTER TABLE subscriptions ADD CONSTRAINT fk_subscriptions_customer FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE;
ALTER TABLE feedback ADD CONSTRAINT fk_feedback_customer FOREIGN KEY (Customer_ID) REFERENCES customers(Customer_ID) ON DELETE CASCADE;
use patient_analysis;

select * from SUBSCRIPTIONS;
select * from  customers;
select * from  consultations;
select * from  programs;

desc customers;
desc consultations;
desc programs;
desc health_measurements;
desc subscriptions;
desc feedback;
select * from health_measurements;




