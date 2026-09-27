import os
import numpy as np
import pandas as pd
from faker import Faker

# ============================================================
# PATIENT JOURNEY ANALYTICS
# Synthetic Healthcare / Wellness Dataset
# ============================================================

# -----------------------------
# SETTINGS
# -----------------------------

NUM_CUSTOMERS = 20000

np.random.seed(42)
fake = Faker("en_IN")
Faker.seed(42)

DATA_FOLDER = "data"

# Create data folder automatically
os.makedirs(DATA_FOLDER, exist_ok=True)

print("\n==========================================")
print(" PATIENT JOURNEY DATASET GENERATOR")
print("==========================================\n")


# ============================================================
# 1. CUSTOMERS
# ============================================================

print("1/6 Creating customers...")

customer_ids = [f"C{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)]

cities = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Chandigarh",
    "Mohali",
    "Noida",
    "Gurugram",
    "Jaipur",
    "Lucknow",
    "Ludhiana"
]

genders = np.random.choice(
    ["Male", "Female"],
    size=NUM_CUSTOMERS,
    p=[0.45, 0.55]
)

ages = np.random.randint(18, 65, NUM_CUSTOMERS)

heights = np.round(
    np.random.normal(165, 10, NUM_CUSTOMERS),
    1
)

# Keep height realistic
heights = np.clip(heights, 145, 195)

weights = np.round(
    np.random.normal(75, 15, NUM_CUSTOMERS),
    1
)

weights = np.clip(weights, 45, 130)

bmi = np.round(
    weights / ((heights / 100) ** 2),
    1
)

customer_join_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2024-01-01", "2026-06-30"),
        NUM_CUSTOMERS
    )
)

customers = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Age": ages,
    "Gender": genders,
    "City": np.random.choice(cities, NUM_CUSTOMERS),
    "Height_cm": heights,
    "Initial_Weight_kg": weights,
    "Initial_BMI": bmi,
    "Join_Date": customer_join_dates
})

customers.to_csv(
    f"{DATA_FOLDER}/customers.csv",
    index=False
)

print(f"   Created {len(customers):,} customers")


# ============================================================
# 2. PROGRAM ENROLLMENT
# ============================================================

print("2/6 Creating program enrollment...")

program_names = [
    "Weight Management",
    "Diabetes Management",
    "PCOS Management",
    "Gut Health",
    "General Wellness"
]

program_prices = {
    "Weight Management": 5999,
    "Diabetes Management": 7999,
    "PCOS Management": 6999,
    "Gut Health": 4999,
    "General Wellness": 3999
}

programs = np.random.choice(
    program_names,
    NUM_CUSTOMERS,
    p=[0.35, 0.18, 0.15, 0.12, 0.20]
)

# Adherence is an important business variable.
# Higher adherence will influence later outcomes.

adherence = np.random.beta(5, 2, NUM_CUSTOMERS) * 100
adherence = np.round(adherence, 1)

# Introduce some low-adherence customers
low_adherence_indices = np.random.choice(
    NUM_CUSTOMERS,
    size=int(NUM_CUSTOMERS * 0.12),
    replace=False
)

adherence[low_adherence_indices] = np.round(
    np.random.uniform(20, 50, len(low_adherence_indices)),
    1
)

program_enrollment_dates = customer_join_dates + pd.to_timedelta(
    np.random.randint(0, 15, NUM_CUSTOMERS),
    unit="D"
)

# Program duration
duration_months = np.random.choice(
    [1, 3, 6, 12],
    NUM_CUSTOMERS,
    p=[0.10, 0.45, 0.35, 0.10]
)

# Probability of completing program increases with adherence
completion_probability = (
    0.15 + (adherence / 100) * 0.80
)

completed = np.random.random(NUM_CUSTOMERS) < completion_probability

# Goal achievement depends on adherence
goal_probability = (
    0.05 + (adherence / 100) * 0.85
)

goal_achieved = np.random.random(NUM_CUSTOMERS) < goal_probability

programs_df = pd.DataFrame({
    "Program_ID": [
        f"P{i:05d}" for i in range(1, NUM_CUSTOMERS + 1)
    ],
    "Customer_ID": customer_ids,
    "Program_Name": programs,
    "Enrollment_Date": program_enrollment_dates,
    "Duration_Months": duration_months,
    "Adherence_Percent": adherence,
    "Program_Completed": np.where(
        completed,
        "Yes",
        "No"
    ),
    "Goal_Achieved": np.where(
        goal_achieved,
        "Yes",
        "No"
    )
})

