import pandas as pd
import os
import glob

def combine_stocks():
    # Directory path containing CSV files
    directory_path = r".\CSV Files"

    # Get a list of all CSV files in the specified directory
    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))

    # Sort the CSV files based on last modified time
    csv_files.sort(key=os.path.getmtime)

    # Read the columns from the first CSV file to use as header
    with open(csv_files[0], 'r') as first_csv:
        header = first_csv.readline().strip()

    # Create an empty list to hold DataFrames
    data_frames = []

    # Loop through the sorted CSV files and append the data to the list of DataFrames
    for csv_file in csv_files:
        df_data = pd.read_csv(csv_file, skiprows=1, header=None)  # Read with header
        data_frames.append(df_data)

    # Concatenate the list of DataFrames into a single DataFrame
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Set the header using the columns from the first CSV file
    combined_data.columns = header.split(',')

    # Save the combined data to a new CSV file
    combined_data.to_csv('stock_data.csv', index=False)
