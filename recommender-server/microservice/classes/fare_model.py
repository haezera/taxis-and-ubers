import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np

# Found in research
OUTLIER_FARE_AMOUNT = 3

class FareModel:
    def __init__(self, data: pd.DataFrame):
        self.fare_and_distance = data.copy()
        self.fare_and_distance['fare/distance'] = (self.fare_and_distance['fare_amount'] / self.fare_and_distance['trip_distance'])
        self.fare_and_distance = self.fare_and_distance[
            self.fare_and_distance['fare_amount'] >= OUTLIER_FARE_AMOUNT
        ]

    def fit(self):
        lower_quantile_data = self.fare_and_distance[
            self.fare_and_distance['fare/distance'] <= self.fare_and_distance['fare/distance'].quantile(0.03)
        ]
        X = sm.add_constant(lower_quantile_data['trip_distance'])
        y = lower_quantile_data['fare_amount']
        self.X = X
        self.Y = y
        model = sm.OLS(X, y).fit()
        self.params = model.params.values

    def plot_fit(self):
        if not hasattr(self, 'model'):
            raise Exception("Model not trained yet. Call .fit() first!")
        
        plot_input = np.linspace(self.fare_and_distance['fare_amount'].min(), self.fare_and_distance['fare_amount'].max(), 500)
        plot_output = plot_input * self.params[1] + self.params[0]

        plt.figure(figsize=(10, 6))
        plt.scatter(self.fare_and_distance['trip_distance'], self.fare_and_distance['fare_amount'])
        plt.plot(plot_input, plot_output)

    def predict(self, trip_distance: float):
        return self.params[1] * trip_distance + self.params[0]
