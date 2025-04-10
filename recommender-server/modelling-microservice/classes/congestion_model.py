from math import radians, cos, sin, asin, sqrt
import pandas as pd 
import numpy as np
import seaborn as sns
from collections import defaultdict
from scipy.stats import zscore


class CongestionModel:
    """
    Models the congestion multiplier for a given time.
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data.copy()
        self.data['congestion'] = self.data.apply(self.get_congestion, axis=1)
        self.data = self.data[self.data['congestion'] > 0]
        self.data['hour'] = self.data['pickup_datetime'].dt.hour

    def get_congestion(self, row):
        # Taken from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
        def haversine(lon1, lat1, lon2, lat2):
            """
            Calculate the great circle distance in kilometers between two points 
            on the earth (specified in decimal degrees)
            """
            # convert decimal degrees to radians 
            lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

            # haversine formula 
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            r = 3956 # in miles
            return c * r

        miles_per_second = 0.007
        euclidean_dist = haversine(row['pickup_longitude'], row['pickup_latitude'], row['dropoff_longitude'], row['dropoff_latitude'])
        euclidean_trip_time = euclidean_dist / miles_per_second

        return row['trip_time_in_secs'] - euclidean_trip_time

    def fit(self):
        groupby_hour_congestion = self.data.groupby('hour')['congestion'].mean()
        zscores = zscore(groupby_hour_congestion)

        # Flatten to 0 if zscore is < 0. Otherwise, substitute the z-score into a 
        # sigmoid function.
        negative_congestion_flattened = [0 if i < 0 else i for i in zscores]
        sigmoid_correction = [0 if 1 / (1 + np.exp(-i)) == 0.5 else 1 / (1 + np.exp(-i)) for i in negative_congestion_flattened]
        congestion_multipliers = 1 + np.array(sigmoid_correction)
        self.congestion_by_hour = dict(enumerate(congestion_multipliers))

    def predict(self, datetime: pd.Timestamp):
        return self.congestion_by_hour[datetime.hour]
