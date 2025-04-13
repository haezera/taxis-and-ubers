from sqlalchemy import create_engine
import pandas as pd

class DataMonolith:
    """
    The data monolith pulls the required data, and passes the
    needed data into different classes (instead of each class pulling
    data independently).
    """

    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        db_url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
        self.engine = create_engine(db_url)

    def pull_date_range(self, start_dt: str, end_dt: str):
        query = '''
            SELECT
                *
            FROM
                trips
            WHERE
                pickup_datetime >= %s
                AND dropoff_datetime <= %s
        '''
        self.data = pd.read_sql(query, self.engine, params=(start_dt, end_dt))

    def return_columns(self, columns: list) -> pd.DataFrame:
        return self.data[columns]

    def return_trip_by_id(self, id: int):
        """
        I think this will be useful if we decide to implement a live algorithm.
        """
        query = '''
            SELECT
                *
            FROM
                trips
            WHERE
                id = %s
        '''
        self.data = pd.read_sql(query, self.engine, params=(id))
