import cdsapi

c = cdsapi.Client()

print("Sending download request for Ocean Wave Data...")

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'download_format': 'unarchived',  # Prevents the zip disguise!
        'variable': [
            'significant_height_of_combined_wind_waves_and_swell',
        ],
        'year': '2023',
        'month': '01',
        'day': '01',
        'time': '12:00',
        'area': [60.0, -100.0, -45.0, 160.0],  # Expanded Maritime Corridor
    },
    'download_waves.nc',
)

print('Wave data download complete!')