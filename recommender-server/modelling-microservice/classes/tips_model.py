import xgboost as xgb
from scipy.stats import zscore
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

class TipsModel:
    """
    Class which calculates
    """
    def __init__(self, data: pd.DataFrame):
        """
        Pass in trips data, with columns ['trip_distance, 'tip_amount']
        """
        if 'trip_distance' not in data.columns or 'tip_amount' not in data.columns:
            raise ValueError('Data requires column "trip_distance" and "tip_amount"')

        self.dists_and_tips = data.copy()

    def clean(self):
        self.dists_and_tips['tip_amount_z_score'] = zscore(self.dists_and_tips['tip_amount'])
        self.dists_and_tips = self.dists_and_tips[abs(self.dists_and_tips['tip_amount_z_score']) < 2]

    def fit(self):
        if not hasattr(self, 'dists_and_tips'):
            raise ValueError("Data not fecthed yet. Call .fetch() first!")

        print('Fitting model...')
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            objective='reg:squarederror',
            random_state=42
        )
        X = self.dists_and_tips[['trip_distance']]
        y = self.dists_and_tips['tip_amount']
        self.model.fit(X, y)

    def plot_fit(self):
        if not hasattr(self, 'model'):
            raise Exception("Model not trained yet. Call .fit() first!")

        X = self.dists_and_tips[['trip_distance']]
        y = self.dists_and_tips['tip_amount']

        # Smooth x range for prediction
        x_input = np.linspace(X.min(), X.max(), 500).reshape(-1, 1)
        pred_output = self.model.predict(x_input)

        # Plot
        plt.figure(figsize=(12, 8))
        plt.scatter(X, y, marker='x', s=1, color='dodgerblue', label='Samples')
        plt.plot(x_input, pred_output, color='tomato', label='XGBoost Prediction')
        sns.despine()
        plt.grid()
        plt.legend()
        plt.title('Trip data shows more resilience to outliers')
        plt.xlabel('Trip Distance')
        plt.ylabel('Tip Amount')
        plt.show()

    def predict(self, trip_distance: float):
        """
        This should probably be chnged to be more scalable - we could
        tag job ids for prediction...
        """
        if not hasattr(self, 'model'):
            raise ValueError("Model not trained yet. Call .fit() first!")
    
        # TODO: To increase scaling, we could possibly tag
        # prediction jobs with ideas, and send them off in bulk?
        X = np.array([[trip_distance]])
        return float(self.model.predict(X)[0])
