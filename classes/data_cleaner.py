import pandas as pd
import numpy as np

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
            (self.data['trip_distance'] != 0) &     # we can't have trips of 0 distance
            (self.data['trip_distance'] < 35) &     # NYC is 35 miles wide at most
            (self.data['trip_distance'] >= 0.1) &   # atleast 0.1 miles
            (self.data['passenger_count'] <= 5)     # biggest taxi is a mini van of 5
        ]

    def remove_negative_values(self):
        self.data = self.data[
            (self.data[self.quant_fields] > 0).all(axis=1)
        ]

    def write_data(self, path: str):
        self.data.to_parquet(path)