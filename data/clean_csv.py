# clean_csv.py
import pandas as pd
import csv

input_csv = "openfoodfacts.csv"
intermediate_csv = "intermediate_cleaned.csv"
final_cleaned_csv = "cleaned_openfoodfacts.csv"

try:
    # First Pass: Remove lines with unmatched quotes
    with open(input_csv, "r", encoding="utf-8") as fin, open(
        intermediate_csv, "w", encoding="utf-8", newline=""
    ) as fout:
        inside_quote = False
        for line_number, line in enumerate(fin, start=1):
            quote_count = line.count('"')
            if quote_count % 2 != 0:
                # Toggle the inside_quote flag
                inside_quote = not inside_quote
                print(f"Unmatched quote at line {line_number}. Skipping this line.")
                continue  # Skip lines with unmatched quotes
            fout.write(line)

    # Second Pass: Use pandas to further clean the CSV
    df = pd.read_csv(
        intermediate_csv,
        sep="\t",
        on_bad_lines="skip",
        quoting=csv.QUOTE_NONE,
        escapechar="\\",
        engine="python",
        dtype=str,  # Read all columns as strings to prevent dtype issues
    )

    # Save the cleaned CSV
    df.to_csv(final_cleaned_csv, sep="\t", index=False)
    print(f"Final cleaned CSV saved as '{final_cleaned_csv}'.")

except Exception as e:
    print(f"An error occurred during CSV cleaning: {e}")
