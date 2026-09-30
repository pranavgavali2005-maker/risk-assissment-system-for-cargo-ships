import pandas as pd

print("Scanning latest maritime weather predictions for active routes...")

# Load the AI predictions dataset
try:
  df = pd.read_csv("bay_of_bengal_risk_predictions.csv")
except FileNotFoundError:
  print("Error: Please run 'train_model.py' first to generate predictions.")
  exit()

# Define your key Indian East Coast destination ports (Approximate coordinates)
target_ports = {
    "Paradip": (20.26, 86.68),
    "Vizag": (17.68, 83.21),
    "Gangavaram": (17.59, 83.25),
    "Haldia": (22.03, 88.06),
    "Dhamra": (21.08, 86.97),
    "Gopalpur": (19.26, 84.90),
}

print("\n" + "=" * 50)
print(" 🚢 MARITIME RISK NOTIFICATION SYSTEM ")
print("=" * 50)

# Threshold for triggering a high-risk warning (out of 100)
RISK_THRESHOLD = 50.0

alerts_triggered = 0

# Check data points near your target ports or high-risk zones
for port_name, (port_lat, port_lon) in target_ports.items():
  # Find weather data points within ~1 degree of the port
  nearby_data = df[
      (df["latitude"].between(port_lat - 1.0, port_lat + 1.0))
      & (df["longitude"].between(port_lon - 1.0, port_lon + 1.0))
  ]

  if not nearby_data.empty:
    avg_risk = nearby_data["predicted_risk_score"].mean()
    max_swh = nearby_data["swh"].max()
    max_wind = nearby_data["wind_speed"].max()

    if avg_risk >= RISK_THRESHOLD:
      print(f"\n🔴 HIGH RISK ALERT near {port_name} port!")
      print(f"   • Risk Score: {avg_risk:.1f} / 100")
      print(f"   • Max Wave Height: {max_swh:.2f} meters")
      print(f"   • Max Wind Speed: {max_wind:.2f} m/s")
      print(f"   • Status: Recommendation to delay entry or reroute.")
      alerts_triggered += 1
    else:
      print(
          f"🟢 {port_name} Port Area: Safe conditions (Risk Score:"
          f" {avg_risk:.1f}/100)"
      )

print("\n" + "=" * 50)
if alerts_triggered == 0:
  print("Summary: All monitored port approaches are currently clear of severe weather risks.")
else:
  print(f"Summary: {alerts_triggered} high-risk weather alerts generated.")
print("=" * 50)