"""
Task 2: Food Delivery Orders Data Cleaning Pipeline
Assessment: Data Science M4-A1 | Modules 3-4
Platform: Food Delivery Analytics
"""

import pandas as pd
import numpy as np

def create_raw_dataset():
    # Base dataset of 22 rows
    data = [
        {"order_id": 1001, "customer_name": "Aarav Sharma",   "restaurant_name": "Spice Villa",       "category": "North Indian", "delivery_time_mins": 35.0, "order_value": 450.0,  "rating": 4.5},
        {"order_id": 1002, "customer_name": "Diya Patel",     "restaurant_name": "Pizza Roma",        "category": "Italian",      "delivery_time_mins": 28.0, "order_value": 680.0,  "rating": 4.8},
        {"order_id": 1003, "customer_name": "Rohan Mehta",    "restaurant_name": "Burger Barn",       "category": "Fast Food",    "delivery_time_mins": np.nan, "order_value": 320.0, "rating": 3.9}, # Missing numeric 1
        {"order_id": 1004, "customer_name": "Ananya Roy",     "restaurant_name": "Dragon Wok",        "category": "Chinese",      "delivery_time_mins": 42.0, "order_value": 850.0,  "rating": 4.2},
        {"order_id": 1005, "customer_name": "Kabir Singh",    "restaurant_name": "Tandoor Treats",    "category": np.nan,         "delivery_time_mins": 50.0, "order_value": np.nan,  "rating": 4.1}, # Missing categorical 1 & numeric 2
        {"order_id": 1006, "customer_name": "Ishita Verma",   "restaurant_name": "Spice Villa",       "category": "North Indian", "delivery_time_mins": 31.0, "order_value": 520.0,  "rating": 4.6},
        {"order_id": 1007, "customer_name": "Siddharth Rao",  "restaurant_name": "Subway Express",    "category": "Fast Food",    "delivery_time_mins": 22.0, "order_value": 290.0,  "rating": np.nan}, # Missing numeric 3
        {"order_id": 1008, "customer_name": "Pooja Hegde",    "restaurant_name": "Pasta Fresca",      "category": "Italian",      "delivery_time_mins": 45.0, "order_value": 920.0,  "rating": 4.4},
        {"order_id": 1009, "customer_name": "Vikram Joshi",   "restaurant_name": "Royal Biryani",     "category": "North Indian", "delivery_time_mins": 38.0, "order_value": 2800.0, "rating": 4.7}, # Outlier order_value
        {"order_id": 1010, "customer_name": "Neha Gupta",     "restaurant_name": "Green Bowl",        "category": "Healthy",      "delivery_time_mins": np.nan, "order_value": 610.0, "rating": 4.3}, # Missing numeric 4
        {"order_id": 1011, "customer_name": "Aditya Kulkarni","restaurant_name": "Dragon Wok",        "category": "Chinese",      "delivery_time_mins": 40.0, "order_value": 740.0,  "rating": 4.0},
        {"order_id": 1012, "customer_name": "Meera Nair",     "restaurant_name": "Spice Villa",       "category": "North Indian", "delivery_time_mins": 33.0, "order_value": 480.0,  "rating": 4.9},
        {"order_id": 1013, "customer_name": "Tanmay Bhat",    "restaurant_name": "Burger Barn",       "category": "Fast Food",    "delivery_time_mins": 25.0, "order_value": 310.0,  "rating": 3.7},
        {"order_id": 1014, "customer_name": "Sneha Iyer",     "restaurant_name": "Dosa Hub",          "category": "South Indian", "delivery_time_mins": 20.0, "order_value": 220.0,  "rating": 4.6},
        {"order_id": 1015, "customer_name": "Varun Dhawan",   "restaurant_name": "Pizza Roma",        "category": "Italian",      "delivery_time_mins": 36.0, "order_value": 3500.0, "rating": 4.5}, # Outlier order_value
        {"order_id": 1016, "customer_name": "Kavita Pillai",  "restaurant_name": "Royal Biryani",     "category": "North Indian", "delivery_time_mins": 48.0, "order_value": 1150.0, "rating": 4.8},
        {"order_id": 1017, "customer_name": "Arjun Kapoor",   "restaurant_name": "Subway Express",    "category": "Fast Food",    "delivery_time_mins": 26.0, "order_value": 340.0,  "rating": 3.8},
        {"order_id": 1018, "customer_name": "Tara Sutaria",   "restaurant_name": "Green Bowl",        "category": "Healthy",      "delivery_time_mins": 30.0, "order_value": 580.0,  "rating": 4.4},
        {"order_id": 1019, "customer_name": "Rahul Deshmukh", "restaurant_name": "Dosa Hub",          "category": "South Indian", "delivery_time_mins": 24.0, "order_value": 260.0,  "rating": 4.7},
        {"order_id": 1020, "customer_name": "Simran Kaur",    "restaurant_name": "Tandoor Treats",    "category": "North Indian", "delivery_time_mins": 44.0, "order_value": 890.0,  "rating": 4.3},
    ]
    df = pd.DataFrame(data)

    # Introduce 3 duplicate rows (duplicating row 1, row 3, row 7)
    duplicates = df.iloc[[1, 3, 7]].copy()
    df_with_dupes = pd.concat([df, duplicates], ignore_index=True)
    return df_with_dupes