programs_df.to_csv(
    f"{DATA_FOLDER}/programs.csv",
    index=False
)

print(f"   Created {len(programs_df):,} program records")


# ============================================================
# 3. CONSULTATIONS
# ============================================================

print("3/6 Creating consultations...")

consultation_rows = []

consultation_types = [
    "Initial Consultation",
    "Diet Consultation",
    "Follow-up",
    "Progress Review",
    "Doctor Consultation",
    "Lifestyle Coaching"
]

consultation_modes = [
    "Online",
    "Phone",
    "In-Person"
]

consultation_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Missed",
    "Cancelled"
]

consultation_id = 1

for i in range(NUM_CUSTOMERS):

    # Higher adherence = more consultations
    base_consultations = int(
        1 + (adherence[i] / 20)
    )

    # Add some randomness
    number_of_consultations = max(
        1,
        int(
            np.random.normal(
                base_consultations,
                1.5
            )
        )
    )

    # Low-adherence customers are more likely to have fewer consultations
    if adherence[i] < 45:
        number_of_consultations = np.random.randint(1, 4)

    for j in range(number_of_consultations):

        consultation_date = (
            program_enrollment_dates[i]
            + pd.Timedelta(
                days=int(
                    np.random.randint(1, max(10, duration_months[i] * 30))
                )
            )
        )

        # High adherence = more likely to complete consultation
        if adherence[i] >= 70:
            status = np.random.choice(
                ["Completed", "Missed", "Cancelled"],
                p=[0.90, 0.07, 0.03]
            )
        elif adherence[i] >= 45:
            status = np.random.choice(
                ["Completed", "Missed", "Cancelled"],
                p=[0.70, 0.20, 0.10]
            )
        else:
            status = np.random.choice(
                ["Completed", "Missed", "Cancelled"],
                p=[0.45, 0.35, 0.20]
            )

        consultation_rows.append({
            "Consultation_ID": f"CON{consultation_id:06d}",
            "Customer_ID": customer_ids[i],
            "Consultation_Date": consultation_date,
            "Consultation_Type": np.random.choice(
                consultation_types
            ),
            "Mode": np.random.choice(
                consultation_modes
            ),
            "Status": status
        })

        consultation_id += 1


consultations_df = pd.DataFrame(
    consultation_rows
)

consultations_df.to_csv(
    f"{DATA_FOLDER}/consultations.csv",
    index=False
)

print(
    f"   Created {len(consultations_df):,} consultation records"
)


# ============================================================
# 4. HEALTH MEASUREMENTS
# ============================================================

print("4/6 Creating health measurements...")

measurement_rows = []

measurement_id = 1

for i in range(NUM_CUSTOMERS):

    # Number of measurements depends on adherence
    if adherence[i] >= 75:
        num_measurements = np.random.randint(3, 7)

    elif adherence[i] >= 50:
        num_measurements = np.random.randint(2, 5)

    else:
        num_measurements = np.random.randint(1, 3)

    start_weight = weights[i]

    for j in range(num_measurements):

        measurement_date = (
            program_enrollment_dates[i]
            + pd.Timedelta(
                days=int(j * 30 + np.random.randint(0, 10))
            )
        )

        # Weight loss depends on adherence
        progress_factor = (
            adherence[i] / 100
        )

        weight_loss = (
            j
            * np.random.uniform(0.5, 2.0)
            * progress_factor
        )

        current_weight = max(
            40,
            start_weight - weight_loss
        )

        current_weight = round(
            current_weight,
            1
        )

        current_bmi = round(
            current_weight /
            ((heights[i] / 100) ** 2),
            1
        )

        measurement_rows.append({
            "Measurement_ID": f"M{measurement_id:06d}",
            "Customer_ID": customer_ids[i],
            "Measurement_Date": measurement_date,
            "Weight_kg": current_weight,
            "BMI": current_bmi
        })

        measurement_id += 1


health_df = pd.DataFrame(
    measurement_rows
)

health_df.to_csv(
    f"{DATA_FOLDER}/health_measurements.csv",
    index=False
)

print(
    f"   Created {len(health_df):,} health measurements"
)


# ============================================================
# 5. FEEDBACK
# ============================================================

print("5/6 Creating customer feedback...")

feedback_rows = []

feedback_id = 1

# Not every customer gives feedback
feedback_customer_indices = np.random.choice(
    NUM_CUSTOMERS,
    size=int(NUM_CUSTOMERS * 0.75),
    replace=False
)

