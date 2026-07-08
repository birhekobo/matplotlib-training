"""
Map-making functions for CHIRPS rainfall data using Cartopy.

Creates publication-quality spatial plots with coastlines, borders,
rivers, and colour bars.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.colors import Normalize

from scripts import data_loading as dl


def create_rainfall_map(
    ds: xr.Dataset,
    time_idx: int = 0,
    ax: Optional[plt.Axes] = None,
    projection: Optional[ccrs.Projection] = None,
    **kwargs,
) -> tuple[plt.Figure, plt.Axes, plt.cm.ScalarMappable]:
    """Plot a rainfall map for a single time step.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset with ``precip`` and ``time`` dimensions.
    time_idx : int
        Index along the time dimension to plot.
    ax : cartopy.mpl.geoaxes.GeoAxesSubplot or None
        GeoAxes to draw on.  A new one is created if *None*.
    projection : ccrs.Projection or None
        Map projection (default: PlateCarree).
    **kwargs
        Forwarded to ``ax.pcolormesh``.

    Returns
    -------
    tuple of (Figure, GeoAxesSubplot, QuadMesh)
    """
    if projection is None:
        projection = ccrs.PlateCarree(central_longitude=0)

    precip = ds["precip"]
    time_val = str(precip.time.values[time_idx])[:10]

    lon = precip.longitude.values
    lat = precip.latitude.values
    data = precip.isel(time=time_idx).values

    if ax is None:
        fig, ax = plt.subplots(
            figsize=kwargs.pop("figsize", (10, 8)),
            subplot_kw={"projection": projection},
        )
    else:
        fig = ax.figure

    norm = Normalize(
        vmin=kwargs.pop("vmin", 0),
        vmax=kwargs.pop("vmax", np.nanmax(data)),
    )
    cmap = kwargs.pop("cmap", "Blues")

    mesh = ax.pcolormesh(
        lon,
        lat,
        data,
        transform=ccrs.PlateCarree(),
        norm=norm,
        cmap=cmap,
        **kwargs,
    )

    ax.coastlines(linewidth=0.7, color="grey")
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.7)
    ax.add_feature(cfeature.OCEAN, facecolor="lightcyan", alpha=0.4)
    ax.add_feature(cfeature.LAKES, facecolor="lightcyan", alpha=0.4, edgecolor="grey")
    ax.add_feature(cfeature.RIVERS, linewidth=0.4, alpha=0.5)

    gl = ax.gridlines(
        draw_labels=True,
        linestyle="--",
        alpha=0.3,
        x_inline=False,
        y_inline=False,
    )
    gl.top_labels = False
    gl.right_labels = False

    ax.set_title(f"CHIRPS Rainfall — {time_val}")
    fig.tight_layout()

    return fig, ax, mesh


def create_ethiopia_basemap(
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """Create a base map of Ethiopia with geographical features.

    Parameters
    ----------
    ax : cartopy.mpl.geoaxes.GeoAxesSubplot or None
        GeoAxes to draw on.  A new one is created if *None*.
    **kwargs
        Forwarded to ``ax.set_extent`` (e.g. *extent*).

    Returns
    -------
    cartopy.mpl.geoaxes.GeoAxesSubplot
    """
    projection = ccrs.PlateCarree()
    extent = kwargs.pop("extent", (32, 48, 3, 15))

    if ax is None:
        fig, ax = plt.subplots(
            figsize=kwargs.pop("figsize", (8, 10)),
            subplot_kw={"projection": projection},
        )
    else:
        fig = ax.figure

    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.coastlines(linewidth=0.8, color="dimgrey")
    ax.add_feature(cfeature.BORDERS, linewidth=0.6, alpha=0.8)
    ax.add_feature(cfeature.OCEAN, facecolor="lightcyan", alpha=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.5, edgecolor="grey")
    ax.add_feature(cfeature.RIVERS, linewidth=0.4, alpha=0.6)
    ax.add_feature(cfeature.LAND, facecolor="linen", alpha=0.3)

    gl = ax.gridlines(
        draw_labels=True,
        linestyle="--",
        alpha=0.3,
        x_inline=False,
        y_inline=False,
    )
    gl.top_labels = False
    gl.right_labels = False

    ax.set_title("Ethiopia — Base Map")

    return ax


def add_colorbar(
    fig: plt.Figure,
    im: plt.cm.ScalarMappable,
    ax: Optional[plt.Axes] = None,
    label: Optional[str] = None,
    **kwargs,
) -> plt.colorbar.Colorbar:
    """Add a colorbar to a figure.

    Parameters
    ----------
    fig : plt.Figure
        The figure to add the colorbar to.
    im : ScalarMappable
        The mappable object (e.g. ``pcolormesh`` return value).
    ax : plt.Axes or None
        Axes to anchor the colorbar to (default: last active axes).
    label : str or None
        Colorbar label text.
    **kwargs
        Forwarded to ``fig.colorbar``.

    Returns
    -------
    matplotlib.colorbar.Colorbar
    """
    default_kwargs = dict(
        orientation="vertical",
        pad=0.05,
        shrink=0.85,
        aspect=25,
    )
    default_kwargs.update(kwargs)

    cbar = fig.colorbar(
        im,
        ax=ax,
        **default_kwargs,
    )
    cbar.set_label(
        label or "Rainfall (mm)",
        fontsize=kwargs.get("label_fontsize", 11),
    )

    return cbar


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CHIRPS map plotting")
    parser.add_argument("path", type=Path, help="CHIRPS NetCDF file")
    parser.add_argument("--time-idx", type=int, default=0)
    parser.add_argument("--vmax", type=float, default=None)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Save map to file",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    ds = dl.load_chirps(args.path)

    vmax = args.vmax or float(
        np.nanpercentile(ds["precip"].isel(time=args.time_idx).values, 98)
    )

    fig, ax, mesh = create_rainfall_map(
        ds,
        time_idx=args.time_idx,
        vmin=0,
        vmax=vmax,
    )
    add_colorbar(fig, mesh, ax=ax)

    if args.output:
        fig.savefig(args.output, dpi=200, bbox_inches="tight")
        print(f"Map saved to {args.output}")

    plt.show()
    ds.close()


if __name__ == "__main__":
    main()
