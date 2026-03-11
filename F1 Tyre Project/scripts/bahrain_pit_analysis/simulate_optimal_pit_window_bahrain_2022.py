import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
import os

# Parameters
total_laps = 57
pit_stop_time = 22 # seconds per pit stop
compounds = ['SOFT', 'MEDIUM', 'HARD']
max_laps = {'SOFT': 14, 'MEDIUM': 25, 'HARD': 33}

# Years to simulate
years = [2022, 2023, 2024, 2025]

data_folder = '../data'
figures_folder = '../figures'

if not os.path.exists(figures_folder):
    os.makedirs(figures_folder)

# Function to compute stint time using quadratic deg model
def stint_time(a, b, c, start_lap, laps_in_stint):
    total = 0
    for i in range(laps_in_stint):
        tyre_age = i + 1
        lap_time = a*tyre_age**2 + b*tyre_age + c
        total += lap_time
    return total

# Check is sequence can cover total laps
def Possible_sequence(seq):
    return sum(max_laps[c] for c in seq) >= total_laps

# Simulation loop per year
for year in years:
    print("\n=== Processing Bahrain GP {} ===".format(year))

    deg_file = os.path.join(data_folder, 'degradation_summaries', 'bahrain_{}_degradation_summary.csv'.format(year))
    deg = pd.read_csv(deg_file)

    coeffs_avg = {}
    for c in compounds:
        comp_data = deg[deg['Compound'] == c]
        coeffs_avg[c] = {'a': comp_data['a'].mean(), 'b':comp_data['b'].mean(), 'c': comp_data['c'].mean()}

    # Generate all possible strategy sequences
    one_stop_sequences = [seq for seq in product(compounds, repeat=2) if possible_sequences(seq)]
    two_stop_sequences = [seq for seq in product(compounds, repeat=3) if possible_sequences(seq)]
    all_sequences = one_stop_sequences + two_stop_sequences

    results = []

    # Function to simulate optimal strategy
    def simulate_strategy(seq):
        best_total_time = None
        best_pits = None

        for pit1 in range(5, total_laps - 5):
            # One stop
            if len(seq) == 2:
                laps1 = pit1
                laps2 = total_laps - laps1
                if laps1 > max_laps[seq[0]] or laps2 > max_laps[seq[1]]:
                    continue
                t1 = stint_time(**coeffs_avg[seq[0]], start_lap = 1, laps_in_stint=laps1)
                t2 = stint_time(**coeffs_avg[seq[1]], start_lap = laps1 + 1, laps_in_stint=laps2)
                total_time = t1 + t2 + pit_stop_time
                if best_total_time is None or total_time < best_total_time:
                    best_total_time = total_time
                    best_pits = [laps1]

            # Two stop
            if len(seq) == 3:
                for pit2 in range(pit1+5, total_laps - 5):
                    laps1 = pit1
                    laps2 = pit2 - pit1
                    laps3 = total_laps - laps1 - laps2
                    if laps3 <= 0:
                        continue
                    if laps1 > max_laps[seq[0]] or laps2 > max_laps[seq[1]] or laps3 > max_laps[seq[2]]:
                        continue
                    t1 = stint_time(**coeffs_avg[seq[0]], start_lap=1, laps_in_stint=laps1)
                    t2 = stint_time(**coeffs_avg[seq[1]], start_lap=laps1+1, laps_in_stint=laps2)
                    t3 = stint_time(**coeffs_avg[seq[2]], start_lap=laps1+laps2+1, laps_in_stint=laps3)
                    total_time = t1 + t2 + t3 + pit_stop_time*2
                    if best_total_time is None or total_time < best_total_time:
                        best_total_time = total_time
                        best_pits = [laps1, laps1 + laps2]
        return best_total_time, best_pits
    
    # Run simulation
    for seq in all_sequences:
        total_time, pits = simulate_strategy(seq)
        if total_time is not None:
            results.append({'Strategy': seq, 'PitLaps': pits, 'TotalTime': round(total_time, 2)})
    
    results_df = pd.DataFrame(results).sort_values('TotalTime').reset_index(drop=True)
    print("Top 5 strategies for {}:".format(year))
    print(results_df.head())

    # Save to csv
    results_df.to_csv(os.path.join(data_folder, 'bahrain_{}_strategy_simulation.csv'.format(year)), index = False)

    # Plot best strategy stints
    best = results_df.iloc[0]
    seq = best['Strategy']
    pit_laps = best['PitLaps']
    stint_laps = [pit_laps[0]] + [pit_laps[i +1] - pit_laps[i] for i in range(len(pit_laps)-1)] + [total_laps - pit_laps[-1]] if len(pit_laps) > 1 else [pit_laps[0], total_laps - pit_laps[0]]

    plt.figure(figsize=(10,5))
    lap_start = 1
    for i, (c, laps_in_stint) in enumerate(zip(seq, stint_laps)):
        laps_range = np.arange(lap_start, lap_start+laps_in_stint)
        a,b,c_quad = coeffs_avg[c]['a'], coeffs_avg[c]['b'], coeffs_avg[c]['c']
        lap_times = a*(np.arange(1,laps_in_stint+1))**2 + b*(np.arange(1,laps_in_stint+1)) + c_quad
        plt.plot(laps_range, lap_times, label="Stint {} - {}".format(i+1, c))
        lap_start += laps_in_stint
    plt.xlabel("Race Lap")
    plt.ylabel("Lap Time (s)")
    plt.title("Best Strategy - Bahrain {} (Generic)".format(year))
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(figures_folder, 'bahrain_{}_best_strategy.png'.format(year)))
    plt.close()

    print("Simulation and plot saved for {}\n".format(year))