# The case

This project utilises data from yellow taxis ranging 2009 - 2024. The source of the data is the New York City
Government, who publicly releases this data from multiple different data vendors.

Source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

The data spans hundreds of millions of rows. This project was 

## Business case
> *Surfer* is a new ridesharing startup, trying to compete with Uber globally, who are currently headquartered in New York. They want to be growingly intentional about the trips they recommend to drivers, as they wish to maximise 
profits to increase funding.
>
> Surfer has tasked their sole data scientist to look through the available yellow taxi data to find statistical insights into profitability of taxi rides, and how they could be smarter about the trips they take. 

## (Non-exhaustive) Business requirements
1. Create **actionable and interpretable** insights into trip profitability. 
2. Determine **trends** regarding taxi and ridesharing earnings; including historical earnings shares, seasonality and more.
3. Design a **live algorithm/score** which predicts trip favourability for profits with strong out-of-sample performance.
4. Create models for tips, surge pricing and fare amounts.
frequency, expected profits and location.

## Technical requirements
1. Ensure data is clean and reliable. 
2. Apply appropiate statistical techniques that avoid overfitting. Justify on features, and make clear reference to model performance and assumption validation.
3. Base models on academic literature that exists for ridesharing/trip recommendation. Ensure strong out-of-sample performance.