import pandas as pd
import numpy as np

# Define file paths
input_csv = "cleaned_openfoodfacts.csv"
output_csv = "data.csv"

# Define chunk size and sample size
chunk_size = 10_000
sample_size = 100_000

# Initialize reservoir for sampling
reservoir = []
current_count = 0

# Specify data types for problematic columns
dtype_spec = {
    "code": "str",
    "last_modified_datetime": "str",
    "brands_tags": "str",
    "emb_codes_tags": "str",
    "labels_tags": "str",
    "additives_tags": "str",
}

# Define critical columns to retain rows
critical_columns = ["code", "product_name", "brands"]

try:
    # Create an iterator for reading the CSV in chunks
    reader = pd.read_csv(
        input_csv,
        sep="\t",
        on_bad_lines="skip",  # Skip bad lines
        chunksize=chunk_size,
        dtype=dtype_spec,
        engine="python",  # Use python engine for robustness
    )

    for chunk_number, chunk in enumerate(reader, start=1):
        print(f"Processing chunk {chunk_number}...")

        # Drop rows where critical columns have missing values
        chunk = chunk.dropna(subset=critical_columns)

        valid_rows = len(chunk)
        print(f"Valid rows in chunk {chunk_number}: {valid_rows}")

        # Iterate over rows for reservoir sampling
        for _, row in chunk.iterrows():
            current_count += 1
            if len(reservoir) < sample_size:
                reservoir.append(row)
            else:
                # Randomly replace elements in the reservoir
                s = np.random.randint(0, current_count)
                if s < sample_size:
                    reservoir[s] = row

        print(f"Current reservoir size: {len(reservoir)}")

        # Stop if reservoir is filld
        if len(reservoir) >= sample_size:
            print("Reservoir filled. Stopping further processing.")
            break

    if not reservoir:
        print("No valid rows found after cleaning.")
    else:
        # Convert reservoir to DataFrame
        sampled_data = pd.DataFrame(reservoir)

        # Reset index
        sampled_data.reset_index(drop=True, inplace=True)

        # Save to CSV
        sampled_data.to_csv(output_csv, index=False)
        print(f"Sampled data saved to {output_csv} with {len(sampled_data)} rows.")

except pd.errors.EmptyDataError:
    print("The input CSV file is empty.")
except pd.errors.ParserError as e:
    print(f"ParserError: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
