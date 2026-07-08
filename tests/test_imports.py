"""Verify that all scripts and their dependencies import without error."""

from __future__ import annotations


def test_import_numpy() -> None:
    import numpy as np

    assert np is not None


def test_import_pandas() -> None:
    import pandas as pd

    assert pd is not None


def test_import_xarray() -> None:
    import xarray as xr

    assert xr is not None


def test_import_matplotlib() -> None:
    import matplotlib  # noqa: F401
    import matplotlib.pyplot as plt

    assert plt is not None


def test_import_cartopy() -> None:
    import cartopy  # noqa: F401
    import cartopy.crs as ccrs

    assert ccrs is not None


def test_import_seaborn() -> None:
    import seaborn as sns

    assert sns is not None


def test_import_scipy() -> None:
    import scipy  # noqa: F401
    from scipy import stats

    assert stats is not None


def test_import_data_loading() -> None:
    from scripts import data_loading as dl

    assert hasattr(dl, "load_chirps")
    assert hasattr(dl, "load_climatology")
    assert hasattr(dl, "load_region")
    assert hasattr(dl, "extract_point")


def test_import_basic_plots() -> None:
    from scripts import basic_plots as bp

    assert hasattr(bp, "plot_time_series")
    assert hasattr(bp, "plot_monthly_climatology")
    assert hasattr(bp, "plot_rainfall_histogram")
    assert hasattr(bp, "plot_scatter")


def test_import_maps() -> None:
    from scripts import maps  # noqa: F401

    assert hasattr(maps, "create_rainfall_map")
    assert hasattr(maps, "create_ethiopia_basemap")
    assert hasattr(maps, "add_colorbar")


def test_import_statistical_plots() -> None:
    from scripts import statistical_plots as sp

    assert hasattr(sp, "plot_boxplot_by_month")
    assert hasattr(sp, "plot_violin_by_season")
    assert hasattr(sp, "plot_trend_with_ci")
    assert hasattr(sp, "plot_heatmap_correlation")


def test_import_dashboard() -> None:
    from scripts import dashboard  # noqa: F401

    assert hasattr(dashboard, "create_rainfall_dashboard")
    assert hasattr(dashboard, "save_all_figures")
    assert hasattr(dashboard, "generate_report")
