"""
Basic plotting functions for CHIRPS rainfall data.

Covers time series, monthly climatology, histograms, and scatter plots
using Matplotlib.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

from scripts import data_loading as dl


def plot_time_series(
    ds: xr.Dataset,
    lon: float,
    lat: float,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot a rainfall time series for a single grid point.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset with ``precip`` variable.
    lon : float
        Longitude of the point.
    lat : float
        Latitude of the point.
    ax : plt.Axes or None
        Axes to draw on.  A new figure+axes is created if *None*.
    **kwargs
        Forwarded to ``ax.plot``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    df = dl.extract_point(ds, lon, lat)

    if ax is None:
        fig, ax = plt.subplots(figsize=kwargs.pop("figsize", (12, 4)))
    else:
        fig = ax.figure

    default_kwargs = dict(color="steelblue", linewidth=0.8, alpha=0.9)
    default_kwargs.update(kwargs)

    ax.plot(df["time"], df["rainfall"], **default_kwargs)
    ax.set_xlabel("Date")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title(f"Daily Rainfall at ({lon:.2f}\u00b0, {lat:.2f}\u00b0)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig, ax


def plot_monthly_climatology(
    ds: xr.Dataset,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot the spatial-mean monthly rainfall climatology.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset with ``precip`` variable and a ``time`` dimension.
    ax : plt.Axes or None
        Axes to draw on.
    **kwargs
        Forwarded to ``ax.bar``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    monthly = (
        ds["precip"].groupby("time.month").mean(dim=["latitude", "longitude", "time"])
    )
    months = np.arange(1, 13)
    month_labels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.figure

    default_kwargs = dict(
        color="cornflowerblue",
        edgecolor="navy",
        alpha=0.85,
    )
    default_kwargs.update(kwargs)

    ax.bar(months, monthly.values, **default_kwargs)
    ax.set_xlabel("Month")
    ax.set_ylabel("Mean Rainfall (mm)")
    ax.set_title("Monthly Rainfall Climatology")
    ax.set_xticks(months)
    ax.set_xticklabels(month_labels)
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    return fig, ax


def plot_rainfall_histogram(
    ds: xr.Dataset,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot a histogram of rainfall values across all pixels and times.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset with ``precip`` variable.
    ax : plt.Axes or None
        Axes to draw on.
    **kwargs
        Forwarded to ``ax.hist``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    data = ds["precip"].values
    data = data[~np.isnan(data)]

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.figure

    default_kwargs = dict(
        bins=80,
        color="mediumseagreen",
        edgecolor="white",
        alpha=0.8,
        density=True,
    )
    default_kwargs.update(kwargs)

    ax.hist(data, **default_kwargs)
    ax.set_xlabel("Daily Rainfall (mm)")
    ax.set_ylabel("Probability Density")
    ax.set_title(f"Rainfall Distribution (n = {len(data):,})")
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    return fig, ax


def plot_scatter(
    x: np.ndarray | pd.Series,
    y: np.ndarray | pd.Series,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Create a scatter plot of two variables.

    Parameters
    ----------
    x, y : array-like
        Data to plot.
    ax : plt.Axes or None
        Axes to draw on.
    x_label : str, optional
        Label for the x-axis (default "X Variable").
    y_label : str, optional
        Label for the y-axis (default "Y Variable").
    **kwargs
        Forwarded to ``ax.scatter``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))
    else:
        fig = ax.figure

    x_label = kwargs.pop("x_label", "X Variable")
    y_label = kwargs.pop("y_label", "Y Variable")

    default_kwargs = dict(
        s=20,
        alpha=0.6,
        color="coral",
        edgecolor="black",
        linewidth=0.3,
    )
    default_kwargs.update(kwargs)

    ax.scatter(x, y, **default_kwargs)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title("Scatter Plot")
    ax.grid(True, alpha=0.3)
    ax.axline((0, 0), (1, 1), color="grey", linestyle="--", alpha=0.5, label="1:1")

    fig.tight_layout()
    return fig, ax


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Basic CHIRPS plotting")
    parser.add_argument("path", type=Path, help="Path to CHIRPS NetCDF")
    parser.add_argument(
        "--plot",
        choices=["timeseries", "climatology", "histogram", "scatter"],
        default="climatology",
    )
    parser.add_argument("--lon", type=float, default=38.5, help="Longitude")
    parser.add_argument("--lat", type=float, default=8.5, help="Latitude")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Save figure to file",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    ds = dl.load_chirps(args.path)

    plot_map = {
        "timeseries": lambda: plot_time_series(ds, args.lon, args.lat),
        "climatology": lambda: plot_monthly_climatology(ds),
        "histogram": lambda: plot_rainfall_histogram(ds),
        "scatter": lambda: plot_scatter(
            np.random.rand(200),
            np.random.rand(200),
        ),
    }

    fig, ax = plot_map[args.plot]()
    print(f"Generated '{args.plot}' plot")

    if args.output:
        fig.savefig(args.output, dpi=150, bbox_inches="tight")
        print(f"Saved to {args.output}")

    plt.show()
    ds.close()


if __name__ == "__main__":
    main()
