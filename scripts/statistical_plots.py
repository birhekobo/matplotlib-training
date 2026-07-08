"""
Statistical visualization functions for CHIRPS rainfall data.

Includes box plots, violin plots, trend estimation with confidence
intervals, and correlation heatmaps.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xarray as xr
from scipy import stats as sp_stats

from scripts import data_loading as dl


def plot_boxplot_by_month(
    ds: xr.Dataset,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Draw a box plot of rainfall grouped by month.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset with ``precip`` variable.
    ax : plt.Axes or None
    **kwargs
        Forwarded to ``ax.boxplot``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    data = ds["precip"]
    months = data.time.dt.month.values

    monthly_groups = {m: [] for m in range(1, 13)}
    flat = data.values.reshape(len(data.time), -1)

    for i, m in enumerate(months):
        vals = flat[i][~np.isnan(flat[i])]
        monthly_groups[m].extend(vals.tolist())

    month_data = [monthly_groups[m] for m in range(1, 13)]
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
        fig, ax = plt.subplots(figsize=(12, 6))
    else:
        fig = ax.figure

    default_kwargs = dict(
        patch_artist=True,
        widths=0.6,
        medianprops=dict(color="red", linewidth=1.5),
    )
    default_kwargs.update(kwargs)

    bp = ax.boxplot(month_data, labels=month_labels, **default_kwargs)

    colors = plt.cm.viridis(np.linspace(0.2, 0.9, 12))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_xlabel("Month")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title("Monthly Rainfall Distribution (Box Plot)")
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    return fig, ax


def plot_violin_by_season(
    ds: xr.Dataset,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Draw a violin plot of rainfall grouped by season.

    Seasons: DJF (Dec-Feb), MAM (Mar-May), JJA (Jun-Aug), SON (Sep-Nov).

    Parameters
    ----------
    ds : xr.Dataset
    ax : plt.Axes or None
    **kwargs
        Forwarded to ``ax.violinplot``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    season_map = {
        "DJF": [12, 1, 2],
        "MAM": [3, 4, 5],
        "JJA": [6, 7, 8],
        "SON": [9, 10, 11],
    }

    months = ds["precip"].time.dt.month.values
    flat = ds["precip"].values.reshape(len(ds.time), -1)

    seasonal_data = {}
    for season, mlist in season_map.items():
        mask = np.isin(months, mlist)
        vals = flat[mask]
        seasonal_data[season] = vals[~np.isnan(vals)]

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        fig = ax.figure

    default_kwargs = dict(
        showmeans=True,
        showmedians=True,
        widths=0.7,
    )
    default_kwargs.update(kwargs)

    labels = list(seasonal_data.keys())
    vp = ax.violinplot(
        [seasonal_data[s] for s in labels],
        positions=[1, 2, 3, 4],
        **default_kwargs,
    )

    colors = ["#2c7bb6", "#d7191c", "#fdae61", "#abd9e9"]
    for i, body in enumerate(vp["bodies"]):
        body.set_facecolor(colors[i % len(colors)])
        body.set_alpha(0.7)

    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(labels)
    ax.set_xlabel("Season")
    ax.set_ylabel("Rainfall (mm)")
    ax.set_title("Seasonal Rainfall Distribution (Violin Plot)")
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    return fig, ax


def plot_trend_with_ci(
    ds: xr.Dataset,
    lon: float,
    lat: float,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot annual rainfall trend with confidence interval for a point.

    Aggregates daily rainfall to annual totals and fits a linear
    regression with 95 % confidence bands.

    Parameters
    ----------
    ds : xr.Dataset
    lon, lat : float
    ax : plt.Axes or None
    **kwargs
        Forwarded to ``ax.plot`` and ``ax.fill_between``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    df = dl.extract_point(ds, lon, lat)
    df["year"] = pd.to_datetime(df["time"]).dt.year
    annual = df.groupby("year")["rainfall"].sum().reset_index()

    years = annual["year"].values
    rainfall = annual["rainfall"].values

    slope, intercept, r_value, p_value, std_err = sp_stats.linregress(
        years,
        rainfall,
    )
    trend_line = slope * years + intercept

    n = len(years)
    y_pred = trend_line
    resid = rainfall - y_pred
    mse = np.sum(resid**2) / (n - 2)
    se_fit = np.sqrt(
        mse
        * (
            1 / n
            + (years - np.mean(years)) ** 2 / np.sum((years - np.mean(years)) ** 2)
        )
    )
    ci = sp_stats.t.ppf(0.975, n - 2) * se_fit

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))
    else:
        fig = ax.figure

    ax.fill_between(
        years,
        y_pred - ci,
        y_pred + ci,
        alpha=0.2,
        color=kwargs.get("ci_color", "steelblue"),
        label="95 % CI",
    )
    ax.plot(
        years,
        y_pred,
        **{
            "color": "crimson",
            "linewidth": 2,
            "label": (
                f"Trend: {slope:.1f} mm/yr "
                f"(p={p_value:.3f}, R\u00b2={r_value ** 2:.2f})"
            ),
            **kwargs,
        },
    )
    ax.scatter(
        years,
        rainfall,
        s=40,
        color="steelblue",
        edgecolor="black",
        linewidth=0.5,
        alpha=0.8,
        zorder=5,
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Annual Rainfall (mm)")
    ax.set_title(f"Annual Rainfall Trend at ({lon:.2f}\u00b0, " f"{lat:.2f}\u00b0)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    return fig, ax


def plot_heatmap_correlation(
    ds: xr.Dataset,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes]:
    """Plot a heatmap of the temporal correlation between grid cells.

    Downsamples to a regular grid to keep the matrix manageable.

    Parameters
    ----------
    ds : xr.Dataset
    ax : plt.Axes or None
    **kwargs
        Forwarded to ``sns.heatmap``.

    Returns
    -------
    tuple of (Figure, Axes)
    """
    step = kwargs.pop("step", 5)
    lon_slice = ds.longitude.values[::step]
    lat_slice = ds.latitude.values[::step]

    ds_sub = ds.sel(
        longitude=lon_slice,
        latitude=lat_slice,
    )

    n_lon = len(ds_sub.longitude)
    n_lat = len(ds_sub.latitude)
    n_cells = n_lon * n_lat

    time_dim = len(ds_sub.time)
    matrix_2d = ds_sub["precip"].values.reshape(time_dim, n_cells)
    matrix_2d = np.nan_to_num(matrix_2d, nan=0.0)

    corr = np.corrcoef(matrix_2d.T)

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8))
    else:
        fig = ax.figure

    sns.heatmap(
        corr,
        ax=ax,
        cmap=kwargs.get("cmap", "RdBu_r"),
        vmin=-1,
        vmax=1,
        square=True,
        xticklabels=False,
        yticklabels=False,
        cbar_kws={"label": "Pearson r"},
        **{k: v for k, v in kwargs.items() if k != "step"},
    )

    ax.set_title(f"Inter-Cell Rainfall Correlation (grid step = {step})")

    fig.tight_layout()
    return fig, ax


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Statistical CHIRPS plots")
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--plot",
        choices=["boxplot", "violin", "trend", "heatmap"],
        default="boxplot",
    )
    parser.add_argument("--lon", type=float, default=38.5)
    parser.add_argument("--lat", type=float, default=8.5)
    parser.add_argument("-o", "--output", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    ds = dl.load_chirps(args.path)

    plot_map = {
        "boxplot": lambda: plot_boxplot_by_month(ds),
        "violin": lambda: plot_violin_by_season(ds),
        "trend": lambda: plot_trend_with_ci(ds, args.lon, args.lat),
        "heatmap": lambda: plot_heatmap_correlation(ds),
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
