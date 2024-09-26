import requests
import dotenv
import pandas as pd
import os

# Load environment variables from a .env file (if applicable)
dotenv.load_dotenv()

# Path to your CSV file
csv_file_path = "branded_food.csv"  # Update this path if the file is located elsewhere

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

# Display the shape of the DataFrame
print(f"Data shape: {data.shape}")  # Outputs (number_of_rows, number_of_columns)
