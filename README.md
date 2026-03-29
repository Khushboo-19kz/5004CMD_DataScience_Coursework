# 5004CMD Mobility Data Analysis

## Overview

This project analyses large-scale mobility data to understand national travel behaviour.
It investigates how people move across different distance ranges, evaluates travel patterns, and compares **sequential vs parallel computing performance**.

The project is based on two datasets and follows the coursework requirements for data preprocessing, analysis, modelling, and performance evaluation.

---

## Objectives

* Analyse how many people stay at home vs travel
* Examine how far people travel when they leave home
* Identify high-volume travel patterns across distance ranges
* Build a predictive model of travel frequency
* Compare sequential and parallel processing performance

---

## Datasets

* **Trips_by_Distance.csv**
  Large dataset containing daily travel statistics across the United States

* **Trips_Full Data.csv**
  Smaller dataset (Week 32) containing detailed trip distributions by distance

---

## Project Structure

```
5004CMD_Mobility_Analysis/
│
├── data/
│   ├── Trips_by_Distance.csv
│   └── Trips_Full Data.csv
│
├── src/
│   └── mobility_analysis_5004cmd.py
│
├── outputs/
│   ├── (generated figures and tables)
│
├── report/
│   └── 5004CMD_Report.pdf
│
├── README.md
├── requirements.txt
```

---

## Methodology

### Data Preprocessing

* Converted date columns to datetime format
* Filtered data to **National level only**
* Removed unnecessary location-based columns
* Aligned datasets for consistent analysis

---

## Analysis

### Question A

* Calculated weekly average population staying at home
* Analysed daily population not staying at home
* Examined travel distribution across distance ranges

### Question B

* Identified dates where:

  * Trips (10–25 miles) exceed 10,000,000
  * Trips (50–100 miles) exceed 10,000,000
* Compared patterns using scatter plots

### Question C

* Built a **Linear Regression model** to predict travel frequency
* Converted distance ranges into numerical values
* Evaluated using:

  * RMSE (Root Mean Squared Error)
  * R² (Coefficient of Determination)

### Question D

* Visualised number of travellers across distance categories
* Compared daily and average travel patterns

---

## Parallel Computing

* Implemented using **multiprocessing**
* Compared:

  * Sequential execution
  * Parallel execution (10 workers)
  * Parallel execution (20 workers)

### Key Finding

Parallel processing did not significantly improve performance due to:

* small task sizes
* overhead of process management

---

## Results

### Q1: Population Staying at Home

![Q1](outputs/q1_weekly_population_staying_home.png)

### Q2: Trip Threshold Comparison

![Q2](outputs/q2_trip_threshold_comparison.png)

### Q3: Regression Model

![Q3](outputs/q3_trip_frequency_vs_distance_regression.png)

### Q4: Travel Distribution

![Q4](outputs/q4_average_travellers_by_distance.png)

---
## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Scikit-learn
* Multiprocessing

---

## Key Insights

* Most travel occurs within shorter distance ranges
* Medium-distance travel (10–25 miles) is significantly more frequent than long-distance travel
* Linear regression shows a measurable relationship between trip distance and frequency
* Sequential processing is more efficient for this dataset due to lower overhead

---

## Author

**Khushboo Zope**
Student ID: 15501082


This project used AI tools (ChatGPT) for guidance in structuring code, debugging, and formatting.
All code and outputs were reviewed, tested, and adapted by the author before submission.