def main():
    print("=" * 75)
    print("SECTION B - TASK 2: FOOD DELIVERY ORDERS DATA CLEANING PIPELINE")
    print("=" * 75)

    # 1. Create simulated DataFrame
    df = create_raw_dataset()
    print(f"\n[1] Initial Raw Dataset Created:")
    print(f"  * Total rows: {len(df)}, Total columns: {len(df.columns)}")
    print(f"  * Columns: {list(df.columns)}")
    print("\nSample Raw Records (first 6 rows):")
    print(df.head(6).to_string(index=False))

    # 2. Inspect and Handle Missing Values
    print("\n" + "-" * 75)
    print("[2] Missing Value Imputation:")
    print("Null Counts BEFORE Imputation:")
    print(df.isnull().sum())

    # Imputation strategies:
    # - delivery_time_mins: median
    # - order_value: median
    # - rating: mean rounded to 1 decimal
    # - category: mode
    med_delivery = df["delivery_time_mins"].median()
    med_order_val = df["order_value"].median()
    mean_rating = round(df["rating"].mean(), 1)
    mode_category = df["category"].mode()[0]

    print(f"\nComputed Imputation Values:")
    print(f"  * Median 'delivery_time_mins' : {med_delivery:.1f} mins")
    print(f"  * Median 'order_value'        : ${med_order_val:.2f}")
    print(f"  * Mean 'rating' (rounded 1 dec): {mean_rating:.1f}")
    print(f"  * Mode 'category'             : '{mode_category}'")

    df["delivery_time_mins"] = df["delivery_time_mins"].fillna(med_delivery)
    df["order_value"] = df["order_value"].fillna(med_order_val)
    df["rating"] = df["rating"].fillna(mean_rating)
    df["category"] = df["category"].fillna(mode_category)

    print("\nNull Counts AFTER Imputation:")
    print(df.isnull().sum())

    # 3. Deduplication
    print("\n" + "-" * 75)
    print("[3] Duplicate Removal:")
    shape_before = df.shape
    df_cleaned = df.drop_duplicates().copy()
    shape_after = df_cleaned.shape
    dupes_removed = shape_before[0] - shape_after[0]

    print(f"  * Shape BEFORE deduplication : {shape_before} ({shape_before[0]} rows, {shape_before[1]} cols)")
    print(f"  * Shape AFTER deduplication  : {shape_after} ({shape_after[0]} rows, {shape_after[1]} cols)")
    print(f"  * Total duplicate rows removed: {dupes_removed}")

    # 4. Outlier Detection and Capping via IQR
    print("\n" + "-" * 75)
    print("[4] Outlier Detection & Capping on 'order_value' (IQR Method):")
    Q1 = df_cleaned["order_value"].quantile(0.25)
    Q3 = df_cleaned["order_value"].quantile(0.75)
    IQR = Q3 - Q1
    lower_fence = Q1 - 1.5 * IQR
    upper_fence = Q3 + 1.5 * IQR

    print(f"  * Q1 (25th percentile) : ${Q1:.2f}")
    print(f"  * Q3 (75th percentile) : ${Q3:.2f}")
    print(f"  * IQR (Q3 - Q1)        : ${IQR:.2f}")
    print(f"  * Lower Fence (Q1-1.5*IQR): ${lower_fence:.2f} (Floor at $0)")
    print(f"  * Upper Fence (Q3+1.5*IQR): ${upper_fence:.2f}")

    outlier_mask = (df_cleaned["order_value"] < lower_fence) | (df_cleaned["order_value"] > upper_fence)
    outlier_rows = df_cleaned[outlier_mask]

    print(f"\nDetected Outlier Rows ({len(outlier_rows)} records exceeding fences):")
    print(outlier_rows[["order_id", "customer_name", "restaurant_name", "order_value"]].to_string(index=False))

    # Cap outliers at upper fence using clip()
    df_cleaned["order_value_uncapped"] = df_cleaned["order_value"]
    df_cleaned["order_value"] = df_cleaned["order_value"].clip(lower=max(0, lower_fence), upper=upper_fence)

    print(f"\nOutlier Capping Summary (using df['order_value'].clip(upper={upper_fence:.2f})):")
    for idx, row in df_cleaned[outlier_mask].iterrows():
        print(f"  * Order #{int(row['order_id'])} ({row['customer_name']}): Original ${row['order_value_uncapped']:.2f} --> Capped to ${row['order_value']:.2f}")

    df_cleaned.drop(columns=["order_value_uncapped"], inplace=True)

    print("\n" + "-" * 75)
    print("[5] Final Cleaned Dataset Preview (first 10 rows):")
    print(df_cleaned.head(10).to_string(index=False))
    print(f"\nFinal Cleaned Dataset Shape: {df_cleaned.shape}")
    print("=" * 75)
    print("TASK 2 COMPLETED SUCCESSFULLY.")
    print("=" * 75)

    return df_cleaned

if __name__ == "__main__":
    main()
