"""
Task 3: Food Delivery Visualisation Dashboard
Assessment: Data Science M4-A1 | Modules 3-4
Platform: Food Delivery Analytics
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Import the data cleaning pipeline from Task 2
from task2_data_cleaning import create_raw_dataset

def get_cleaned_data():
    df = create_raw_dataset()
    # Missing value imputation
    med_delivery = df["delivery_time_mins"].median()
    med_order_val = df["order_value"].median()
    mean_rating = round(df["rating"].mean(), 1)
    mode_category = df["category"].mode()[0]

    df["delivery_time_mins"] = df["delivery_time_mins"].fillna(med_delivery)
    df["order_value"] = df["order_value"].fillna(med_order_val)
    df["rating"] = df["rating"].fillna(mean_rating)
    df["category"] = df["category"].fillna(mode_category)

    # Deduplication
    df_cleaned = df.drop_duplicates().copy()

    # Outlier capping
    Q1 = df_cleaned["order_value"].quantile(0.25)
    Q3 = df_cleaned["order_value"].quantile(0.75)
    IQR = Q3 - Q1
    upper_fence = Q3 + 1.5 * IQR
    df_cleaned["order_value"] = df_cleaned["order_value"].clip(lower=0, upper=upper_fence)

    return df_cleaned

def main():
    print("=" * 75)
    print("SECTION B - TASK 3: FOOD DELIVERY VISUALISATION DASHBOARD")
    print("=" * 75)

    # 1. Load cleaned data
    df = get_cleaned_data()
    print(f"\n[1] Data Loaded Successfully: {df.shape[0]} rows, {df.shape[1]} columns.")

    # 2. Configure Matplotlib & Seaborn aesthetics
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        'font.sans-serif': 'Segoe UI',
        'font.family': 'sans-serif',
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'axes.labelweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
    })

    # 3. Create 2x2 subplot figure
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Food Delivery Operational & Financial Analytics Dashboard", fontsize=16, fontweight='bold', y=0.98)

    # -------------------------------------------------------------
    # Plot 1 (top-left): Seaborn countplot showing order count per category
    # -------------------------------------------------------------
    order_order = df['category'].value_counts().index
    sns.countplot(
        data=df, 
        x='category', 
        order=order_order, 
        ax=axes[0, 0], 
        palette='viridis',
        hue='category',
        legend=False
    )
    axes[0, 0].set_title("Plot 1: Order Volume by Cuisine Category", pad=10)
    axes[0, 0].set_xlabel("Cuisine Category")
    axes[0, 0].set_ylabel("Total Number of Orders")
    # Add count labels on top of bars
    for p in axes[0, 0].patches:
        height = int(p.get_height())
        if height > 0:
            axes[0, 0].annotate(f"{height}",
                                (p.get_x() + p.get_width() / 2., height),
                                ha='center', va='bottom',
                                xytext=(0, 3), textcoords='offset points',
                                fontweight='semibold')

    # -------------------------------------------------------------
    # Plot 2 (top-right): Seaborn boxplot showing delivery_time_mins by category
    # -------------------------------------------------------------
    sns.boxplot(
        data=df, 
        x='category', 
        y='delivery_time_mins', 
        ax=axes[0, 1], 
        palette='Spectral',
        hue='category',
        legend=False,
        boxprops=dict(alpha=0.85)
    )
    axes[0, 1].set_title("Plot 2: Delivery Time Distribution by Category", pad=10)
    axes[0, 1].set_xlabel("Cuisine Category")
    axes[0, 1].set_ylabel("Delivery Duration (Minutes)")
    axes[0, 1].tick_params(axis='x', rotation=15)

    # -------------------------------------------------------------
    # Plot 3 (bottom-left): Matplotlib horizontal bar chart of avg order_value per restaurant
    # -------------------------------------------------------------
    avg_order_rest = df.groupby('restaurant_name')['order_value'].mean().sort_values()
    colors = plt.cm.plasma(np.linspace(0.2, 0.85, len(avg_order_rest)))
    
    bars = axes[1, 0].barh(avg_order_rest.index, avg_order_rest.values, color=colors, edgecolor='none', height=0.65)
    axes[1, 0].set_title("Plot 3: Average Order Value by Restaurant", pad=10)
    axes[1, 0].set_xlabel("Average Order Value ($)")
    axes[1, 0].set_ylabel("Restaurant Partner")
    # Add value labels at end of horizontal bars
    for bar in bars:
        width = bar.get_width()
        axes[1, 0].annotate(f"${width:.2f}",
                            (width, bar.get_y() + bar.get_height() / 2.),
                            ha='left', va='center',
                            xytext=(5, 0), textcoords='offset points',
                            fontsize=9, fontweight='semibold')
    axes[1, 0].set_xlim(0, max(avg_order_rest.values) * 1.18)

    # -------------------------------------------------------------
    # Plot 4 (bottom-right): Seaborn heatmap of correlation matrix of numeric columns
    # -------------------------------------------------------------
    numeric_df = df[['delivery_time_mins', 'order_value', 'rating']]
    corr_matrix = numeric_df.corr()
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt=".3f", 
        cmap='coolwarm', 
        vmin=-1, 
        vmax=1, 
        ax=axes[1, 1], 
        linewidths=1.2, 
        linecolor='white',
        cbar_kws={'label': 'Pearson Correlation (r)'}
    )
    axes[1, 1].set_title("Plot 4: Correlation Matrix (Numeric Features)", pad=10)
    axes[1, 1].set_xlabel("Operational & Financial Metrics")
    axes[1, 1].set_ylabel("Operational & Financial Metrics")

    # 4. Prevent overlapping with tight_layout()
    plt.tight_layout()

    # 5. Save figure with exact specifications
    output_filename = "food_delivery_dashboard.png"
    plt.savefig(output_filename, dpi=150, bbox_inches='tight')
    plt.close()

    # 6. Confirm file is saved with print statement
    if os.path.exists(output_filename):
        file_size_kb = os.path.getsize(output_filename) / 1024
        print(f"\n[SUCCESS] Multi-panel visualization dashboard successfully created and saved:")
        print(f"  * File Path : {os.path.abspath(output_filename)}")
        print(f"  * Resolution: 150 DPI")
        print(f"  * File Size : {file_size_kb:.2f} KB")
    else:
        print("\n[ERROR] Failed to save the dashboard image.")

    print("=" * 75)
    print("TASK 3 COMPLETED SUCCESSFULLY.")
    print("=" * 75)

if __name__ == "__main__":
    main()
