"""Prepare CHIRPS rainfall data subset for course exercises."""

import xarray as xr
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent
CHIRPS_PATH = DATA_DIR.parent / "chirps_1981_2022.nc"

def prepare_climatology():
    """Compute monthly climatology (1981-2010) and save."""
    print("Computing monthly climatology...")
    ds = xr.open_dataset(CHIRPS_PATH, engine="netcdf4")
    clim = ds.groupby("time.month").mean(dim="time")
    clim.to_netcdf(DATA_DIR / "chirps_climatology.nc")
    print(f"  Saved: {DATA_DIR / 'chirps_climatology.nc'}")

def prepare_annual_data():
    """Compute annual totals and save."""
    print("Computing annual totals...")
    ds = xr.open_dataset(CHIRPS_PATH, engine="netcdf4")
    annual = ds.resample(time="YE").sum(dim="time")
    annual.to_netcdf(DATA_DIR / "chirps_annual.nc")
    print(f"  Saved: {DATA_DIR / 'chirps_annual.nc'}")

def prepare_ethiopia_subset():
    """Extract Ethiopia bounding box subset."""
    print("Extracting Ethiopia subset...")
    ds = xr.open_dataset(CHIRPS_PATH, engine="netcdf4")
    eth = ds.sel(
        longitude=slice(33, 48),
        latitude=slice(3, 15)
    )
    eth.to_netcdf(DATA_DIR / "chirps_ethiopia.nc")
    print(f"  Saved: {DATA_DIR / 'chirps_ethiopia.nc'}")

def prepare_sample_point():
    """Extract time series at a sample point near Addis Ababa."""
    print("Extracting sample point time series...")
    ds = xr.open_dataset(CHIRPS_PATH, engine="netcdf4")
    point = ds.sel(
        longitude=38.75, latitude=9.03, method="nearest"
    )
    df = point.to_dataframe().reset_index()
    df.to_csv(DATA_DIR / "addis_ababa_rainfall.csv", index=False)
    print(f"  Saved: {DATA_DIR / 'addis_ababa_rainfall.csv'}")

def prepare_region_averages():
    """Compute regional averages for Ethiopian regions."""
    print("Computing regional averages...")
    regions = {
        "Tigray": {"lon": (36.5, 39.8), "lat": (12.5, 14.9)},
        "Amhara": {"lon": (36.5, 40.5), "lat": (9.5, 12.5)},
        "Oromia": {"lon": (34.5, 43.0), "lat": (3.5, 9.5)},
        "SNNPR": {"lon": (34.5, 39.5), "lat": (4.5, 8.0)},
        "Somali": {"lon": (41.0, 48.0), "lat": (3.5, 11.0)},
        "Afar": {"lon": (39.8, 42.5), "lat": (8.5, 14.5)},
        "Benishangul": {"lon": (34.0, 37.0), "lat": (8.5, 11.5)},
        "Gambela": {"lon": (33.0, 35.5), "lat": (7.0, 8.5)},
        "Harari": {"lon": (42.0, 42.5), "lat": (9.0, 9.5)},
        "Dire Dawa": {"lon": (42.0, 42.8), "lat": (8.5, 9.5)},
    }
    ds = xr.open_dataset(CHIRPS_PATH, engine="netcdf4")
    results = []
    for name, bbox in regions.items():
        subset = ds.sel(
            longitude=slice(bbox["lon"][0], bbox["lon"][1]),
            latitude=slice(bbox["lat"][0], bbox["lat"][1])
        )
        ts = subset.mean(dim=["longitude", "latitude"])
        df = ts.to_dataframe().reset_index()
        df["region"] = name
        results.append(df)
    combined = np.concatenate(results) if len(results) > 1 else results[0]
    import pandas as pd
    combined = pd.concat(results, ignore_index=True)
    combined.to_csv(DATA_DIR / "ethiopia_regional_rainfall.csv", index=False)
    print(f"  Saved: {DATA_DIR / 'ethiopia_regional_rainfall.csv'}")

def main():
    print("=" * 60)
    print("CHIRPS Data Preparation for Matplotlib Training")
    print("=" * 60)
    prepare_climatology()
    prepare_annual_data()
    prepare_ethiopia_subset()
    prepare_sample_point()
    prepare_region_averages()
    print("\nAll datasets prepared successfully!")

if __name__ == "__main__":
    main()
