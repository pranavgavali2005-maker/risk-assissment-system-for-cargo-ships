import pandas as pd

def clean_local_cyclone_data():
    filename = "ibtracs.NI.list.v04r01.csv"
    print(f"Loading local IBTrACS file: {filename}...")
    
    # Read the CSV, specifically skipping row 1 (the units row)
    try:
        df_cyclone = pd.read_csv(filename, skiprows=[1], low_memory=False)
    except FileNotFoundError:
        print(f"Error: Could not find {filename}. Ensure it is in the same folder.")
        return

    # Convert ISO_TIME to datetime format
    df_cyclone['ISO_TIME'] = pd.to_datetime(df_cyclone['ISO_TIME'])

    # Filter for 2021 onwards to match your Copernicus dataset
    df_cyclone = df_cyclone[df_cyclone['ISO_TIME'].dt.year >= 2021]

    # Keep only the essential columns required for the Risk Score
    columns_to_keep = ['SID', 'NAME', 'ISO_TIME', 'LAT', 'LON', 'WMO_WIND', 'NATURE']
    df_clean = df_cyclone[columns_to_keep].copy()

    # Clean up missing wind data (convert to numbers, fill missing with 0)
    df_clean['WMO_WIND'] = pd.to_numeric(df_clean['WMO_WIND'], errors='coerce').fillna(0)

    # Save the output
    output_name = "clean_cyclone_data.csv"
    df_clean.to_csv(output_name, index=False)
    
    print(f"\nSuccessfully filtered down to {len(df_clean)} recent cyclone records.")
    print(f"Saved cleanly as '{output_name}'.")
    print(df_clean.head())

if __name__ == "__main__":
    clean_local_cyclone_data()