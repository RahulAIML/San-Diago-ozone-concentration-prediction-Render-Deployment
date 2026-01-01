import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'figure.max_open_warning': 0})

def generate_plots(data_path="final_cal.csv", output_dir="report_plots"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Loading data from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: {data_path} not found.")
        return

    # Ensure date column exists and is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    print("Generating plots...")

    # 1. Target Variable Distribution (Ozone)
    if 'ozone' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df['ozone'], kde=True, color='skyblue')
        plt.title('Distribution of Ozone Levels')
        plt.xlabel('Ozone (ppb)')
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(output_dir, 'ozone_distribution.png'))
        plt.close()
        print(" - Ozone distribution plot saved.")

    # 2. Correlation Heatmap (Top numeric features)
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        # Calculate correlation with ozone if it exists
        if 'ozone' in numeric_df.columns:
            corr_with_ozone = numeric_df.corrwith(numeric_df['ozone']).abs().sort_values(ascending=False)
            top_features = corr_with_ozone.head(15).index.tolist()
            corr_matrix = numeric_df[top_features].corr()
        else:
            corr_matrix = numeric_df.corr()
            
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Correlation Heatmap (Top Features)')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
        plt.close()
        print(" - Correlation heatmap saved.")

    # 3. Time Series of Ozone
    if 'date' in df.columns and 'ozone' in df.columns:
        plt.figure(figsize=(14, 6))
        plt.plot(df['date'], df['ozone'], label='Ozone', color='royalblue', alpha=0.7)
        plt.title('Ozone Levels Over Time')
        plt.xlabel('Date')
        plt.ylabel('Ozone (ppb)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'ozone_time_series.png'))
        plt.close()
        print(" - Ozone time series saved.")

    # 4. Ozone vs Temperature (Scatter)
    if 'tmax' in df.columns and 'ozone' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='tmax', y='ozone', data=df, hue='ozone', palette='viridis', alpha=0.6)
        plt.title('Ozone vs Max Temperature')
        plt.xlabel('Max Temperature (°C)')
        plt.ylabel('Ozone (ppb)')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'ozone_vs_temp.png'))
        plt.close()
        print(" - Ozone vs Temp scatter saved.")

    # 5. Ozone vs CUTI (Scatter)
    if 'CUTI' in df.columns and 'ozone' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='CUTI', y='ozone', data=df, color='orange', alpha=0.6)
        plt.title('Ozone vs Upwelling Index (CUTI)')
        plt.xlabel('CUTI')
        plt.ylabel('Ozone (ppb)')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'ozone_vs_cuti.png'))
        plt.close()
        print(" - Ozone vs CUTI scatter saved.")

    # 6. Monthly Average Ozone
    if 'date' in df.columns and 'ozone' in df.columns:
        df['month'] = df['date'].dt.month_name()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                       'July', 'August', 'September', 'October', 'November', 'December']
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x='month', y='ozone', data=df, order=month_order, errorbar=None, palette='viridis')
        plt.title('Average Ozone Levels by Month')
        plt.xticks(rotation=45)
        plt.ylabel('Average Ozone (ppb)')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'ozone_monthly_avg.png'))
        plt.close()
        print(" - Monthly average ozone saved.")

    print(f"All plots saved to {output_dir}")

if __name__ == "__main__":
    generate_plots()