feedback_comments_good = [
    "Very helpful program",
    "Good guidance from the team",
    "I achieved my goal",
    "Excellent support",
    "Very satisfied",
    "Good experience",
    "The coach was helpful"
]

feedback_comments_bad = [
    "Could be better",
    "I missed some sessions",
    "Program was difficult to follow",
    "Need more follow-up",
    "Not fully satisfied",
    "Expected better results"
]

for i in feedback_customer_indices:

    # Goal achievement and adherence influence satisfaction
    if adherence[i] >= 75:

        rating = np.random.choice(
            [4, 5],
            p=[0.30, 0.70]
        )

    elif adherence[i] >= 50:

        rating = np.random.choice(
            [3, 4, 5],
            p=[0.30, 0.50, 0.20]
        )

    else:

        rating = np.random.choice(
            [1, 2, 3],
            p=[0.20, 0.45, 0.35]
        )

    if rating >= 4:
        comment = np.random.choice(
            feedback_comments_good
        )
    else:
        comment = np.random.choice(
            feedback_comments_bad
        )

    feedback_date = (
        program_enrollment_dates[i]
        + pd.Timedelta(
            days=int(
                np.random.randint(
                    30,
                    max(31, duration_months[i] * 30)
                )
            )
        )
    )

    feedback_rows.append({
        "Feedback_ID": f"F{feedback_id:06d}",
        "Customer_ID": customer_ids[i],
        "Feedback_Date": feedback_date,
        "Rating": rating,
        "Comment": comment
    })

    feedback_id += 1


feedback_df = pd.DataFrame(
    feedback_rows
)

feedback_df.to_csv(
    f"{DATA_FOLDER}/feedback.csv",
    index=False
)

print(
    f"   Created {len(feedback_df):,} feedback records"
)


# ============================================================
# 6. SUBSCRIPTIONS
# ============================================================

print("6/6 Creating subscriptions...")

subscription_rows = []

subscription_id = 1

for i in range(NUM_CUSTOMERS):

    program_name = programs[i]

    base_price = program_prices[
        program_name
    ]

    # Slight variation in pricing
    price = base_price + np.random.choice(
        [-500, 0, 0, 0, 500]
    )

    # Renewal probability depends on:
    # adherence + goal achievement + completion

    renewal_score = (
        adherence[i] * 0.5
        + (goal_achieved[i] * 25)
        + (completed[i] * 15)
    )

    # Convert to probability
    renewal_probability = min(
        0.90,
        max(
            0.05,
            renewal_score / 120
        )
    )

    renewed = (
        np.random.random()
        < renewal_probability
    )

    subscription_status = (
        "Renewed"
        if renewed
        else "Not Renewed"
    )

    total_revenue = price

    if renewed:

        renewal_months = np.random.choice(
            [1, 3, 6],
            p=[0.20, 0.50, 0.30]
        )

        renewal_revenue = (
            price * renewal_months
        )

        total_revenue += renewal_revenue

    else:

        renewal_months = 0

    subscription_rows.append({
        "Subscription_ID": f"S{subscription_id:06d}",
        "Customer_ID": customer_ids[i],
        "Program_Name": program_name,
        "Plan_Price": price,
        "Initial_Duration_Months": duration_months[i],
        "Renewed": subscription_status,
        "Renewal_Months": renewal_months,
        "Total_Revenue": total_revenue
    })

    subscription_id += 1


subscriptions_df = pd.DataFrame(
    subscription_rows
)

subscriptions_df.to_csv(
    f"{DATA_FOLDER}/subscriptions.csv",
    index=False
)

print(
    f"   Created {len(subscriptions_df):,} subscription records"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n==========================================")
print(" DATASET GENERATION COMPLETED!")
print("==========================================\n")

print("Files created:")

print(
    f"customers.csv              : {len(customers):,} rows"
)

print(
    f"programs.csv               : {len(programs_df):,} rows"
)

print(
    f"consultations.csv          : {len(consultations_df):,} rows"
)

print(
    f"health_measurements.csv    : {len(health_df):,} rows"
)

print(
    f"feedback.csv               : {len(feedback_df):,} rows"
)

print(
    f"subscriptions.csv          : {len(subscriptions_df):,} rows"
)

print("\nLocation:")
print(f"All files are inside: {DATA_FOLDER}/")

print("\n==========================================")
print(" Important:")
print("This is SYNTHETIC data.")
print("It is not real company/customer data.")
print("==========================================\n")