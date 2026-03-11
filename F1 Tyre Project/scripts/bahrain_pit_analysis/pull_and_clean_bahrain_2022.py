import fastf1
import pandas as pd
import os

# Set working directory to your project folder
os.chdir(r"C:\Users\harry\OneDrive\Desktop\F1 Tyre Project\scripts")

# Pull raw Norris data
fastf1.Cache.enable_cache('../data')

years = [2022,2023,2024,2025]

for year in years:
    print("\nProcessing Bahrain GP " + str(year) + "...")

    # Load Bahrain 2022 race session
    session = fastf1.get_session(year, 'Bahrain', 'R')
    session.load()

    # Get Norris lap data
    laps = session.laps

    # Clean the data

    # Remove the first lap as standing start
    laps = laps[laps['LapNumber'] > 1]

    # Keep only accurate laps (excluding SC, VSC, etc.)
    laps = laps[laps['IsAccurate']]

    # Remove in/out laps
    laps = laps[laps['PitInTime'].isna()]
    laps = laps[laps['PitOutTime'].isna()]

    # Convert LapTime to seconds - easier to compare
    laps['LapTimeSeconds'] = laps['LapTime'].dt.total_seconds()

    # Remove rows with missing lap times
    laps = laps.dropna(subset=['LapTimeSeconds'])

    # Reset index
    laps = laps.reset_index(drop=True)

    # Save cleaned dataset
    output_file = '../data/bahrain_' + str(year) + '_clean.csv'
    laps.to_csv(output_file, index = False)

    print(str(year) + " dataset saved to " + output_file)
    print("Total cleaned laps:", len(laps))
    print("Drivers in dataset:", laps['Driver'].unique())