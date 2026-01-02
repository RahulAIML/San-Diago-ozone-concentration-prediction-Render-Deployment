# Ozone Ocean Predictor - San Diego

This is an academic project designed to predict Ozone levels in San Diego based on Ocean Upwelling indices (CUTI/BEUTI) and meteorological data.

## 🚀Features
- **Machine Learning Model**: Uses Random Forest/XGBoost to forecast Ozone levels.
- **Interactive Frontend**: React-based UI for inputting parameters and viewing predictions.
- **Advanced EDA**: Comprehensive exploratory data analysis plots available in `report_plots/`.
- **Regime Detection**: Identifies atmospheric regimes based on upwelling and temperature.
- **Lightweight Backend**: Minimal Flask API replacing the original Django backend for easier deployment.

## 🛠️ Tech Stack
- **Frontend**: React (Vite), TailwindCSS, Recharts.
- **Backend**: Python (Flask), SQLite.
- **Data Science**: Pandas, Scikit-learn, Seaborn.
- **Deployment**: Configured for Render.com.

## 🏃‍♂️ Running Locally

### Prerequisites
- Python 3.9+
- Node.js & npm

### Steps
1. **Clone the repository** (if not already done).
2. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Build Frontend**:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```
4. **Run the Application**:
   ```bash
   python app.py
   ```
   The app will be available at `http://localhost:5000`.

## 📊 Analytics
Check the `report_plots/` directory for generated visualizations:
- `wind_rose_approximation.png`: Wind patterns.
- `3d_ozone_temp_cuti.png`: 3D relationship between temperature, upwelling, and ozone.
- `ozone_kde_seasonal.png`: Seasonal distribution of ozone levels.

## 🧪 Testing
Run the end-to-end test suite to verify functionality:
```bash
python test_e2e.py
```
