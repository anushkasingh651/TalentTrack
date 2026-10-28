import random
from pathlib import Path
from datetime import date, timedelta

import pandas as pd

# Reproducible fictional data
random.seed(42)

# Project directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Recruitment dataset configuration
roles = [
    "Data Analyst",
    "Software Engineer",
    "Recruitment Intern",
    "Business Analyst",
    "Finance Analyst",
]

locations = [
    "Delhi NCR",
    "Bengaluru",
    "Mumbai",
    "Pune",
    "Hyderabad",
]

sources = [
    "Company Database",
    "LinkedIn",
    "Job Portal",
    "Employee Referral",
    "Campus Hiring",
]

stages = [
    "New",
    "Contacted",
    "Interested",
    "Screening",
    "Shortlisted",
    "Interview Scheduled",
    "Interview Completed",
    "Selected",
    "Rejected",
]

stage_weights = [10, 14, 12, 13, 12, 12, 9, 5, 13]

contact_statuses = [
    "Not Contacted",
    "Contacted",
    "Responded",
    "No Response",
]

records = []
today = date.today()

# Generate 500 fictional candidate records
for i in range(1, 501):
    application_date = today - timedelta(
        days=random.randint(0, 60)
    )

    stage = random.choices(
        stages,
        weights=stage_weights,
        k=1,
    )[0]

    contact_status = random.choice(contact_statuses)

    # Keep contact status consistent with later recruitment stages
    if stage in [
        "Interested",
        "Screening",
        "Shortlisted",
        "Interview Scheduled",
        "Interview Completed",
        "Selected",
    ]:
        contact_status = "Responded"

    interview_date = ""
    interview_status = "Not Scheduled"

    if stage == "Interview Scheduled":
        interview_date = (
            today + timedelta(days=random.randint(1, 10))
        ).isoformat()
        interview_status = "Scheduled"

    elif stage == "Interview Completed":
        interview_date = (
            today - timedelta(days=random.randint(0, 10))
        ).isoformat()
        interview_status = "Completed"

    elif stage == "Selected":
        interview_date = (
            today - timedelta(days=random.randint(1, 15))
        ).isoformat()
        interview_status = "Completed"

    follow_up_date = (
        application_date
        + timedelta(days=random.randint(1, 7))
    )

    records.append(
        {
            "Candidate ID": f"TT{i:04d}",
            "Job Role": random.choice(roles),
            "Location": random.choice(locations),
            "Application Date": application_date.isoformat(),
            "Source": random.choice(sources),
            "Recruitment Stage": stage,
            "Contact Status": contact_status,
            "Interview Date": interview_date,
            "Interview Status": interview_status,
            "Follow-up Date": follow_up_date.isoformat(),
        }
    )

# Create the DataFrame
df = pd.DataFrame(records)

# Remove duplicates and validate required fields
df.drop_duplicates(subset=["Candidate ID"], inplace=True)

required_columns = [
    "Candidate ID",
    "Job Role",
    "Application Date",
    "Recruitment Stage",
    "Contact Status",
]

df.dropna(subset=required_columns, inplace=True)

# Save the dataset
output_path = DATA_DIR / "candidates.csv"
df.to_csv(output_path, index=False)

# Display summary
print("\n" + "=" * 45)
print("  TALENTTRACK DATA GENERATOR")
print("=" * 45)
print(f"\nDataset created: {output_path}")
print(f"Total candidate records: {len(df)}")

print("\nCandidates by recruitment stage:")
print(df["Recruitment Stage"].value_counts().to_string())

print("\nCandidates by job role:")
print(df["Job Role"].value_counts().to_string())

print("\nData validation:")
print(f"Duplicate candidate IDs: {df['Candidate ID'].duplicated().sum()}")
print(f"Missing required values: {df[required_columns].isna().sum().sum()}")

print("\nDataset generation completed successfully!")
print("=" * 45)

