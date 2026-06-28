# f1-race-strategy-simulation
This project uses python and F1 lap time data from the Bahrian Grand Prix 2022-2025 to model tyre wear, fuel loads and track evolutionto find the optimal pit stategy at these races. This is done by finding the strategy that produces the lowest total race time.

## Project Goals
- Normalise lap time data to isolate effects of tyre wear by accounting for track evolution and fuel loss.
- Estimate the optimal pit laps for these races by finding the minimum race time from all possible strategies.
- Look at results from 2022-2025 to see if strategies have changed over the years and compare my results to real life strategy choices.

## Methods
- Python:
    - Pandas for data modelling
    - numpy for calculations
    - matplotlib for visualisation

## Status
- Strategy simulation has been completed and the results have been compared to real life race strategies.

## Conclusions
Overall, the simulation produced strategies that held a strong level of similarity to those chosen by Formula 1 teams. This shows that the modelling decisions made have been effective. In particular, in 2023, the simulation suggested SOFT-HARD-HARD for the optimal strategy, which matches the strategy that Max Verstappen used to win the 2023 Bahrain Grand Prix. In 2025, the simulation also correctly reproduced the SOFT–MEDIUM–MEDIUM strategy used by third-place finisher Lando Norris. Although the simulation did not produce the 1st-placed strategy for every year, it correctly identified the two-stop approach and realistic pit windows. The discrepancies are mainly due to factors not included in the model such as safety cars, traffic, changing race conditions and overtaking opportunities. Overall, these results show that a model based on tyre degradation, fuel loads and track evolution can reproduce the general trends found in Formula 1 strategy. This model also highlights the importance of incorporatinn other race-influencing factors when developing more sophisticated models, such as those used by Formula 1 teams.
