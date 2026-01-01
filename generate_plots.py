import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

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

    # Ensure date column
    if 'date' not in df.columns and 'Date' in df.columns:
        df.rename(columns={'Date': 'date'}, inplace=True)
        
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month_name()
        df['year'] = df['date'].dt.year
        df['season'] = df['date'].dt.month.map({1:'Winter', 2:'Winter', 3:'Spring', 4:'Spring', 5:'Spring', 6:'Summer', 7:'Summer', 8:'Summer', 9:'Fall', 10:'Fall', 11:'Fall', 12:'Winter'})
    
    target_col = 'ozone_ppb' if 'ozone_ppb' in df.columns else 'ozone'
    if target_col not in df.columns: 
        print("Target column (ozone/ozone_ppb) not found.") 
        return

    print("Generating plots...")

    # --- 1. Advanced Distributions ---
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.kdeplot(df[target_col].dropna(), fill=True, color="teal", label="Overall Ozone", ax=ax)
        if 'season' in df.columns:
            for season in df['season'].unique():
                subset = df[df['season']==season][target_col].dropna()
                if len(subset) > 1:
                    sns.kdeplot(subset, fill=False, label=season, ax=ax)
        plt.title('Ozone Distribution (Overall vs Seasonal)')
        plt.legend()
        plt.savefig(os.path.join(output_dir, 'ozone_kde_seasonal.png'))
        plt.close()
        print(" - Saved ozone_kde_seasonal.png")
    except Exception as e:
        print(f"Failed to generate ozone_kde_seasonal.png: {e}")

    # --- 2. Wind Rose (Approximation) ---
    try:
        if 'wdir' in df.columns and 'wspd' in df.columns:
            df_wind = df.dropna(subset=['wdir', 'wspd']).copy()
            if not df_wind.empty:
                plt.figure(figsize=(8, 8))
                ax = plt.subplot(111, polar=True)
                # Binning wind direction
                df_wind['wdir_bin'] = pd.cut(df_wind['wdir'], bins=np.linspace(0, 360, 17), labels=np.linspace(0, 360, 17)[:-1])
                # Average wind speed per direction
                wind_stats = df_wind.groupby('wdir_bin', observed=False)['wspd'].mean().reset_index()
                # Drop NaNs if any bin is empty
                wind_stats = wind_stats.dropna()
                
                if not wind_stats.empty:
                    bars = ax.bar(np.deg2rad(wind_stats['wdir_bin'].astype(float)), wind_stats['wspd'], 
                           width=0.3, bottom=0.0, color='turquoise', alpha=0.8)
                    ax.set_theta_zero_location('N')
                    ax.set_theta_direction(-1) # Clockwise
                    plt.title('Wind Rose: Avg Wind Speed by Direction')
                    plt.savefig(os.path.join(output_dir, 'wind_rose_approximation.png'))
                    plt.close()
                    print(" - Saved wind_rose_approximation.png")
    except Exception as e:
        print(f"Failed to generate wind_rose_approximation.png: {e}")

    # --- 3. 3D Scatter Plot (Static) ---
    try:
        if 'tmax' in df.columns and 'CUTI' in df.columns:
            df_3d = df.dropna(subset=['tmax', 'CUTI', target_col]).sample(n=min(1000, len(df)), random_state=42) # Sample for performance/clarity
            if not df_3d.empty:
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                sc = ax.scatter(df_3d['tmax'], df_3d['CUTI'], df_3d[target_col], c=df_3d[target_col], cmap='viridis', s=20, alpha=0.6)
                ax.set_xlabel('Max Temp (°C)')
                ax.set_ylabel('CUTI (Upwelling)')
                ax.set_zlabel('Ozone (ppb)')
                plt.title('3D Plot: Ozone vs Temp vs Upwelling')
                plt.colorbar(sc, label='Ozone (ppb)')
                plt.savefig(os.path.join(output_dir, '3d_ozone_temp_cuti.png'))
                plt.close()
                print(" - Saved 3d_ozone_temp_cuti.png")
    except Exception as e:
        print(f"Failed to generate 3d_ozone_temp_cuti.png: {e}")

    # --- 4. Ocean-Atmosphere Interaction (BEUTI vs CUTI) ---
    try:
        if 'CUTI' in df.columns and 'BEUTI' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.regplot(x='CUTI', y='BEUTI', data=df, scatter_kws={'alpha':0.3, 'color':'navy', 's': 10}, line_kws={'color':'red'})
            plt.title('Ocean Dynamics: CUTI vs BEUTI')
            plt.xlabel('Coastal Upwelling Transport Index (CUTI)')
            plt.ylabel('Biologically Effective Upwelling (BEUTI)')
            plt.savefig(os.path.join(output_dir, 'ocean_dynamics_cuti_beuti.png'))
            plt.close()
            print(" - Saved ocean_dynamics_cuti_beuti.png")
    except Exception as e:
        print(f"Failed to generate ocean_dynamics_cuti_beuti.png: {e}")

    # --- 5. Rolling Statistics (Time Series) ---
    try:
        if 'date' in df.columns:
            df_sorted = df.sort_values('date').copy()
            df_sorted['ozone_roll_30'] = df_sorted[target_col].rolling(window=30).mean()
            df_sorted['ozone_roll_7'] = df_sorted[target_col].rolling(window=7).mean()
            
            plt.figure(figsize=(14, 7))
            plt.plot(df_sorted['date'], df_sorted[target_col], label='Daily Ozone', alpha=0.3, color='gray')
            plt.plot(df_sorted['date'], df_sorted['ozone_roll_7'], label='7-Day Rolling Avg', color='blue', linewidth=1)
            plt.plot(df_sorted['date'], df_sorted['ozone_roll_30'], label='30-Day Rolling Avg', color='red', linewidth=2)
            plt.title('Ozone Time Series with Rolling Averages')
            plt.legend()
            plt.savefig(os.path.join(output_dir, 'ozone_rolling_stats.png'))
            plt.close()
            print(" - Saved ozone_rolling_stats.png")
    except Exception as e:
        print(f"Failed to generate ozone_rolling_stats.png: {e}")

    # --- 6. Correlation Heatmap (Refined) ---
    try:
        numeric_top = df.select_dtypes(include=[np.number])
        if target_col in numeric_top.columns:
            # Focus on top 20 correlated features
            cors = numeric_top.corrwith(numeric_top[target_col]).abs().sort_values(ascending=False).head(20).index
            plt.figure(figsize=(12, 10))
            sns.heatmap(numeric_top[cors].corr(), annot=True, cmap='RdBu', center=0, fmt=".2f", linewidths=0.5)
            plt.title('Top 20 Features Correlation Matrix')
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'correlation_top20.png'))
            plt.close()
            print(" - Saved correlation_top20.png")
    except Exception as e:
        print(f"Failed to generate correlation_top20.png: {e}")

    # --- 7. Seasonal Boxplots ---
    try:
        if 'month' in df.columns:
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                           'July', 'August', 'September', 'October', 'November', 'December']
            plt.figure(figsize=(14, 6))
            sns.boxplot(x='month', y=target_col, data=df, order=month_order, palette='Set3', hue='month', legend=False)
            plt.title('Monthly Ozone Variance (Boxplot)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'ozone_monthly_boxplot.png'))
            plt.close()
            print(" - Saved ozone_monthly_boxplot.png")
    except Exception as e:
        print(f"Failed to generate ozone_monthly_boxplot.png: {e}")

    # --- 8. SST Anomaly vs Ozone ---
    try:
        if 'sst_anomaly' in df.columns and 'season' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x='sst_anomaly', y=target_col, data=df, hue='season', alpha=0.6)
            plt.title('Ozone vs SST Anomaly')
            plt.axvline(0, color='black', linestyle='--')
            plt.savefig(os.path.join(output_dir, 'ozone_sst_anomaly.png'))
            plt.close()
            print(" - Saved ozone_sst_anomaly.png")
    except Exception as e:
        print(f"Failed to generate ozone_sst_anomaly.png: {e}")

    print(f"Procesing complete. Check {output_dir} for results.")

if __name__ == "__main__":
    generate_plots()
