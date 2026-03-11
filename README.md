# f1-race-strategy-simulation
This project uses python and F1 lap time data from the Bahrian Grand Prix 2022-2025 to model tyre wear and find the optimal pit laps at these races. This is done by finding the strategy that produces the lowest total race time.

## Project Goals
- Normalise lap time data to isolate effects of tyre wear by accounting for track evolution and fuel loss.
- Estimate the optimal pit laps for these races by finding the minimum race time from all possible strategies.
- Look at results from 2022-2025 to see if strategies have changed over the years and compare my results to real life strategy and Pirelli's forecast strategies.

## Methods
- Python:
    - Pandas for data modelling
    - numpy for calculations
    - matplotlib for visualisation

## Status
- This project is currently in progress.
- So far I have cleaned the data and made the relevant adjustments.
- Completed inital tyre degradation analysis.
- Future work will include strategy simulation and pit strategy analysis.
