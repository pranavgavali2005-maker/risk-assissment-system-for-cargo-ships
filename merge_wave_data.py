import os
import zipfile
import pandas as pd
import xarray as xr

wave_file = "download_waves.nc"

print("1. Inspecting and unzipping wave data...")
if zipfile.is_zipfile(wave_file):
  with zipfile.ZipFile(wave_file, "r") as zip_ref:
    zip_ref.extractall("extracted_waves")
    real_file_name = zip_ref.namelist()[0]
  actual_nc_path = os.path.join("extracted_waves", real_file_name)
else:
  actual_nc_path = wave_file

print(f"2. Reading NetCDF file: {actual_nc_path}...")
ds_waves = xr.open_dataset(actual_nc_path, engine="netcdf4")
df_waves = ds_waves.to_dataframe().reset_index()
df_waves = df_waves.dropna()

print("3. Loading existing atmospheric data (processed_climate_data.csv)...")
df_atmos = pd.read_csv("processed_climate_data.csv")

# Standardize timestamp types to prevent ValueError
df_atmos["valid_time"] = pd.to_datetime(df_atmos["valid_time"])
df_waves["valid_time"] = pd.to_datetime(df_waves["valid_time"])

print("4. Merging atmospheric and wave datasets on spatial coordinates...")
df_merged = pd.merge(
    df_atmos, df_waves, on=["valid_time", "latitude", "longitude"], how="inner"
)

# Remove duplicate or internal CDS metadata columns
cols_to_drop = [
    col
    for col in df_merged.columns
    if col.endswith("_y") or col in ["expver", "number"]
]
df_merged = df_merged.drop(columns=cols_to_drop, errors="ignore")

output_csv = "final_training_data.csv"
df_merged.to_csv(output_csv, index=False)

print("\n--- Merged Dataset Preview ---")
print(df_merged.head())
print(f"\nTotal aligned data points: {len(df_merged)}")
print(f"Saved merged dataset to: {output_csv}")