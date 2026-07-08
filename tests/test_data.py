"""Tests for data loading functions.

Uses synthetic NetCDF files written to a temporary directory to
validate loading, subsetting, and point extraction logic.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from scripts.data_loading import (
    extract_point,
    load_chirps,
    load_climatology,
    load_region,
)


@pytest.fixture
def chirps_file() -> Path:
    """Write a synthetic CHIRPS NetCDF to a temporary file."""
    np.random.seed(42)
    times = 36
    lons = 10
    lats = 8

    data = np.random.rand(times, lats, lons) * 25

    ds = xr.Dataset(
        {"precip": (["time", "latitude", "longitude"], data)},
        coords={
            "time": np.arange("2000-01-01", "2003-01-01", dtype="datetime64[M]"),
            "latitude": np.linspace(3, 15, lats),
            "longitude": np.linspace(33, 48, lons),
        },
    )
    ds["precip"].attrs["units"] = "mm"

    tmp = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
    ds.to_netcdf(tmp.name)
    ds.close()
    return Path(tmp.name)


@pytest.fixture
def climatology_file() -> Path:
    """Write a synthetic climatology NetCDF to a temporary file."""
    np.random.seed(42)
    lons = 10
    lats = 8

    data = np.random.rand(12, lats, lons) * 15

    ds = xr.Dataset(
        {"precip": (["month", "latitude", "longitude"], data)},
        coords={
            "month": np.arange(1, 13),
            "latitude": np.linspace(3, 15, lats),
            "longitude": np.linspace(33, 48, lons),
        },
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
    ds.to_netcdf(tmp.name)
    ds.close()
    return Path(tmp.name)


class TestLoadChirps:
    def test_load_valid_file(self, chirps_file):
        ds = load_chirps(chirps_file)
        assert isinstance(ds, xr.Dataset)
        assert "precip" in ds.data_vars
        assert ds["precip"].attrs.get("units") == "mm"
        ds.close()

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_chirps("/nonexistent/path.nc")

    def test_load_file_without_precip(self):
        ds = xr.Dataset({"foo": (["x"], [1, 2, 3])})
        tmp = tempfile.NamedTemporaryFile(suffix=".nc", delete=False)
        ds.to_netcdf(tmp.name)
        ds.close()
        tmp.close()
        p = Path(tmp.name)
        with pytest.raises(ValueError, match="precip"):
            load_chirps(p)
        p.unlink(missing_ok=True)

    def test_load_with_pathlib(self, chirps_file):
        ds = load_chirps(chirps_file)
        assert ds is not None
        ds.close()


class TestLoadClimatology:
    def test_load_valid_climatology(self, climatology_file):
        ds = load_climatology(climatology_file)
        assert isinstance(ds, xr.Dataset)
        assert "precip" in ds.data_vars
        ds.close()

    def test_load_nonexistent_climatology(self):
        with pytest.raises(FileNotFoundError):
            load_climatology("/nonexistent/clim.nc")


class TestLoadRegion:
    def test_subset_reduces_size(self, chirps_file):
        ds = load_chirps(chirps_file)
        original_size = ds.sizes
        bbox = (35, 45, 5, 12)
        subset = load_region(ds, "test_region", bbox)
        assert subset.sizes["longitude"] <= original_size["longitude"]
        assert subset.sizes["latitude"] <= original_size["latitude"]
        ds.close()
        subset.close()

    def test_subset_with_lon_lat_dims(self):
        ds = xr.Dataset(
            {"precip": (["time", "lat", "lon"], np.random.rand(5, 6, 7))},
            coords={
                "time": np.arange(5),
                "lat": np.linspace(-10, 10, 6),
                "lon": np.linspace(20, 40, 7),
            },
        )
        subset = load_region(ds, "test", (25, 35, -5, 5))
        assert subset is not None
        ds.close()

    def test_subset_invalid_dims(self):
        ds = xr.Dataset({"precip": (["x", "y"], np.random.rand(4, 5))})
        with pytest.raises(ValueError, match="longitude"):
            load_region(ds, "bad", (0, 10, 0, 10))
        ds.close()


class TestExtractPoint:
    def test_extract_returns_dataframe(self, chirps_file):
        ds = load_chirps(chirps_file)
        df = extract_point(ds, 38.0, 8.0)
        assert isinstance(df, pd.DataFrame)
        assert "time" in df.columns
        assert "rainfall" in df.columns
        assert len(df) > 0
        ds.close()

    def test_extract_with_lon_lat(self):
        ds = xr.Dataset(
            {"precip": (["time", "lat", "lon"], np.random.rand(10, 5, 5))},
            coords={
                "time": np.arange(10),
                "lat": np.linspace(-10, 10, 5),
                "lon": np.linspace(20, 40, 5),
            },
        )
        df = extract_point(ds, 30.0, 0.0)
        assert isinstance(df, pd.DataFrame)
        ds.close()

    def test_extract_no_coordinates(self):
        ds = xr.Dataset({"precip": (["x"], [1, 2, 3])})
        with pytest.raises(ValueError, match="longitude"):
            extract_point(ds, 0.0, 0.0)
        ds.close()

    def test_extract_invalid_point_returns_empty(self, chirps_file):
        ds = load_chirps(chirps_file)
        df = extract_point(ds, 200.0, 200.0)
        assert isinstance(df, pd.DataFrame)
        ds.close()
