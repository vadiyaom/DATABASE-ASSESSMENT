"""
Task 1: Daily Order Analysis with NumPy
Assessment: Data Science M4-A1 | Modules 3-4
Platform: Food Delivery Analytics
"""

import numpy as np

def main():
    print("=" * 70)
    print("SECTION B - TASK 1: DAILY ORDER ANALYSIS WITH NUMPY")
    print("=" * 70)

    # 1. Set seed for reproducibility and generate arrays
    np.random.seed(42)
    daily_orders = np.random.randint(100, 801, size=30)
    daily_revenue = np.random.uniform(5000.0, 50000.0, size=30)

    print("\n[1] Generated Datasets (30 Days):")
    print(f"Daily Orders Array (shape: {daily_orders.shape}):\n{daily_orders}")
    print(f"\nDaily Revenue Array Sample (first 5 days):\n{np.round(daily_revenue[:5], 2)}")

    # 2. Calculate summary statistics
    total_orders = np.sum(daily_orders)
    total_revenue = np.sum(daily_revenue)
    mean_orders = np.mean(daily_orders)
    std_orders = np.std(daily_orders)
    max_rev_index = np.argmax(daily_revenue)
    max_rev_value = daily_revenue[max_rev_index]

    print("\n" + "-" * 70)
    print("[2] Summary Statistics:")
    print(f"  • Total Orders across 30 days      : {total_orders:,}")
    print(f"  • Total Revenue across 30 days     : ${total_revenue:,.2f}")
    print(f"  • Mean Daily Orders                : {mean_orders:.2f}")
    print(f"  • Standard Deviation of Orders     : {std_orders:.2f}")
    print(f"  • Day with Highest Revenue         : Day {max_rev_index} (0-indexed) / Day {max_rev_index + 1} (1-indexed)")
    print(f"  • Peak Day Revenue                 : ${max_rev_value:,.2f}")

    # 3. Boolean indexing: Surge/Peak days where orders > mean + 1 std dev
    threshold = mean_orders + (1.0 * std_orders)
    peak_mask = daily_orders > threshold
    peak_days_indices = np.where(peak_mask)[0]
    peak_orders = daily_orders[peak_mask]
    peak_revenue = daily_revenue[peak_mask]
    peak_count = len(peak_orders)
    total_peak_revenue = np.sum(peak_revenue)

    print("\n" + "-" * 70)
    print(f"[3] Peak Days Analysis (Threshold: Orders > {threshold:.2f}):")
    print(f"  • Number of Peak Days Identified   : {peak_count}")
    print(f"  • Peak Days (0-indexed indices)    : {peak_days_indices.tolist()}")
    print(f"  • Orders on Peak Days              : {peak_orders.tolist()}")
    print(f"  • Combined Revenue on Peak Days    : ${total_peak_revenue:,.2f}")
    print(f"  • Revenue Share of Peak Days       : {(total_peak_revenue / total_revenue) * 100:.2f}%")

    # 4. Reshape 30-element order array into 5x6 matrix and sum along axis=1
    weekly_matrix = daily_orders.reshape(5, 6)
    weekly_totals = np.sum(weekly_matrix, axis=1)

    print("\n" + "-" * 70)
    print("[4] Weekly Block Reshaping (5 Blocks x 6 Days):")
    print("Reshaped 5x6 Matrix:")
    print(weekly_matrix)
    print("\nTotal Orders per Weekly Block (np.sum(axis=1)):")
    for block_num, total in enumerate(weekly_totals, start=1):
        print(f"  • Block {block_num} (Days {(block_num-1)*6 + 1:02d}-{block_num*6:02d}) : {total:,} orders")

    print("\nVerification: Sum of Weekly Blocks =", np.sum(weekly_totals), "(Matches Total Orders:", total_orders == np.sum(weekly_totals), ")")
    print("=" * 70)
    print("TASK 1 COMPLETED SUCCESSFULLY.")
    print("=" * 70)

if __name__ == "__main__":
    main()
