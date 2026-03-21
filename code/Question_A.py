import pandas as pd
import matplotlib.pyplot as plt

# Read/Load datasets

Trips_by_Distance = pd.read_csv("Trips_by_Distance.csv")
Trips_Full Data = pd.read_csv("Trips_Full Data.csv")

# Convert date format
trips_by_distance["Date"] = pd.to_datetime(trips_by_distance["Date"])
trips_full_data["Date"] = pd.to_datetime(trips_full_data["Date"])
# Keep only national-level data from trip by distance dataet
national_only = trips_by_distance[trips_by_distance["Level"] == "National"].copy()

# Drop unnecessary columns
national_only.drop(
    columns=["State FIPS", "State Postal Code", "County FIPS", "County Name"],
    errors="ignore",
    inplace=True
)

# Match the week covered by the trips full dataset
start_date = trips_full_data["Date"].min()
end_date = trips_full_data["Date"].max()

selected_week_data = national_only[national_only["Date"].between(start_date, end_date)].copy()


# QA-1: People staying at home per week

weekly_home = (
    national_only.groupby("Week")["Population Staying at Home"]
    .mean()
    .reset_index()
    .sort_values("Week")
)

if weekly_home["Week"].min() == 0:
    weekly_home["Week"] += 1

print("Average population staying at home per week:")
print(weekly_home)

plt.figure(figsize=(12, 6))
plt.bar(weekly_home["Week"], weekly_home["Population Staying at Home"])
plt.xlabel("Week")
plt.ylabel("Population Staying at Home")
plt.title("Average Population Staying at Home per Week")
plt.tight_layout()
plt.show()

# Supporting evidence: people not staying at home during selected week

not_home_daily = (
    trips_full_data.groupby("Date")["People Not Staying at Home"]
    .mean()
    .reset_index()
    .sort_values("Date")
)

print("\nAverage people not staying at home per day:")
print(not_home_daily)

plt.figure(figsize=(12, 6))
plt.bar(not_home_daily["Date"].dt.strftime("%Y-%m-%d"),
        not_home_daily["People Not Staying at Home"])
plt.xlabel("Date")
plt.ylabel("People Not Staying at Home")
plt.title("Average Population Not Staying at Home per Day")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# QA-2: How far people are travelling when not staying at home
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

distance_means = trips_full_data[distance_cols].mean().sort_values(ascending=False)

print("\nAverage trips by distance range:")
print(distance_means)

plt.figure(figsize=(12, 6))
distance_means.plot(kind="bar")
plt.xlabel("Distance Range")
plt.ylabel("Mean Number of Trips")
plt.title("Average Trips by Distance Range")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
