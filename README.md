#json-list-of-objects-key-extractor

json-list-of-objects-key-extractor is a command-line Python utility that extracts a specified subset of keys from a JSON file containing a list of objects. The tool validates its inputs, checks that the file exists and is properly formatted, and then creates a new output file containing only the requested key/value pairs. By default, the output is written as a JSON file, but you can optionally output the data as a CSV file.

##Features
	+	Input Validation:
Ensures that the JSON file exists in the same directory as the script and that it contains a list of JSON objects.
	+	Customizable Key Extraction:
Extract only the keys you specify via command-line arguments.
	+	Flexible Output Formats:
Generates output in JSON format by default or in CSV format if the -c flag is provided.
	+	Robust Error Handling:
Provides descriptive error messages for missing arguments, file not found, incorrect JSON structure, and missing keys.

##Prerequisites
	+	Python 3.x
	+	Standard Python libraries: os, sys, json, csv, and argparse
 
##Usage

Run the script from the command line with the following required flags:
	+	-f: The filename of the JSON file (located in the same directory as the script).
	+	-n: An integer indicating the number of JSON keys to extract.
	+	-k: A comma-separated list of JSON keys to extract.
	+	-c: (Optional) If provided, output will be in CSV format; if omitted, output will be in JSON format.

Example

To extract the keys domain, reseller, and description from domain_list.json and output the result as CSV, run:
> python3 json-list-of-objects-key-extractor.py -f domain_list.json -n 3 -k domain,reseller,description -c

For JSON output, omit the -c flag:
> python3 json-list-of-objects-key-extractor.py -f domain_list.json -n 3 -k domain,reseller,description

##Output
	+	JSON Output:
      The default output is written to json_output.json.
	+	CSV Output:
      When the -c flag is provided, the output is written to json_output.csv with each JSON key as a column header and one row per JSON object.

##Error Handling
	+	If required arguments are missing, the program prints a message specifying the missing flag and what is expected.
	+	If the JSON file does not exist or is not formatted correctly (i.e., not a list of JSON objects), the program prints "JSON FILE NOT FOUND!" and exits.
	+	If any of the specified keys are not present in one or more JSON objects, the program prints "Requested KEY(s) not present in input file!" and exits.

##License

This project is licensed under the MIT License.
