# 🏥 Healthcare & Wellness Analytics

### MySQL + Python + Streamlit Customer Journey Analytics Project

A data analytics project focused on analyzing the customer journey of a synthetic healthcare and wellness platform — from registration and consultation to program completion, goal achievement, subscription renewal, revenue, feedback, and health outcomes.

The project uses **MySQL and SQL for database management and business analysis**, while **Python, Pandas, Plotly, and Streamlit** are used to build an interactive analytics dashboard.

> **Dataset Note:** This project uses synthetic data created for portfolio and analytics practice purposes. It does not contain real customer, patient, or healthcare data.

---

## 📌 Project Overview

The project analyzes the complete customer journey:

**Registration → Consultation → Program Enrollment → Program Completion → Goal Achievement → Subscription Renewal**

The goal is to understand customer engagement, program performance, retention, revenue, feedback, and health outcomes.

---

## 🎯 Business Problem

The project aims to identify patterns and opportunities related to:

* Customer engagement
* Consultation performance
* Program completion
* Goal achievement
* Customer adherence
* Customer retention
* Subscription renewal
* Revenue
* Customer feedback
* Health outcomes

---

## 🛠️ Tools & Technologies

| Technology     | Purpose                                             |
| -------------- | --------------------------------------------------- |
| **Python**     | Data generation and dashboard development           |
| **MySQL**      | Database and SQL analysis                           |
| **SQL**        | Data validation, calculations and business analysis |
| **Pandas**     | Data retrieval and processing                       |
| **Plotly**     | Interactive visualizations                          |
| **Streamlit**  | Interactive dashboard                               |
| **VS Code**    | Development                                         |
| **Git/GitHub** | Version control                                     |

---

# 🗄️ Database

### Database Name

`patient_analysis`

### Tables

| Table                 | Purpose                                       |
| --------------------- | --------------------------------------------- |
| `customers`           | Customer details and registration information |
| `consultations`       | Consultation records                          |
| `programs`            | Program enrollment and performance            |
| `health_measurements` | Weight and BMI measurements                   |
| `feedback`            | Customer ratings and comments                 |
| `subscriptions`       | Subscription and revenue information          |

### Customer Journey

```text
Registration
      ↓
Consultation
      ↓
Program Enrollment
      ↓
Program Completion
      ↓
Goal Achievement
      ↓
Subscription Renewal
```

---

# 📊 Key Project Metrics

| Metric                           |            Value |
| -------------------------------- | ---------------: |
| 👥 Total Customers               |       **20,000** |
| 🩺 Consultation Records          |       **68,578** |
| 📋 Enrolled Customers            |       **20,000** |
| ✅ Completed Programs             |       **13,715** |
| 🎯 Goals Achieved                |       **12,381** |
| 🔄 Renewed Customers             |        **9,814** |
| 📈 Enrollment → Completion       |       **68.58%** |
| 🎯 Completion → Goal Achievement |       **90.28%** |
| 🔄 Goal Achievement → Renewal    |       **79.27%** |
| 📊 Overall Goal → Renewal        |       **49.07%** |
| 💰 Total Subscription Revenue    | **₹326,149,699** |
| 💵 Average Revenue per Customer  |   **₹16,307.48** |
| ⚖️ Average Weight Change         |     **-2.18 kg** |
| 🧮 Average BMI Change            |        **-0.81** |

> Dashboard calculations are generated dynamically using SQL queries rather than hardcoded numerical values.

---

# 🔍SQL Analysis Performed

## 1. 🗄️ Database & Data Understanding

* Database structure
* Table relationships
* Primary and foreign keys
* Data types
* Customer journey

## 2. ✅ Data Quality & Validation

* NULL checks
* Duplicate checks
* Primary key validation
* Foreign key validation
* Invalid value checks
* Data consistency

## 3. 🚶 Customer Journey / Funnel Analysis

* Registration → Consultation
* Consultation → Enrollment
* Enrollment → Completion
* Completion → Goal Achievement
* Goal Achievement → Renewal
* Funnel drop-offs and conversion rates

## 4. 🩺 Consultation Analysis

* Consultation volume
* Completed consultations
* Completion rate
* Consultation type performance
* Consultation mode performance
* Remote / Online vs In-Person

## 5. 📋 Program Performanc Analysis

* Program enrollment
* Program completion
* Completion rate
* Goal achievement
* Adherence analysis
* Program duration
* Enrollment vs completion

## 6. 🔄 Success & Retention Analysis

* Completion → Goal Achievement
* Goal Achievement → Renewal
* Completion → Renewal
* Retention metrics
* Customer success patterns

