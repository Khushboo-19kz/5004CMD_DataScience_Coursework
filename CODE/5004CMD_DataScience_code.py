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
