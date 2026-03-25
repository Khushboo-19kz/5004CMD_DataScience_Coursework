import pandas as pd
import matplotlib.pyplot as plt

# load the main dataset
trips_by_distance = pd.read_csv("Trips_by_Distance.csv")

# make sure Date is treated as a date column
trips_by_distance["Date"] = pd.to_datetime(trips_by_distance["Date"])

# only use national data
national_only = trips_by_distance[trips_by_distance["Level"] == "National"].copy()

# keep only the columns needed for this question
national_only = national_only[["Date", "Number of Trips 10-25", "Number of Trips 50-100"]]

# dates where 10-25 trips are above 10 million
set_10_25 = national_only[national_only["Number of Trips 10-25"] > 10_000_000].copy()

# dates where 50-100 trips are above 10 million
set_50_100 = national_only[national_only["Number of Trips 50-100"] > 10_000_000].copy()

# dates where both conditions happen at the same time
both_sets = national_only[
    (national_only["Number of Trips 10-25"] > 10_000_000) &
    (national_only["Number of Trips 50-100"] > 10_000_000)
].copy()

# print the matching dates and values
print("Dates where Number of Trips 10-25 > 10,000,000:")
print(set_10_25[["Date", "Number of Trips 10-25"]])

print("\nDates where Number of Trips 50-100 > 10,000,000:")
print(set_50_100[["Date", "Number of Trips 50-100"]])

print("\nSummary:")
print(f"Number of dates where Number of Trips 10-25 > 10,000,000: {len(set_10_25)}")
print(f"Number of dates where Number of Trips 50-100 > 10,000,000: {len(set_50_100)}")
print(f"Number of dates where both conditions are true: {len(both_sets)}")

# scatterplot to compare both trip ranges
plt.figure(figsize=(12, 6))

plt.scatter(
    set_10_25["Date"],
    set_10_25["Number of Trips 10-25"],
    label="10-25 trips (>10M)",
    alpha=0.7
)

plt.scatter(
    set_50_100["Date"],
    set_50_100["Number of Trips 50-100"],
    label="50-100 trips (>10M)",
    alpha=0.7
)

# log scale helps because the two ranges are very different in size
plt.yscale("log")

plt.xlabel("Date")
plt.ylabel("Number of Trips")
plt.title("Comparison of Dates Where Trip Counts Exceed 10,000,000")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()
