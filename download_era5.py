import cdsapi

c = cdsapi.Client()

print("Sending download request for Expanded Atmospheric Data...")

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'download_format': 'unarchived',  # Prevents the zip disguise!
        'variable': [
            '10m_u_component_of_wind',
            '10m_v_component_of_wind',
            'mean_sea_level_pressure',
            'sea_surface_temperature',
        ],
        'year': '2023',
        'month': '01',
        'day': '01',
        'time': '12:00',
        'area': [60.0, -100.0, -45.0, 160.0],  # Must match download_waves.py!
    },
    'download_sample.nc',
)

print('Atmospheric data download complete!')