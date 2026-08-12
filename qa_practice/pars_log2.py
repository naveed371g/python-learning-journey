# This Python script extracts specific error lines and relevant timestamps from a system log file,
# saving them to a results file. It uses Regular Expressions (Regex) to reliably locate and pull
# out the exact data you need for your testing validations.

import re


def extract_log_data(log_file_path, output_file_path, search_keyword):
    # Regex pattern to find the keyword and extract the timestamp + message
    # Customize the timestamp part of the pattern to match your specific log format
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?(' + \
        re.escape(search_keyword) + r'.*)'

    matches_found = 0

    try:
        with open(log_file_path, 'r') as log_file, open(output_file_path, 'w') as out_file:
            for line in log_file:
                match = re.search(pattern, line)
                if match:
                    timestamp = match.group(1)
                    message = match.group(2)

                    # Format and write the extracted data to the new file
                    out_file.write(f"[{timestamp}] - {message}\n")
                    matches_found += 1

        print(
            f"Extraction complete. Found {matches_found} matches. Saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{log_file_path}' was not found.")


# --- How to run the script ---
if __name__ == "__main__":
    # Define your file paths and the keyword you are searching for
    LOG_FILE = 'system_server.log'
    RESULTS_FILE = 'extracted_errors.txt'
    KEYWORD = 'ERROR'

    extract_log_data(LOG_FILE, RESULTS_FILE, KEYWORD)
