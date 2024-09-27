import pandas as pd
import dotenv
import os

# Load environment variables (if applicable)
dotenv.load_dotenv()

# Path to your CSV file
csv_file_path = "branded_food.csv"

# Check if the file exists
if not os.path.isfile(csv_file_path):
    raise FileNotFoundError(f"The file {csv_file_path} does not exist.")

# Load the CSV data into a pandas DataFrame
try:
    data = pd.read_csv(csv_file_path)
    print("Data loaded successfully.")
except Exception as e:
    print(f"An error occurred while loading the data: {e}")
    raise

# Calculate the percentage of missing values per column
missing_percentage = (data.isnull().sum() / len(data)) * 100
print("\n--- Percentage of Missing Values ---")
print(missing_percentage)

# Define the threshold for missing values
threshold = 90  # in percentage

# Identify columns to drop
columns_to_drop = missing_percentage[missing_percentage > threshold].index
print("\nColumns to be dropped (>90% missing values):")
print(columns_to_drop.tolist())

# Drop the columns with >90% missing values
data_cleaned = data.drop(columns=columns_to_drop)
print(f"\nData shape after dropping columns: {data_cleaned.shape}")

# Define the path for the cleaned CSV
cleaned_csv_path = "branded_food_cleaned.csv"

# Save the cleaned DataFrame to a new CSV
data_cleaned.to_csv(cleaned_csv_path, index=False)
print(f"\nCleaned data saved to '{cleaned_csv_path}'.")
