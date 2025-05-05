# An investigation into 15 years of NYC taxi data.

Author: Haeohreum Kim

Date: 2025

---

This end-to-end data project considers a hypothetical business case of a company called `Surfer`, starting up a ride share business in NYC. 

This is a project with *lots* of data - we are talking millions and millions of taxi trips. I used this project as a way to teach myself more about how to apply machine learning techniques beyond linear regression, as well as outside of the domain of financial markets which is what I've become accustomed to.

[Read about the case and requirements](./business_case.md)

## Assumptions

There have been some assumptions made about the data (and my access to external information) to make the project interesting, and more akin to a real life business case.

[Assumptions](./assumptions.md)

## Data wrangling

### General data cleaning
[The data cleaning process](./ds-research/data/research/data_quality.ipynb)

[Understanding pickup and drop off locations](./ds-research/data/research/understanding_locations.ipynb)

### Inflation of currency/amount
[An investigation into inflation](./ds-research/data/research/inflation.ipynb)

### Fixed fare clustering
[An investigation into fixed fare clustering](./ds-research/data/research/fixed_fares.ipynb)

## Regression, feature creation and analytics

[Descriptive trends](./ds-research/research/descriptive_trends.ipynb)

[Predicting tips](./ds-research/research/tips.ipynb)

[Finding the fare rate](./ds-research/research/fare_amount.ipynb)

[Congestion multiplier](./ds-research/research/congestion.ipynb)

## Final model details

> The main goal of the project was to find:
> 1. A model for fares
> 2. A model for predicting total revenue from a trip
>
> Of course, a model for predicting total revenue from a trip will be a model for fares + tips and other expenses.

The fare model was comprised of two separate components:
1. A fare rate, which was calculated with a modified `quantile regression` on a 1 year lookback window of taxi data
2. A congestion multiplier, which caps at 2x, and used a hypothetical `congestion` feature to add multipliers into the fare

The *total revenue* model adds on top of this, a tip prediction model. The tip prediction model uses gradient-boosted decision trees (`XGBoost`) to capture non-linear behaviours around short and longer distance trips. 
