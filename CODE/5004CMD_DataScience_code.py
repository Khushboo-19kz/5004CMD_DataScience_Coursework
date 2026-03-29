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

