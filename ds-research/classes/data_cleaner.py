import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class TaxiDataCleaner:
    def __init__(self, path: str):
        self.data = pd.read_parquet(path)
        self.path = path
        self.quant_fields = [
            'passenger_count', 'trip_distance', 
            'fare_amount', 
            'tip_amount', 
            'tolls_amount', 
            'total_amount'
        ]

    def create_features(self):
        def adjusted_zscore(series):
            median = np.median(series)
            mad = np.median(np.abs(series - median))
            return 0.6745 * (series - median) / mad

        self.data['pickup_datetime'] = pd.to_datetime(self.data['pickup_datetime'])
        self.data['dropoff_datetime'] = pd.to_datetime(self.data['dropoff_datetime'])

        self.data['trip_time_in_secs'] = (self.data['dropoff_datetime'] - self.data['pickup_datetime']).dt.total_seconds()
        self.data['fare_per_sec'] = self.data['fare_amount'] / self.data['trip_time_in_secs']
        self.data['trip_time_z_score'] = adjusted_zscore(self.data['trip_time_in_secs'])

        self.data['day'] = self.data['pickup_datetime'].dt.day_name()
        self.data['time'] = self.data['pickup_datetime'].dt.time
        
    def remove_nans(self):
        """
        Removes any rows that have NaNs in our quantitative fields
        """
        self.data = self.data.dropna(subset=self.quant_fields)

    def remove_nonsense_values(self):
        """
        In our data quality analysis, we defined the bounds for our analysis.
        This means we want:
            - No trips of 0 distance 
            - We want taxi trips that only plausibly occured within NYC 
            - We want trips of atleast 0.1 miles
            - We want a maximum of 5 passengers.
        """
        self.data = self.data[
            (self.data['trip_distance'] != 0) &         # we can't have trips of 0 distance
            (self.data['trip_distance'] < 35) &         # NYC is 35 miles wide at most
            (self.data['trip_distance'] >= 0.1) &       # atleast 0.1 miles
            (self.data['passenger_count'] <= 5) &       # biggest taxi is a mini van of 5
            (self.data['trip_time_in_secs'] >= 300) &      # trips of atleast 5 minutes
            (abs(self.data['trip_time_z_score'] < 2))   # remove outliers
        ]

    def remove_negative_values(self):
        self.data = self.data[
            (self.data[self.quant_fields] > 0).all(axis=1)
        ]

    def remove_outlier_cluster(self):
        X = self.data[['fare_per_sec']]
        X_scaled = StandardScaler().fit_transform(X)

        self.data['cluster'] = KMeans(n_clusters=2).fit_predict(X_scaled)
        major_cluster = self.data['cluster'].value_counts().idxmax()
        self.data = self.data[self.data['cluster'] == major_cluster]

        # Optionally drop the cluster label afterward
        self.data.drop(columns=['cluster'], inplace=True)

    def clean_data(self, cluster=True):
        self.create_features()
        self.remove_nans()
        self.remove_negative_values()
        self.remove_nonsense_values()
        if cluster: self.remove_outlier_cluster()

    def write_data(self, path: str):
        self.data.to_parquet(path)
