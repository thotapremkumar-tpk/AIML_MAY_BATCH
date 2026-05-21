import numpy as np
import pandas as pd
from io import StringIO

# ─────────────────────────────────────────────
# Sample Dataset Creation
# ─────────────────────────────────────────────
data = """student_id,name,gender,math_score,science_score,attendance,exam_date
1,Alice,Female,85,90,75,2024-03-15
2,Bob,Male,92,88,82,2024-03-15
3,Charlie,Male,78,NaN,65,2024/03/15
4,Diana,Female,NaN,76,91,2024-03-15
5,Eve,Female,95,98,88,15-03-2024
6,Frank,Male,200,85,55,2024-03-15
7,Grace,Female,88,92,78,2024-03-15
8,Hank,Male,70,NaN,48,2024-03-15
9,Ivy,Female,85,90,75,2024-03-15
10,Jack,Male,92,88,82,2024-03-15
11,Alice,Female,85,90,75,2024-03-15
12,Leo,Male,NaN,55,-5,2024-03-15
13,Mia,Female,60,62,95,2024-03-15
14,Nina,Female,300,70,70,2024-03-15
"""

df = pd.read_csv(StringIO(data))

print("=" * 60)
print("   ASSESSMENT: Data Preprocessing using NumPy & Pandas")
print("=" * 60)

# ─────────────────────────────────────────────
# PART 1 — NumPy Operations
# ─────────────────────────────────────────────
print("\n" + "─" * 60)
print("PART 1 — NumPy Operations")
print("─" * 60)

# Create NumPy array from math_score (drop NaN first)
math_array = np.array(df['math_score'].dropna())
print(f"\nNumPy array from math_score:\n{math_array}")

# Mean, Median, Max, Min
print(f"\nMean   : {np.mean(math_array):.2f}")
print(f"Median : {np.median(math_array):.2f}")
print(f"Maximum: {np.max(math_array):.2f}")
print(f"Minimum: {np.min(math_array):.2f}")

# Normalize the scores (Min-Max Normalization)
normalized = (math_array - np.min(math_array)) / (np.max(math_array) - np.min(math_array))
print(f"\nNormalized math_scores (Min-Max):\n{np.round(normalized, 4)}")

# ─────────────────────────────────────────────
# PART 2 — Pandas Exploration
# ─────────────────────────────────────────────
print("\n" + "─" * 60)
print("PART 2 — Pandas Exploration")
print("─" * 60)

# Load dataset
print("\n[Loading dataset...]")
print(f"Dataset loaded with shape: {df.shape}")

# First 5 rows
print("\nFirst 5 rows of the dataset:")
print(df.head())

# Data types
print("\nData types of all columns:")
print(df.dtypes)

# Missing values
print("\nTotal missing values in each column:")
print(df.isnull().sum())

# Students with attendance below 70%
print("\nStudents with attendance below 70%:")
low_attendance = df[df['attendance'] < 70][['student_id', 'name', 'attendance']]
print(low_attendance)

# ─────────────────────────────────────────────
# PART 3 — Data Preprocessing
# ─────────────────────────────────────────────
print("\n" + "─" * 60)
print("PART 3 — Data Preprocessing")
print("─" * 60)

# 3a. Handle missing values
print("\n[3a] Handling missing values...")
df['math_score'] = df['math_score'].fillna(df['math_score'].median())
df['science_score'] = df['science_score'].fillna(df['science_score'].median())
# Fix invalid attendance value (negative)
df['attendance'] = df['attendance'].apply(lambda x: np.nan if x < 0 else x)
df['attendance'] = df['attendance'].fillna(df['attendance'].median())
print("Missing values after handling:")
print(df.isnull().sum())

# 3b. Convert incorrect data formats
print("\n[3b] Converting exam_date to datetime format...")
def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y'):
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    return pd.NaT

df['exam_date'] = df['exam_date'].apply(parse_date)
print(f"exam_date dtype after conversion: {df['exam_date'].dtype}")
print(df[['name', 'exam_date']].head())

# 3c. Detect and handle outliers using IQR
print("\n[3c] Detecting and handling outliers in math_score & science_score...")

def handle_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"  Outliers in '{col}' (bounds: {lower:.1f} – {upper:.1f}):")
    print(f"  {outliers[['name', col]].to_string(index=False)}")
    # Cap outliers
    df[col] = df[col].clip(lower=lower, upper=upper)
    return df

df = handle_outliers_iqr(df, 'math_score')
df = handle_outliers_iqr(df, 'science_score')
print("\nmath_score & science_score after outlier handling:")
print(df[['name', 'math_score', 'science_score']])

# 3d. Find and remove duplicate rows
print("\n[3d] Finding and removing duplicate rows...")
duplicates = df[df.duplicated()]
print(f"Number of duplicate rows found: {len(duplicates)}")
print(duplicates[['student_id', 'name']])
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
print(f"Shape after removing duplicates: {df.shape}")

# ─────────────────────────────────────────────
# PART 4 — Data Analysis
# ─────────────────────────────────────────────
print("\n" + "─" * 60)
print("PART 4 — Data Analysis")
print("─" * 60)

# 4a. Create average_score column
df['average_score'] = (df['math_score'] + df['science_score']) / 2
print("\n[4a] New column 'average_score' added.")
print(df[['name', 'math_score', 'science_score', 'average_score']])

# 4b. Top 5 students by average_score
print("\n[4b] Top 5 students based on average_score:")
top5 = df.nlargest(5, 'average_score')[['name', 'gender', 'average_score']]
print(top5.to_string(index=False))

# 4c. Correlation between attendance and marks
print("\n[4c] Correlation between attendance and average_score:")
corr = df['attendance'].corr(df['average_score'])
print(f"  Pearson Correlation: {corr:.4f}")
if corr > 0.5:
    print("  → Strong positive correlation: higher attendance → higher marks.")
elif corr > 0:
    print("  → Weak positive correlation between attendance and marks.")
else:
    print("  → Negative/no correlation between attendance and marks.")

# 4d. Group by gender and calculate average marks
print("\n[4d] Average marks grouped by gender:")
gender_group = df.groupby('gender')[['math_score', 'science_score', 'average_score']].mean().round(2)
print(gender_group)

print("\n" + "=" * 60)
print("   Assessment Complete!")
print("=" * 60)