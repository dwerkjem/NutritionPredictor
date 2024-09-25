import json


def find_json_error(file_path):
    """
    Tries to load the JSON file line by line or chunk by chunk to identify where the parsing error occurs.

    Parameters:
        file_path (str): Path to the JSON file.

    Returns:
        None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            json_data = file.read()

        # Try to load the entire file first
        json.loads(json_data)
        print("JSON is valid!")

    except json.JSONDecodeError as e:
        print(f"Error detected: {e}")
        print(f"Error at line: {e.lineno}, column: {e.colno}")

        # Now we try to identify the problem by reading line by line
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, 1):
                try:
                    json.loads(line)  # Try to load each line as JSON
                except json.JSONDecodeError as line_error:
                    print(f"Error in line {line_number}: {line_error}")
                    print(f"Problematic line: {line.strip()}")
                    break


# Example usage
find_json_error("brandedDownload.json")
