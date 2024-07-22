import os
import glob
import pandas as pd
import json

def safe_extract_from_json(column, key):
    results = []
    for index, item in enumerate(column):
        try:
            # Ensure item is a string and replace Python 'None' with JSON 'null'
            item_str = str(item).replace('None', 'null').replace("'", '"')
            item_json = json.loads(item_str)  # Convert string to JSON
            extracted_value = item_json.get(key, '')  # Use empty string for missing keys
            results.append(extracted_value)
        except json.JSONDecodeError as e:
            print(f"Error in row {index} with item {item}: {e}")
            results.append('')  # Append an empty string if there is an error
    return results

# Define the directories
input_dir = '/excel_chunks/path'
output_dir = '/clean_chunks/path'

# List all Excel files in the input directory
excel_files = glob.glob(os.path.join(input_dir, '*.xlsx'))

# Process each file
for file_path in excel_files:
    # Load the data
    df = pd.read_excel(file_path)

    # Check if the expected columns exist to avoid KeyErrors
    expected_columns = ['links', 'source', 'title', 'published_at', 'body']
    if not all(column in df.columns for column in expected_columns):
        print(f"Missing one or more of the expected columns in {file_path}. Skipping this file.")
        continue

    # Apply the function to extract fields from JSON columns
    df['Link'] = safe_extract_from_json(df['links'], 'permalink')
    df['Source'] = safe_extract_from_json(df['source'], 'name')
    df['Domain'] = safe_extract_from_json(df['source'], 'domain')

    # Validate if there are any non-empty entries after processing
    if df[['Link', 'Source', 'Domain']].isnull().all().all():
        print(f"All entries in Link, Source, and Domain are empty after processing {file_path}. Review the original data.")

    # Select and rename the necessary columns
    final_df = df[['title', 'Link', 'Source', 'published_at', 'Domain', 'body']].copy()
    final_df.rename(columns={'published_at': 'Date', 'body': 'Snippet'}, inplace=True)

    # Construct the output file path and save the cleaned data
    base_name = os.path.basename(file_path)
    new_file_path = os.path.join(output_dir, f'cleaned_{base_name}')
    final_df.to_excel(new_file_path, index=False)

print("All files have been processed.")