## 7. 💰 Revenue & Subscription Analysis

* Total revenue
* Average revenue
* Subscription duration
* Renewal analysis
* Revenue distribution
* Top customer revenue
* Revenue segmentation

## 8. ⚖️ Health Outcomes Analysis

* Initial vs latest weight
* Weight change
* Initial vs latest BMI
* BMI change
* Health outcome segmentation

> Health changes are descriptive and do not establish that the platform or program caused the observed outcomes.

## 9. 🧠 Advanced Customer Insights

* Customer segmentation
* High-value customer analysis
* Revenue segmentation
* Adherence segmentation
* Adherence vs completion
* Adherence vs goal achievement
* Adherence vs renewal
* Ranking and window functions

---

# 🖥️ Streamlit Dashboard

The project contains an interactive **8-page Streamlit dashboard**.

### 📊 Page 1 — Customer Journey & Business Overview

* Customer KPIs
* Journey funnel
* Completion and goal metrics
* Renewal metrics
* Key insights

### 🩺 Page 2 — Consultation Analysis

* Consultation KPIs
* Type analysis
* Mode analysis
* Completion rate
* Remote vs In-Person

### 📋 Page 3 — Program Performance & Feedback Analysis

* Program performance
* Completion and goal achievement
* Adherence
* Program duration
* Customer feedback
* Average rating
* Rating distribution
* Positive feedback rate
* Feedback vs renewal

### 🔄 Page 4 — Success & Retention Analysis

* Completion → Goal
* Goal → Renewal
* Completion → Renewal
* Retention metrics
* Success insights

### 💰 Page 5 — Revenue & Subscription Analysis

* Revenue KPIs
* Subscription duration
* Renewal analysis
* Revenue distribution
* Top customer revenue
* Revenue insights

### ⚖️ Page 6 — Health Outcomes

* Health KPIs
* Weight analysis
* BMI analysis
* Weight change distribution
* Health outcome segmentation

### 🧠 Page 7 — Advanced Customer Insights

* Customer segmentation
* High-value customers
* Revenue segmentation
* Adherence analysis
* Advanced SQL insights

### 📌 Page 8 — Executive Summary

* Overall KPIs
* Customer journey summary
* Feedback summary
* Health outcome summary
* Key business insights
* Business recommendations

---

# 🗂️ Project Structure

```text
Healthcare_Wellness_Analytics/
│
├── Home.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pages/
│   ├── 1_Customer_Journey.py
│   ├── 2_Consultation_Analysis.py
│   ├── 3_Program_Performance.py
│   ├── 4_Success_&_Retention_Analysis.py
│   ├── 5_Revenue_&_Subscription_Analysis.py
│   ├── 6_Health_Outcomes.py
│   ├── 7_Advanced_Analysis.py
│   └── 8_Executive_Summary.py
│
├── sql/
│   ├── 01_DATABASE SETUP.sql
│   ├── 02_DATA QUALITY & VALIDATION.sql
│   ├── 03_CUSTOMER JOURNEY ANALYSIS.sql
│   ├── 04_CONSULTATION EFFECTIVENESS ANALYSIS.sql
│   ├── 05_PROGRAM PERFORMANCE ANALYSIS.sql
│   ├── 06_SUCCESS & RETENTION ANALYSIS.sql
│   ├── 07_REVENUE & SUBSCRIPTION  ANALYSIS.sql
│   ├── 08_HEALTH OUTCOME ANALYSIS.sql
│   └── 09_ADVANCED SQL INSIGHTS.sql
│
│── screenshots/
│
└── csv_datasets/
```

---

# 🗃️ SQL Analysis Files

| File                                  | Analysis                    |
| ------------------------------------- | --------------------------- |
| `01_DATABASE SETUP.sql`               | Database setup              |
| `02_DATA QUALITY & VALIDATION.sql`      | Data quality and validation |
| `03_CUSTOMER JOURNEY ANALYSIS.sql`      | Customer journey and funnel |
| `04_CONSULTATION EFFECTIVENESS ANALYSIS.sql`        | Consultation analysis       |
| `05_PROGRAM PERFORMANCE ANALYSIS.sql` | Program performance         |
| `06_SUCCESS & RETENTION ANALYSIS.sql`            | Success and retention       |
| `07_REVENUE & SUBSCRIPTION  ANALYSIS.sql`         | Revenue and subscription    |
| `08_HEALTH OUTCOME ANALYSIS.sql`              | Health outcomes             |
| `09_ADVANCED SQL INSIGHTS.sql`   | Advanced SQL analysis       |

