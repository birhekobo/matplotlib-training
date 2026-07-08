"""
Data loading utilities for CHIRPS rainfall data.

Provides functions to load NetCDF files, subset regions, and extract
point time series for use throughout the Matplotlib Training Course.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import xarray as xr

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def load_chirps(path: str | Path) -> xr.Dataset:
    """Load a CHIRPS rainfall NetCDF file into an xarray Dataset.

    Parameters
    ----------
    path : str or Path
        Path to the NetCDF file.

    Returns
    -------
    xr.Dataset
        Dataset with at least a ``precip`` variable and ``time``,
        ``latitude``, ``longitude`` dimensions.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file lacks a ``precip`` variable.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"CHIRPS file not found: {path}")

    if not path.suffix.lower() in (".nc", ".netcdf"):
        logger.warning("File does not have a .nc extension: %s", path)

    ds = xr.open_dataset(path)
    logger.info("Loaded dataset: %s — shape %s", path.name, dict(ds.sizes))

    if "precip" not in ds.data_vars:
        found = list(ds.data_vars)
        ds.close()
        raise ValueError(
            f"Dataset at {path} does not contain a 'precip' variable. "
            f"Found: {found}"
        )

    return ds


def load_climatology(path: str | Path) -> xr.Dataset:
    """Load a CHIRPS climatology NetCDF file.

    Parameters
    ----------
    path : str or Path
        Path to the climatology NetCDF file.

    Returns
    -------
    xr.Dataset
        Dataset with monthly climatology values.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Climatology file not found: {path}")

    ds = xr.open_dataset(path)
    logger.info("Loaded climatology: %s", path.name)

    if "precip" not in ds.data_vars:
        found = list(ds.data_vars)
        ds.close()
        raise ValueError(
            f"Climatology at {path} lacks a 'precip' variable. " f"Found: {found}"
        )

    return ds


def load_region(
    ds: xr.Dataset, name: str, bbox: tuple[float, float, float, float]
) -> xr.Dataset:
    """Subset a dataset to a rectangular bounding box.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset with ``longitude`` and ``latitude`` coordinates.
    name : str
        Human-readable name for the region (used in logging).
    bbox : tuple of float
        (lon_min, lon_max, lat_min, lat_max).

    Returns
    -------
    xr.Dataset
        Subsetted dataset.
    """
    lon_min, lon_max, lat_min, lat_max = bbox

    if "longitude" in ds.dims and "latitude" in ds.dims:
        subset = ds.sel(
            longitude=slice(lon_min, lon_max),
            latitude=slice(lat_max, lat_min),
        )
    elif "lon" in ds.dims and "lat" in ds.dims:
        subset = ds.sel(
            lon=slice(lon_min, lon_max),
            lat=slice(lat_max, lat_min),
        )
    else:
        raise ValueError(
            "Dataset must have longitude/latitude or lon/lat dimensions. "
            f"Found dims: {list(ds.dims)}"
        )

    logger.info(
        "Subset '%s' — lon [%.2f, %.2f], lat [%.2f, %.2f] — shape %s",
        name,
        lon_min,
        lon_max,
        lat_min,
        lat_max,
        dict(subset.sizes),
    )
    return subset


def extract_point(
    ds: xr.Dataset, lon: float, lat: float, method: str = "nearest"
) -> pd.DataFrame:
    """Extract a time series at the grid cell nearest a given point.

    Parameters
    ----------
    ds : xr.Dataset
        Input dataset.
    lon : float
        Longitude of the point.
    lat : float
        Latitude of the point.
    method : str, optional
        Interpolation method passed to ``sel`` (default ``"nearest"``).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ``time`` and ``precip``.
    """
    if "longitude" in ds.dims:
        lon_dim, lat_dim = "longitude", "latitude"
    elif "lon" in ds.dims:
        lon_dim, lat_dim = "lon", "lat"
    else:
        raise ValueError(
            f"Cannot find longitude/latitude dimensions. Found: {list(ds.dims)}"
        )

    point = ds.sel(**{lon_dim: lon, lat_dim: lat}, method=method)

    df = point["precip"].to_dataframe().reset_index()
    df = df.rename(columns={"precip": "rainfall"})
    df = df.dropna(subset=["rainfall"])
    df = df.sort_values("time")

    logger.info(
        "Extracted point at (%.4f, %.4f) — %d records, " "range [%.2f, %.2f] mm",
        lon,
        lat,
        len(df),
        float(df["rainfall"].min()),
        float(df["rainfall"].max()),
    )
    return df


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CHIRPS data loading utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    info_parser = sub.add_parser("info", help="Print dataset summary")
    info_parser.add_argument("path", type=Path, help="Path to NetCDF file")

    region_parser = sub.add_parser("region", help="Subset a bounding box")
    region_parser.add_argument("path", type=Path)
    region_parser.add_argument("name", type=str)
    region_parser.add_argument(
        "bbox",
        type=float,
        nargs=4,
        metavar=("lon_min", "lon_max", "lat_min", "lat_max"),
    )
    region_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Save subset to NetCDF",
    )

    point_parser = sub.add_parser("point", help="Extract point time series")
    point_parser.add_argument("path", type=Path)
    point_parser.add_argument("lon", type=float)
    point_parser.add_argument("lat", type=float)
    point_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Save CSV to path",
    )

    return parser.parse_args()


def _cli_info(args: argparse.Namespace) -> None:
    ds = load_chirps(args.path)
    print(ds)
    print(f"\nVariable: precip")
    print(f"  Shape:   {ds['precip'].shape}")
    print(f"  Units:   {ds['precip'].attrs.get('units', 'N/A')}")
    print(f"  Time:    {str(ds['time'].values[0])} to " f"{str(ds['time'].values[-1])}")
    print(
        f"  Lon:     {float(ds['longitude'].values[0]):.2f} to "
        f"{float(ds['longitude'].values[-1]):.2f}"
    )
    print(
        f"  Lat:     {float(ds['latitude'].values[0]):.2f} to "
        f"{float(ds['latitude'].values[-1]):.2f}"
    )
    ds.close()


def _cli_region(args: argparse.Namespace) -> None:
    ds = load_chirps(args.path)
    subset = load_region(ds, args.name, args.bbox)
    print(subset)
    if args.output:
        subset.to_netcdf(args.output)
        print(f"Saved to {args.output}")
    ds.close()


def _cli_point(args: argparse.Namespace) -> None:
    ds = load_chirps(args.path)
    df = extract_point(ds, args.lon, args.lat)
    print(df.head(10))
    print(f"\nTotal records: {len(df)}")
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"Saved to {args.output}")
    ds.close()


def main() -> None:
    args = _parse_args()
    commands = {
        "info": _cli_info,
        "region": _cli_region,
        "point": _cli_point,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
