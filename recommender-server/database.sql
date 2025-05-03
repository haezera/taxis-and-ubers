-- trips table for data. 
CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance NUMERIC,
    fare_amount NUMERIC,
    tip_amount NUMERIC,
    trip_time_in_secs NUMERIC,
    fare_per_sec NUMERIC,
    day TEXT,
    "time" TIME,
    pickup_longitude NUMERIC,
    pickup_latitude NUMERIC,
    dropoff_longitude NUMERIC,
    dropoff_latitude NUMERIC
);

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- these are simulated rides between drivers and users
CREATE TABLE rides (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    fare_amount NUMERIC NOT NULL,
    estimated_revenue NUMERIC NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
);