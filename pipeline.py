import pandas as pd
import os
import numpy as np

# =========================
# 1. LOAD RAW DATA
# =========================
df = pd.read_csv("raw_data/sales.csv", encoding="latin1")

print("Original rows:", len(df))

# =========================
# 2. CLEAN DATA
# =========================

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Remove rows where sales is missing
if "sales" in df.columns:
    df.dropna(subset=["sales"], inplace=True)

# Convert order_date to datetime
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df[df["order_date"].notna()]

# Create revenue column
if "sales" in df.columns:
    df["revenue"] = df["sales"]

print("Rows after cleaning:", len(df))

# =========================
# 3. SCALE DATA TO 100K (REALISTIC)
# =========================

target_rows = 100000
multiplier = target_rows // len(df) + 1

scaled_data = []

for i in range(multiplier):
    temp = df.copy()

    # FIX: convert order_id to numeric before modifying
    if "order_id" in temp.columns:
        temp["order_id"] = pd.to_numeric(temp["order_id"], errors="coerce")
        temp["order_id"] = temp["order_id"].fillna(0).astype(int)
        temp["order_id"] = temp["order_id"] + (i * 100000)

    # Slight variation in revenue
    if "revenue" in temp.columns:
        temp["revenue"] = temp["revenue"] * (1 + np.random.uniform(0.01, 0.05))

    # Shift dates slightly
    if "order_date" in temp.columns:
        temp["order_date"] = temp["order_date"] + pd.to_timedelta(i, unit="D")

    scaled_data.append(temp)

df = pd.concat(scaled_data, ignore_index=True)
df = df.head(target_rows)

print("Final rows after scaling:", len(df))

# =========================
# 4. SAVE CLEANED DATA
# =========================

os.makedirs("processed_data", exist_ok=True)
df.to_csv("processed_data/cleaned_sales.csv", index=False)

print("Cleaned dataset saved successfully.")

# =========================
# 5. LOAD DATA INTO DATABASE
# =========================

from sqlalchemy import create_engine

# Create SQLite database
engine = create_engine("sqlite:///database/sales.db")

# Load cleaned CSV
clean_df = pd.read_csv("processed_data/cleaned_sales.csv")

# Insert into database
clean_df.to_sql("sales_data", engine, if_exists="replace", index=False)

print("Data inserted into SQLite database successfully.")