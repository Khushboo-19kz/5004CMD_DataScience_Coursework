import pandas as pd
import matplotlib.pyplot as plt

# load the dataset
big_dataset = pd.read_csv("Trips_by_Distance.csv")

# convert Date into datetime format
big_dataset["Date"] = pd.to_datetime(big_dataset["Date"])

# keep only national-level data
national_only = big_dataset[big_dataset["Level"] == "National"].copy()

# keep only the columns needed for this question
national_only = national_only[["Number of Trips 10-25", "Number of Trips 50-100", "Date"]]

# create filtered sets based on the conditions in the question
set1 = national_only[national_only["Number of Trips 10-25"] > 10000000]
set2 = national_only[national_only["Number of Trips 50-100"] > 10000000]
set3 = national_only[
    (national_only["Number of Trips 10-25"] > 10000000) &
    (national_only["Number of Trips 50-100"] > 10000000)
]
set4 = national_only[
    (national_only["Number of Trips 10-25"] > 10000000) &
    (national_only["Number of Trips 50-100"] < 10000000)
]

# print number of rows in each set
print("Number of rows in Set 1 (Number of Trips 10-25 > 10,000,000):", len(set1))
print("Number of rows in Set 2 (Number of Trips 50-100 > 10,000,000):", len(set2))
print("Number of rows in Set 3 (Both conditions met):", len(set3))
print("Number of rows in Set 4 (10-25 > 10,000,000 and 50-100 < 10,000,000):", len(set4))

# print matching dates
print("\nSet 1 dates:")
print(set1[["Date", "Number of Trips 10-25"]])

print("\nSet 2 dates:")
print(set2[["Date", "Number of Trips 50-100"]])

# scatterplot comparison
plt.figure(figsize=(12, 6))

plt.scatter(
    set1["Date"],
    set1["Number of Trips 10-25"],
    alpha=0.6,
    label="Set 1: Trips 10-25 > 10M"
)

plt.scatter(
    set2["Date"],
    set2["Number of Trips 50-100"],
    alpha=0.6,
    label="Set 2: Trips 50-100 > 10M"
)

# log scale makes both sets easier to compare
plt.yscale("log")

plt.title("Comparison of Dates Where Trip Counts Exceed 10,000,000")
plt.xlabel("Date")
plt.ylabel("Number of Trips")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()
