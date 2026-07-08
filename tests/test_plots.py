"""Tests for basic plotting functions.

Verifies that plotting functions return the expected figure/axes
tuples and can render without error.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for testing

import matplotlib.pyplot as plt
import numpy as np
import pytest
import xarray as xr

from scripts.basic_plots import (
    plot_monthly_climatology,
    plot_rainfall_histogram,
    plot_scatter,
    plot_time_series,
)
from scripts.maps import add_colorbar, create_ethiopia_basemap, create_rainfall_map


@pytest.fixture
def dummy_dataset() -> xr.Dataset:
    """Create a small synthetic CHIRPS-like dataset for testing."""
    np.random.seed(42)
    times = 24
    lons = 5
    lats = 4
    data = np.random.rand(times, lats, lons) * 20

    ds = xr.Dataset(
        {"precip": (["time", "latitude", "longitude"], data)},
        coords={
            "time": np.arange("2000-01-01", "2002-01-01", dtype="datetime64[M]"),
            "latitude": np.linspace(8, 12, lats),
            "longitude": np.linspace(36, 40, lons),
        },
    )
    return ds


@pytest.fixture
def dummy_point_data() -> xr.Dataset:
    """Single-point time series dataset."""
    np.random.seed(42)
    times = 100
    ds = xr.Dataset(
        {
            "precip": (
                ["time", "latitude", "longitude"],
                np.random.rand(times, 1, 1) * 15,
            )
        },
        coords={
            "time": np.arange("2000-01-01", "2000-04-10", dtype="datetime64[D]"),
            "latitude": [9.0],
            "longitude": [38.0],
        },
    )
    return ds


class TestBasicPlots:
    def test_plot_time_series_returns_fig_ax(self, dummy_point_data):
        fig, ax = plot_time_series(dummy_point_data, lon=38.0, lat=9.0)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_plot_time_series_with_existing_axes(self, dummy_point_data):
        _, ax = plt.subplots()
        fig, ax_out = plot_time_series(dummy_point_data, lon=38.0, lat=9.0, ax=ax)
        assert ax_out is ax
        plt.close(fig)

    def test_plot_monthly_climatology_returns_fig_ax(self, dummy_dataset):
        fig, ax = plot_monthly_climatology(dummy_dataset)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_plot_rainfall_histogram_returns_fig_ax(self, dummy_dataset):
        fig, ax = plot_rainfall_histogram(dummy_dataset)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_plot_scatter_returns_fig_ax(self):
        x = np.random.rand(50)
        y = np.random.rand(50)
        fig, ax = plot_scatter(x, y)
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_plot_scatter_with_existing_axes(self):
        _, ax = plt.subplots()
        x = np.random.rand(20)
        y = np.random.rand(20)
        fig, ax_out = plot_scatter(x, y, ax=ax)
        assert ax_out is ax
        plt.close(fig)


class TestMaps:
    def test_create_rainfall_map_returns_fig_ax_mesh(self, dummy_dataset):
        result = create_rainfall_map(dummy_dataset, time_idx=0)
        assert len(result) == 3
        fig, ax, mesh = result
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_create_ethiopia_basemap_returns_geoaxes(self, dummy_dataset):
        ax = create_ethiopia_basemap()
        assert isinstance(ax, plt.Axes)
        plt.close(ax.figure)

    def test_add_colorbar(self, dummy_dataset):
        fig, ax, mesh = create_rainfall_map(dummy_dataset, time_idx=0)
        cbar = add_colorbar(fig, mesh, ax=ax, label="mm")
        import matplotlib.colorbar

        assert isinstance(cbar, matplotlib.colorbar.Colorbar)
        plt.close(fig)
