# An investigation 15 years of NYC taxi data.

Author: Haeohreum Kim

Date: 2025

---

This end-to-end data project considers a hypothetical business case of a company called `Surfer`, starting up a ride share business in NYC. 

This is a project with *lots* of data - we are talking millions and millions of taxi trips. I used this project as a way to teach myself more about how to apply machine learning techniques beyond linear regression, as well as outside of the domain of financial markets which is what I've become accustomed to.

[Read about the case and requirements](./business_case.md)

## Read the full paper/report here

## Assumptions

There have been some assumptions made about the data (and my access to external information) to make the project interesting, and more akin to a real life business case.

[Assumptions](./assumptions.md)

## Data wrangling

### General data cleaning
[The data cleaning process](./data/research/data_quality.ipynb)

[Understanding pickup and drop off locations](./data/research/understanding_locations.ipynb)

### Inflation of currency/amount
[An investigation into inflation](./data/research/inflation.ipynb)

### Fixed fare clustering
[An investigation into fixed fare clustering](./data/research/fixed_fares.ipynb)

## Regression, feature creation and analytics

[Descriptive trends](./research/descriptive_trends.ipynb)

[Predicting tips](./research/tips.ipynb)

[Finding the fare rate](./research/fare_amount.ipynb)

[Congestion multiplier](./research/congestion.ipynb)

