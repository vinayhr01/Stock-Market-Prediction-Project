import pandas as pd
import os
import glob

def combine_stocks():
    # Directory path containing CSV files
    directory_path = r"C:\Users\1rn19\Desktop\stock-market-prediction\CSV Files"

    # Get a list of all CSV files in the specified directory
    csv_files = glob.glob(os.path.join(directory_path, '*.csv'))

    # Sort the CSV files based on last modified time
    csv_files.sort(key=os.path.getmtime)

    # Read the columns from the first CSV file
    with open(csv_files[0], 'r') as first_csv:
        columns = first_csv.readline().strip().split(',')[:8]  # Keep only the first 7 columns

    # Create an empty list to hold DataFrames
    data_frames = []

    # Loop through the sorted CSV files and append the first 7 columns to the list of DataFrames
    for csv_file in csv_files:
        df_data = pd.read_csv(csv_file, usecols=range(8), header=None, skiprows=1)  # Read without header
        data_frames.append(df_data)

    # Concatenate the list of DataFrames into a single DataFrame
    combined_data = pd.concat(data_frames, ignore_index=True)

    # Add the columns to the combined DataFrame
    combined_data.columns = columns

    # Save the combined data to a new CSV file
    combined_data.to_csv('combined_stocks.csv', index=False)