import os
import pandas as pd

# Define the directory where the Excel files are located
input_directory = "Dist_exports_am24"  # Update this to the correct path
output_file = "dist_exports_am24.csv"

# Initialize an empty list to store DataFrames
dataframes = []

# Loop through each file in the directory
for file in os.listdir(input_directory):
    # Check if the file is an Excel file
    if file.endswith(".xlsx") or file.endswith(".xls"):
        file_path = os.path.join(input_directory, file)
        try:
            # Read the Excel file, skipping the first row and using the second row as headers
            df = pd.read_excel(file_path, header=1)  # `header=1` skips the first row (index 0) and uses the second row (index 1) as column names
            # Add the DataFrame to the list
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Concatenate all DataFrames into one
merged_df = pd.concat(dataframes, ignore_index=True)

# Export the merged DataFrame to a CSV file
merged_df.to_csv(output_file, index=False)

print(f"All files merged into {output_file}")
