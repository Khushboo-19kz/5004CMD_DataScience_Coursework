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

# =========================
# QUESTION B
# =========================

# Filter dates where trips exceed 10,000,000
set_10_25 = national_only[national_only["Number of Trips 10-25"] > 10_000_000][
    ["Date", "Number of Trips 10-25"]
].copy()

set_50_100 = national_only[national_only["Number of Trips 50-100"] > 10_000_000][
    ["Date", "Number of Trips 50-100"]
].copy()

print("Dates where Number of Trips 10-25 > 10,000,000:")
print(set_10_25)

print("\nDates where Number of Trips 50-100 > 10,000,000:")
print(set_50_100)

print("\nCount of dates for 10-25 range:", len(set_10_25))
print("Count of dates for 50-100 range:", len(set_50_100))

# Merge on Date to compare shared dates
comparison = pd.merge(set_10_25, set_50_100, on="Date", how="outer")

print("\nComparison table:")
print(comparison)

# Scatterplot comparison
plt.figure(figsize=(12, 6))
plt.scatter(set_10_25["Date"], set_10_25["Number of Trips 10-25"], label="10-25 Trips", alpha=0.7)
plt.scatter(set_50_100["Date"], set_50_100["Number of Trips 50-100"], label="50-100 Trips", alpha=0.7)

plt.xlabel("Date")
plt.ylabel("Number of Trips")
plt.title("Comparison of Dates with More Than 10,000,000 Trips")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# QUESTION C
# =========================

# Convert the wide-format week dataset into long format
# so that each row is one (distance, trip_count) pair
records = []

for _, row in small_dataset.iterrows():
    for col in distance_cols:
        records.append({
            "Date": row["Date"],
            "Distance_Miles": distance_midpoints[col],
            "Trip_Frequency": row[col]
        })

model_df = pd.DataFrame(records)

print("Model dataset:")
print(model_df.head())

# Features and target
X = model_df[["Distance_Miles"]]
y = model_df["Trip_Frequency"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a simple linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation metrics
rmse = math.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("RMSE:", rmse)
print("R^2:", r2)
print("Intercept:", model.intercept_)
print("Slope:", model.coef_[0])

# Scatterplot with regression line
plt.figure(figsize=(10, 6))
plt.scatter(model_df["Distance_Miles"], model_df["Trip_Frequency"], alpha=0.7, label="Actual Data")

# Create sorted values for a clean regression line
x_line = np.linspace(model_df["Distance_Miles"].min(), model_df["Distance_Miles"].max(), 200)
x_line_df = pd.DataFrame({"Distance_Miles": x_line})
y_line = model.predict(x_line_df)

plt.plot(x_line, y_line, linewidth=2, label="Linear Regression Line")
plt.xlabel("Trip Length (Miles)")
plt.ylabel("Trip Frequency")
plt.title("Trip Frequency vs Trip Length")
plt.legend()
plt.tight_layout()
plt.show()
