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

# =========================
# QUESTION A
# =========================

# 1A. Average number of people staying at home per week
weekly_home = (
    national_only.groupby("Week", as_index=False)["Population Staying at Home"]
    .mean()
    .sort_values("Week")
)

print("Average population staying at home per week:")
print(weekly_home)

plt.figure(figsize=(12, 6))
plt.plot(
    weekly_home["Week"],
    weekly_home["Population Staying at Home"],
    marker="o",
    linewidth=2
)

plt.xlabel("Week")
plt.ylabel("Average Population Staying at Home")
plt.title("Average Population Staying at Home per Week (National)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# 1B. Average people not staying at home in the small dataset (Week 32)
not_home_daily = small_dataset[["Date", "People Not Staying at Home"]].copy()
print("\nPeople not staying at home by day (Week 32):")
print(not_home_daily)

plt.figure(figsize=(10, 5))
plt.plot(
    not_home_daily["Date"],
    not_home_daily["People Not Staying at Home"],
    marker="o",
    linewidth=2
)

plt.xlabel("Date")
plt.ylabel("People Not Staying at Home")
plt.title("People Not Staying at Home per Day")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# 1C. How far people travel when they do not stay home:
# Calculate mean trips for each distance band in the small dataset
mean_trips_by_distance = small_dataset[distance_cols].mean().sort_values(ascending=False)

print("\nMean trips by distance range (Week 32):")
print(mean_trips_by_distance)

plt.figure(figsize=(12, 6))
plt.bar(mean_trips_by_distance.index, mean_trips_by_distance.values)

for i, v in enumerate(mean_trips_by_distance.values):
    plt.text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=8)

plt.xlabel("Distance Range")
plt.ylabel("Average Number of Trips")
plt.title("Average Trips by Distance Range")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
