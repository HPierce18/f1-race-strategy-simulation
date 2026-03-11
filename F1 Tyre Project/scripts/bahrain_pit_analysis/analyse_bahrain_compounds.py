import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set working directory to your project folder
os.chdir(r"C:\Users\harry\OneDrive\Desktop\F1 Tyre Project\scripts")

print("Working dir:", os.getcwd())
print("Files in ../data:", os.listdir('../data'))

# Outline the parameters
years = [2022,2023,2024,2025]
total_laps = 57 # Laps at Bahrain GP
fuel_delta = 0.08 # Seconds per lap lost due to fuel consumption
track_delta = 0.015 # Seconds per lap lost due to track evolution
min_stint_laps = 4 # Ignore stints shorter than this

# Output folder
deg_folder = '../data/degradation_summaries'
figures_folder = '../figures'
os.makedirs(deg_folder, exist_ok = True)
os.makedirs(figures_folder, exist_ok = True)

# Loop over years

for year in years:
    print("\n=== Processing Bahrain GP", year, "===\n")
    
    # Load cleanes dataset
    laps = pd.read_csv('../data/bahrain_' + str(year) + '_clean.csv')
    laps['RaceLap'] = range(1, len(laps) + 1)

    # Get all drivers
    drivers = laps['Driver'].unique()

    # Loop over drivers
    for driver in drivers:
        print("Driver: " + driver)
        driver_laps = laps[laps['Driver'] == driver].copy()

        # Tyre age per stint
        driver_laps['TyreAge'] = driver_laps.groupby('Stint').cumcount() + 1

        # Remove outlying slow laps
        median_time = driver_laps['LapTimeSeconds'].median()
        driver_laps = driver_laps[driver_laps['LapTimeSeconds'] < median_time + 3]

        # Fuel and track correction
        driver_laps['CorrectedLapTime'] = driver_laps['LapTimeSeconds'] + (total_laps - driver_laps['RaceLap']) * fuel_delta + driver_laps['RaceLap'] * track_delta # add on the time lost to correct to isolate effects of tyre wear

        # Group by stint and compound
        grouped = driver_laps.groupby(['Stint', 'Compound'])
        deg_summary = []
        plt.figure(figsize=(10,6))

        for (stint,compound), group in grouped:
            # Skip very short stints
            if len(group) < min_stint_laps:
                continue

            group = group.reset_index(drop=True)
            x = group['TyreAge']
            y = group['CorrectedLapTime']

            # Fit a quadratic model
            coeffs = np.polyfit(x, y, 2)
            a, b, c = coeffs

            deg_summary.append({'Year': year, 'Driver': driver, 'Stint': stint, 'Compound': compound, 'a': a, 'b': b, 'c': c, 'Laps':len(group)})

            # Scatter plot of lap times
            plt.scatter(x, y, label='Stint ' + str(stint) + ' ' + compound)

            # Plot fitted quadratic curve
            tyre_range = np.linspace(x.min(), x.max(), 100)
            fitted_line = a*tyre_range**2 + b*tyre_range + c # Compute fitted quadratic values
            plt.plot(tyre_range, fitted_line, linestyle = '--') # Plot curve

        # Save ged summary csv

        deg_df = pd.DataFrame(deg_summary)
        if not deg_df.empty:
            output_file = deg_folder + '/' + driver + '_' + str(year) + '_deg_summary.csv'
            deg_df.to_csv(output_file, index=False)
            print("Saved degradation summary to " + output_file)

            # Save plot to figures
            plt.xlabel('Tyre Age (laps)')
            plt.ylabel('Corrected Lap Time (seconds)')
            plt.title(driver + 'Bahrain ' + str(year) + ' Tyre Degradation')
            plt.legend()
            plt.tight_layout()

            plot_file = figures_folder + '/' + driver + '_' + str(year) + '_tyre_deg.png'
            plt.savefig(plot_file)
            plt.close()
            print("Saved degradation plot to " + plot_file)