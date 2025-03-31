##########################
# Allan V. Aquino Vieira #
##########################

import os
import sys
import json
import csv
import argparse


def parse_arguments():
    """
    Parse the command line arguments provided by the user.

    Required arguments:
      -f : The filename of the JSON file containing a list of JSON objects.
      -n : An integer indicating the expected number of JSON keys.
      -k : A comma-separated list of JSON keys to extract from each object.

    Optional arguments:
      -c : If present, the program will output a CSV file instead of a JSON file.

    If any required argument is missing, argparse will automatically display a usage 
    message and exit.
    """
    parser = argparse.ArgumentParser(
        description="Extract a subset of keys from a JSON list file and output as JSON or CSV."
    )
    parser.add_argument(
        "-f", required=True,
        help="Filename of the JSON file (located in the same directory as this program)."
    )
    parser.add_argument(
        "-n", type=int, required=True,
        help="An integer indicating the number of JSON keys to extract."
    )
    parser.add_argument(
        "-k", required=True,
        help="Comma-separated JSON keys to extract (e.g., key1,key2,...)."
    )
    parser.add_argument(
        "-c", action="store_true",
        help="Optional flag: if provided, output will be in CSV format instead of JSON."
    )
    return parser.parse_args()


def load_json_file(filename):
    """
    Load and return the JSON data from the specified file.

    This function checks if the file exists in the same directory as the script,
    then reads the file and attempts to load it as JSON.

    Parameters:
        filename (str): The name of the JSON file.

    Returns:
        A Python object representing the JSON data if successful.

    If the file is not found or the JSON is invalid, the function prints an error
    message ("JSON FILE NOT FOUND!") and exits the program.
    """
    # Get the directory where this script is located.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    # Check if the file exists
    if not os.path.isfile(filepath):
        print("JSON FILE NOT FOUND!")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception:
        print("JSON FILE NOT FOUND!")
        sys.exit(1)

    return data


def extract_keys(data, keys):
    """
    Create a new list of JSON objects that contain only the specified keys.

    This function iterates over the list of JSON objects (dictionaries) in 'data'
    and builds a new dictionary for each object that includes only the requested keys.

    If any JSON object does not contain one of the specified keys, the function prints
    "Requested KEY(s) not present in input file!" and exits.

    Parameters:
        data (list): A list of dictionaries representing JSON objects.
        keys (list): A list of keys to extract from each JSON object.

    Returns:
        A new list of dictionaries with only the specified keys.
    """
    subset = []
    for item in data:
        if not isinstance(item, dict):
            print("JSON FILE NOT FOUND!")
            sys.exit(1)
        # Ensure every requested key is present in the JSON object.
        for key in keys:
            if key not in item:
                print("Requested KEY(s) not present in input file!")
                sys.exit(1)
        # Build the new dictionary containing only the requested keys.
        new_item = {key: item[key] for key in keys}
        subset.append(new_item)
    return subset


def output_json(data, output_filename="json_output.json"):
    """
    Write the given data to a JSON file with pretty-print formatting.

    Parameters:
        data: The Python object (usually a list of dictionaries) to write as JSON.
        output_filename (str): The name of the output JSON file.
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)
        print(f"JSON output written to {output_filename}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")
        sys.exit(1)


def output_csv(data, keys, output_filename="json_output.csv"):
    """
    Write the given data to a CSV file.

    Each JSON key is used as a column header. Each JSON object in the list corresponds
    to a row in the CSV file.

    Parameters:
        data (list): The list of dictionaries to write to CSV.
        keys (list): The column headers (i.e., the JSON keys).
        output_filename (str): The name of the output CSV file.
    """
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV output written to {output_filename}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)


def main():
    """
    Main function that ties together the argument parsing, file reading, key extraction,
    and output formatting.

    This function performs the following steps:
      1. Parses the command line arguments.
      2. Validates that the number of keys provided (-k) matches the expected count (-n).
      3. Loads the JSON file from the current directory.
      4. Verifies that the JSON data is a list of objects.
      5. Extracts only the specified keys from each JSON object.
      6. Outputs the result either as a JSON file (json_output.json) or a CSV file 
         (json_output.csv) based on the presence of the -c flag.
    """
    # Parse command line arguments.
    args = parse_arguments()

    # Split the keys from the -k flag by commas and remove extra whitespace.
    keys = [key.strip() for key in args.k.split(",") if key.strip()]

    # Verify that the number of keys provided matches the -n argument.
    if len(keys) != args.n:
        print("Number of keys provided does not match the -n argument!")
        sys.exit(1)

    # Load the JSON data from the specified file.
    data = load_json_file(args.f)

    # Ensure that the loaded data is a list of JSON objects.
    if not isinstance(data, list):
        print("JSON FILE NOT FOUND!")
        sys.exit(1)

    # Extract only the requested keys from each JSON object.
    subset_data = extract_keys(data, keys)

    # Output the data in the requested format: CSV if -c flag is provided; otherwise JSON.
    if args.c:
        output_csv(subset_data, keys)
    else:
        output_json(subset_data)


if __name__ == "__main__":
    main()
