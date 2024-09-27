import requests
import dotenv
import pandas as pd
import os
from scipy import stats
import numpy as np

# Load environment variables
dotenv.load_dotenv()

# Path to CSV
csv_file_path = "branded_food.csv"

# Check file existence
if not os.path.isfile(csv_file_path):
    raise FileNotFoundError(f"The file {csv_file_path} does not exist.")

# Load data
try:
    data = pd.read_csv(csv_file_path)
    print("Data loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the data: {e}")
    raise

print(f"Data shape: {data.shape}")

# 1. Inspect Data Types
print("\n--- Data Types ---")
print(data.dtypes)

# Convert specific columns if necessary
# Example: data['price'] = pd.to_numeric(data['price'], errors='coerce')

# 2. Check for Missing Values
print("\n--- Missing Values ---")
missing_values = data.isnull().sum()
print(missing_values)
missing_percentage = (missing_values / len(data)) * 100
print("\n--- Percentage of Missing Values ---")
print(missing_percentage)

# Handle missing values (Example: Fill numerical with mean, categorical with mode)
numerical_cols = data.select_dtypes(include=[np.number]).columns
categorical_cols = data.select_dtypes(include=["object", "category"]).columns

for col in numerical_cols:
    if data[col].isnull().sum() > 0:
        data[col].fillna(data[col].mean(), inplace=True)

for col in categorical_cols:
    if data[col].isnull().sum() > 0:
        data[col].fillna(data[col].mode()[0], inplace=True)

# 3. Identify Duplicates
print("\n--- Duplicates ---")
duplicate_rows = data.duplicated().sum()
print(f"Number of duplicate rows: {duplicate_rows}")

if duplicate_rows > 0:
    data = data.drop_duplicates()
    print(f"Data shape after removing duplicates: {data.shape}")

# 4. Summary Statistics
print("\n--- Summary Statistics ---")
print(data.describe())

# 5. Detect Outliers using Z-Score
print("\n--- Detecting Outliers with Z-Score ---")
z_scores = np.abs(stats.zscore(data.select_dtypes(include=[np.number])))
threshold = 3
outliers = (z_scores > threshold).any(axis=1)
print(f"Number of outliers: {outliers.sum()}")

# Optionally remove outliers
data = data[~outliers]
print(f"Data shape after removing outliers: {data.shape}")

# 6. Validate Categorical Data
print("\n--- Categorical Data Validation ---")
for col in categorical_cols:
    unique_vals = data[col].unique()
    print(f"\nUnique values in '{col}':\n", unique_vals)
    # Example: Standardize to lowercase
    data[col] = data[col].str.lower()
    # Example: Replace known inconsistencies
    # data[col] = data[col].replace({'old_value': 'new_value'})

# 7. Ensure Data Consistency and Integrity
print("\n--- Data Consistency Checks ---")
# Example: Date consistency
if "manufacture_date" in data.columns and "expiry_date" in data.columns:
    data["manufacture_date"] = pd.to_datetime(data["manufacture_date"], errors="coerce")
    data["expiry_date"] = pd.to_datetime(data["expiry_date"], errors="coerce")
    invalid_dates = data[data["expiry_date"] < data["manufacture_date"]]
    print(f"Records with expiry_date before manufacture_date: {invalid_dates.shape[0]}")
    # Remove invalid dates
    data = data[data["expiry_date"] >= data["manufacture_date"]]

# Example: Logical numerical relationships
if "calories" in data.columns:
    negative_calories = data[data["calories"] < 0].shape[0]
    print(f"Records with negative calories: {negative_calories}")
    # Remove negative calories
    data = data[data["calories"] >= 0]

print("\n--- Final Data Shape ---")
print(data.shape)
