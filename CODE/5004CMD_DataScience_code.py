#---------------------
#Importing set up 
#--------------------

import time
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -------------------------
# Load datasets
# -------------------------
big_dataset = pd.read_csv("Trips_by_Distance.csv")
small_dataset = pd.read_csv("Trips_Full Data.csv")

# Convert dates to datetime
big_dataset["Date"] = pd.to_datetime(big_dataset["Date"])
small_dataset["Date"] = pd.to_datetime(small_dataset["Date"])

# Keep only National data, as required by the guide
national_only = big_dataset[big_dataset["Level"] == "National"].copy()

# Optional: remove location columns that are not needed for National-level analysis
cols_to_drop = ["State FIPS", "State Postal Code", "County FIPS", "County Name"]
national_only = national_only.drop(columns=cols_to_drop, errors="ignore")

# Distance columns from the week-level dataset
distance_cols = [
    "Trips <1 Mile",
    "Trips 1-3 Miles",
    "Trips 3-5 Miles",
    "Trips 5-10 Miles",
    "Trips 10-25 Miles",
    "Trips 25-50 Miles",
    "Trips 50-100 Miles",
    "Trips 100-250 Miles",
    "Trips 250-500 Miles",
    "Trips 500+ Miles"
]

# Distance midpoints for modelling
distance_midpoints = {
    "Trips <1 Mile": 0.5,
    "Trips 1-3 Miles": 2,
    "Trips 3-5 Miles": 4,
    "Trips 5-10 Miles": 7.5,
    "Trips 10-25 Miles": 17.5,
    "Trips 25-50 Miles": 37.5,
    "Trips 50-100 Miles": 75,
    "Trips 100-250 Miles": 175,
    "Trips 250-500 Miles": 375,
    "Trips 500+ Miles": 500
}