> **Note:** Customer feedback is analyzed in the Streamlit dashboard. It is not included as a separate SQL analysis section.

---

# 🧠 SQL Concepts Demonstrated

* `SELECT`
* `WHERE`
* `GROUP BY`
* `ORDER BY`
* `HAVING`
* `CASE`
* `COUNT()`
* `COUNT(DISTINCT ...)`
* `SUM()`
* `AVG()`
* `ROUND()`
* Conditional aggregation
* Subqueries
* CTEs
* Window functions
* `ROW_NUMBER()`
* Ranking
* Joins
* Customer-level aggregation
* Data validation
* KPI calculations
* Customer segmentation

---

# 📈 SQL-First Dashboard Approach

The project follows a **SQL-first approach**.

Important numerical calculations are performed dynamically in SQL, including:

* Customer counts
* Completion rates
* Goal achievement rates
* Renewal rates
* Funnel metrics
* Program performance
* Adherence metrics
* Revenue
* Subscription metrics
* Weight and BMI changes
* Customer segmentation
* Rankings

Python retrieves the SQL results and uses them for dashboard display and visualization.

This keeps the dashboard connected to the database and reduces hardcoded calculations.

---

# ⚙️ Installation & Setup

## 1. Open the Project

Open the `Healthcare_Wellness_Analytics` folder in VS Code.

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```text
streamlit
pandas
plotly
mysql-connector-python
numpy
```

---

# 🗄️ Configure MySQL

Create the database in MySQL :

```sql
CREATE DATABASE patient_analysis;
```

The project uses the following tables:

> **Important:** These tables are imported into the database  using "MySQL Workbench Table Data Import Wzard"..



```text
customers
consultations
programs
health_measurements
feedback
subscriptions
```

The SQL files in the `sql/` folder contain the database setup documentation, validation queries, and analysis queries.

Start with:

```text
sql/01_DATABASE SETUP.sql
```

The Streamlit application connects to MySQL using:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="patient_analysis"
)
```

> **Important:** Write your actual MySQL password while running the dashboard..

---

# ▶️ Run the Dashboard

From the project root folder:

```bash
python -m streamlit run app.py
```

Streamlit automatically detects the `pages/` folder.


---

# 💡 Key Business Insights

The project provides insights into:

* Customer journey and funnel performance
* Consultation performance
* Program completion and goal achievement
* Customer adherence
* Customer feedback and ratings
* Subscription renewal
* Revenue contribution
* Weight and BMI changes
* Customer segmentation

---

# 🎯 Business Recommendations

Based on the analysis:

* Improve customer engagement throughout the program journey.
* Monitor adherence and identify lower-engagement customers.
* Use regular follow-ups to reduce program drop-offs.
* Analyze higher-performing programs.
* Strengthen engagement before subscription expiry.
* Use customer feedback to identify improvement opportunities.
* Monitor health outcomes alongside engagement and retention.
* Use customer segmentation for data-driven decisions.

---

# 📊 Portfolio Skills Demonstrated

### Data Analytics

* Business problem analysis
* KPI development
* Funnel analysis
* Program performance
* Retention analysis
* Revenue analysis
* Customer segmentation
* Feedback analysis
* Health outcome analysis

### SQL

* Data validation
* Aggregations
* Conditional logic
* CTEs
* Window functions
* Ranking
* Joins
* Segmentation
* KPI calculations

### Python

* MySQL connectivity
* Pandas
* Data processing
* Streamlit development

### Visualization

* Plotly charts
* KPI cards
* Funnel visualization
* Bar charts
* Line charts
* Distribution charts

---

# 📸 Dashboard Screenshots

Dashboard screenshots are stored in:

```text
screenshots/
```

---

# 📌 Project Purpose

This project demonstrates the complete analytics workflow:

```text
SQL
 ↓
Data Validation
 ↓
Business Analysis
 ↓
KPI Development
 ↓
Customer Insights
 ↓
Data Visualization
 ↓
Interactive Dashboard
```

It demonstrates practical use of **MySQL, SQL, Python, Pandas, Plotly, and Streamlit** for business analytics.

---

# ⚠️ Data Disclaimer

This project uses **synthetically generated data** for educational and portfolio purposes.

It does not represent real customers, patients, healthcare providers, or medical records.

No real personal or medical information is used.

---

# 👩‍💻 Author

**Riya Kapila**

B.Tech — Computer Science & Engineering

### Areas of Interest

* Data Analytics
* Business Analytics
* SQL
* Python
* Power BI
* Business Intelligence
