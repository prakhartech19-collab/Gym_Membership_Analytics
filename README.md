# Gym & Fitness Center Membership Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-orange.svg)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26%2B-informational.svg)](https://numpy.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-success.svg)](https://matplotlib.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13%2B-blueviolet.svg)](https://seaborn.pydata.org/)
[![OpenPyXL](https://img.shields.io/badge/OpenPyXL-3.1%2B-lightgrey.svg)](https://openpyxl.readthedocs.io/)

A data analytics project analyzing member check-in logs, workout durations, group classes, and membership tiers for a fitness facility. The dataset spans 22 calendar months (January 2025 through October 2026) across 850 verified check-in records. 

The main goals are identifying peak facility congestion, evaluating class popularity, analyzing revenue distribution by tier, finding churn-risk members, and providing practical operational recommendations.

---

## Project Structure

```
Gym_Membership_Analytics/
├── 12_gym_membership.csv          # Raw dataset file (862 rows)
├── gym_analytics.py               # Main data cleaning and analysis script
├── dashboard.py                   # Streamlit dashboard for interactive exploration
├── requirements.txt               # Project dependencies
├── README.md                      # Documentation
│
├── charts/                        # Saved visual deliverables
│   ├── peak_hours_heatmap.png     # Heatmap of weekday vs. hour check-in volume
│   ├── duration_boxplot_by_tier.png # Boxplot of workout durations across tiers
│   └── class_popularity_bar.png   # Bar chart of attendance per fitness class
│
└── outputs/                       # Exported datasets and reports
    ├── cleaned_12_gym_membership.csv  # Cleaned, imputed, and transformed dataset
    └── gym_analytics_report.xlsx      # Styled 4-sheet Excel report
```

---

## Dataset Schema

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `Checkin_ID` | String | Unique log identifier for each check-in (e.g. `G00000`). |
| `Member_ID` | String | Unique ID assigned to each member (e.g. `M0316`). |
| `Membership_Tier` | Categorical | Plan level (`Basic`, `Gold`, `Platinum`). |
| `Gender` | Categorical | Gender recorded (`Male`, `Female`, `Other`). |
| `Checkin_Time` | Datetime | Check-in timestamp. |
| `Workout_Duration_Mins` | Numeric | Recorded workout duration in minutes (has missing values). |
| `Fitness_Class` | Categorical | Class attended (`Strength`, `Spin`, `HIIT`, `Zumba`, `Yoga`, or empty for general floor workouts). |
| `Monthly_Fee` | Numeric | Monthly fee paid in INR (₹999, ₹1,499, ₹2,499). |

---

## Setup & Installation

1. **Navigate to the project directory:**
   ```powershell
   cd Gym_Membership_Analytics
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   # python3 -m venv venv && source venv/bin/activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## Analysis & Findings

### 1. Data Cleaning & Preprocessing (Tasks 1–4)
- **Duplicates:** Identified and removed 12 duplicate `Checkin_ID` records, bringing the dataset from 862 down to 850 valid entries.
- **Missing Values:** Found 21 missing values in `Workout_Duration_Mins` (~2.5%) and 155 empty values in `Fitness_Class` (~18%, indicating open floor visits without a structured class).
- **Imputation:** Missing workout durations were imputed using the median duration of each member's respective tier (`Basic`: 70 min, `Gold`: 76 min, `Platinum`: 68 min). Median was chosen over mean because gym durations often have extreme values (e.g., quick 20-min visits vs. 2-hour workouts) that drag the arithmetic mean.
- **Feature Engineering:** Extracted `Weekday`, `Visit_Hour` (0–23), and `Year_Month` from `Checkin_Time`.

### 2. Facility KPIs & Tier Comparison (Tasks 5–6)
- **Total Valid Check-Ins:** 850 visits across 348 unique members.
- **Overall Average Duration:** 72.4 minutes (Median: 71.0 minutes).

| Membership Tier | Total Check-Ins | Unique Members | Visits / Member | Mean Duration (min) | Share of Check-Ins |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Basic** | 463 | 270 | 1.71 | 72.1 | 54.5% |
| **Gold** | 279 | 202 | 1.38 | 73.7 | 32.8% |
| **Platinum** | 108 | 93 | 1.16 | 70.6 | 12.7% |

*Takeaway:* Basic members visit most frequently per person (1.71 visits), while Platinum members visit the least (1.16 visits). This points to an under-utilization risk among higher-paying members.

### 3. Peak Demand Patterns (Task 7)
- **Top Hours:** Check-ins peak at **7:00 AM** (63 visits) and **1:00 PM** (63 visits), with a secondary wave at **6:00 PM** and **9:00 PM** (51 visits each).
- **Weekly Distribution:**
  - **Saturday:** 137 check-ins (16.1%) — busiest day of the week.
  - **Monday:** 127 check-ins (14.9%)
  - **Wednesday:** 126 check-ins (14.8%)
  - **Thursday:** 125 check-ins (14.7%)
  - **Sunday:** 120 check-ins (14.1%)
  - **Tuesday:** 114 check-ins (13.4%)
  - **Friday:** 101 check-ins (11.9%) — slowest day (~26% lower than Saturday).

### 4. Class Popularity (Task 8)
- 153 visits (18.0%) were unstructured gym floor workouts (no class).
- Across structured studio sessions:
  1. **Strength Training:** 151 check-ins (21.7% of classes)
  2. **Spin Cycling:** 143 check-ins (20.5% of classes)
  3. **HIIT:** 136 check-ins (19.5% of classes)
  4. **Zumba:** 135 check-ins (19.4% of classes)
  5. **Yoga:** 132 check-ins (18.9% of classes)

*Takeaway:* Strength and Spin together account for over 42% of all class attendance.

### 5. Duration by Gender (Task 9)
- **Male:** 292 visits | Mean: 73.05 min | Median: 71.0 min
- **Female:** 296 visits | Mean: 73.02 min | Median: 72.0 min
- **Other:** 262 visits | Mean: 71.01 min | Median: 70.0 min

*Takeaway:* The average difference between male and female sessions is roughly 0.03 minutes (under 2 seconds). Gender has virtually zero impact on session length.

### 6. Revenue Breakdown (Task 10)
To prevent inflating revenue by counting multiple visits per month as separate payments, members were deduplicated by `(Member_ID, Year_Month)`:

| Membership Tier | Active Member-Months | Total Revenue | Average Monthly Revenue | Revenue Share |
| :--- | :---: | :---: | :---: | :---: |
| **Basic** (₹999) | 395 | ₹658,605 | ₹29,936.59 | 49.4% |
| **Gold** (₹1,499) | 276 | ₹442,724 | ₹20,123.82 | 33.2% |
| **Platinum** (₹2,499) | 134 | ₹232,366 | ₹10,562.09 | 17.4% |
| **Total** | **805** | **₹1,333,695** | **₹60,622.50** | **100.0%** |

### 7. Engagement & Retention Risks (Task 11)
- Members averaging fewer than 2 visits per month over the 22-month tracking window were flagged.
- Because the overall dataset average is 2.44 visits per member spread across 22 months, all 348 members averaged under 2 visits/month over the entire timeframe.
- The average inactivity period since last check-in sits above 200 days across Basic and Gold, highlighting a clear need for active re-engagement outreach.

### 8. Statistical Metrics & Outlier Detection (Tasks 12–14)
- **NumPy Distribution:** Mean = 72.41 min, Median = 71.00 min, Variance = 975.79, Standard Deviation = 31.24 min.
- **Quartiles:** Q1 = 47.00 min, Q2 = 71.00 min, Q3 = 98.75 min.
- **IQR & Outliers:** IQR = 51.75 min. With lower bound at -30.63 min and upper bound at 176.38 min, there are **0 statistical outliers** (min is 20 min, max is 129 min).
- **Session Intensity Breakdown:**
  - **Short (< 30 min):** 89 sessions (10.5%) — Quick cardio or lunch-break visits.
  - **Moderate (30–60 min):** 242 sessions (28.5%) — Standard classes and regular workouts.
  - **Extended (> 60 min):** 519 sessions (61.1%) — Longer lifting or multi-class routines.

---

## Visual Deliverables

| File | Type | Description |
| :--- | :--- | :--- |
| `charts/peak_hours_heatmap.png` | Heatmap | Hourly congestion across each day of the week (Monday–Sunday). |
| `charts/duration_boxplot_by_tier.png` | Boxplot | Spread, medians, and quartile distributions for Basic, Gold, and Platinum. |
| `charts/class_popularity_bar.png` | Bar Chart | Attendance counts ranked across all structured group classes. |

---

## Generated Reports

1. **Cleaned CSV (`outputs/cleaned_12_gym_membership.csv`):**  
   Contains all 850 rows with imputed durations, extracted dates/hours, and workout intensity tags.

2. **Excel Workbook (`outputs/gym_analytics_report.xlsx`):**  
   Formatted multi-sheet Excel file with customized headers and auto-sized columns:
   - `Tier_Comparison`: Summary counts, unique members, visits per member, and durations.
   - `Class_Popularity`: Ranked class attendance numbers and percentage shares.
   - `Busiest_Days`: Day-by-day check-in traffic from Monday to Sunday.
   - `Low_Engagement_Members`: List of members with low visit frequencies and inactivity days.

---

## Key Recommendations (Task 15)

1. **Adjust Staffing to Peak Times:**  
   Floor traffic concentrates heavily at 7:00 AM and 1:00 PM, plus secondary evening peaks at 6:00 PM and 9:00 PM. Schedule extra floor trainers and reception staff during 6:30–8:30 AM and 12:30–2:00 PM. Schedule equipment maintenance and deep cleaning during off-peak hours (2:00–4:00 PM).

2. **Run Promotions on Slower Days:**  
   Friday is the slowest day of the week (26% lower check-ins than Saturday). Introduce Friday perks, like guest passes or smoothie bar discounts, to balance weekly utilization.

3. **Expand High-Demand Classes:**  
   Strength Training and Spin make up over 42% of class visits. Adding more morning and weekend slots for these two classes will better serve demand. Lower-attendance afternoon Yoga sessions can be rescheduled or converted to high-energy hybrid formats.

4. **Automate Churn Outreach:**  
   Set up automated follow-ups for inactive members:
   - **Day 14 without a visit:** Send a workout tip or friendly check-in text.
   - **Day 28 without a visit:** Offer a free body scan or personal trainer consultation.
   - **Day 45 without a visit:** Have a staff member call directly to offer a goal reassessment.

5. **Target Upgrades for Active Basic Members:**  
   Basic tier members currently visit more often than Platinum members (1.71 vs 1.16 visits/person). Offer active Basic members a 14-day free trial of Gold or Platinum. At the same time, add clear perks to Platinum (priority class booking, locker access) so high-tier members get tangible value for their subscription.

---

## How to Run

Run the analysis script:
```powershell
python gym_analytics.py
```

Launch the interactive dashboard (optional):
```powershell
pip install streamlit
streamlit run dashboard.py
```

---

## Author

**Prakhar Tiwari**  
- **Admission No:** 2026B01010421  
- **Email:** officialprakhar50@gmail.com

---

## License

This project is licensed under the MIT License - feel free to use and adapt it for learning or portfolio purposes.
