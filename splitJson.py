import pandas as pd
import os

# Correct the file paths
json_file_path = 'json/file/path'
output_folder = 'output/file/path'

# Ensure the output directory exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Function to read a large JSON file in chunks and convert each to an Excel file
def convert_json_to_excel_chunks(file_path, chunk_size=1000):
    chunk_number = 0
    try:
        reader = pd.read_json(file_path, lines=True, chunksize=chunk_size)
        for chunk in reader:
            # Convert timezone-aware datetimes to timezone-naive
            for col in chunk.select_dtypes(include=['datetime64[ns, UTC]']).columns:
                chunk[col] = chunk[col].dt.tz_localize(None)

            chunk_number += 1
            output_file_path = os.path.join(output_folder, f'chunk_{chunk_number}.xlsx')
            chunk.to_excel(output_file_path, index=False)
            print(f'Chunk {chunk_number} has been written to {output_file_path}')
    except ValueError as e:
        print(f'Error reading the JSON file: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


# Convert the JSON file into multiple Excel files
convert_json_to_excel_chunks(json_file_path)
