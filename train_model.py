import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

print("1. Loading the finalized marine dataset...")
df = pd.read_csv("final_training_data.csv")

print("2. Engineering the Maritime Risk Score...")
# Calculate total wind speed (magnitude of u and v vectors)
df['wind_speed'] = np.sqrt(df['u10']**2 + df['v10']**2)

# Create a baseline Risk Score (0 to 100)
# High waves, fast winds, and low pressure increase the risk
baseline_pressure = 101325  # Standard atmospheric pressure in Pascals
df['risk_score'] = (
    (df['swh'] * 15) +           # Wave height multiplier
    (df['wind_speed'] * 2.5) +   # Wind speed multiplier
    ((baseline_pressure - df['msl']) * 0.05) # Pressure drop penalty
)

# Normalize the score to strictly fall between 0 (Safe) and 100 (Extreme Danger)
df['risk_score'] = df['risk_score'].clip(0, 100)

print("3. Preparing features for the AI...")
# Features (X) and Target (y)
features = ['latitude', 'longitude', 'u10', 'v10', 'msl', 'sst', 'swh', 'wind_speed']
X = df[features]
y = df['risk_score']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("4. Training the XGBoost Model...")
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5
)
model.fit(X_train, y_train)

# Test the accuracy
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Model Training Complete! Error Margin (RMSE): {rmse:.2f} risk points")

print("5. Generating full map predictions...")
# Predict risk for the entire grid to feed the map
df['predicted_risk_score'] = model.predict(X)

# Save the predictions for the Folium map to read
output_map_file = "bay_of_bengal_risk_predictions.csv"
df.to_csv(output_map_file, index=False)
print(f"Success! Predictions saved to {output_map_file}")
