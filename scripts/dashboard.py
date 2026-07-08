"""
Dashboard and reporting utilities for CHIRPS rainfall analysis.

Generates multi-panel summary figures, exports all plots, and
produces a Markdown report.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from scripts import data_loading as dl
from scripts.basic_plots import (
    plot_monthly_climatology,
    plot_rainfall_histogram,
    plot_time_series,
)
from scripts.maps import add_colorbar, create_rainfall_map
from scripts.statistical_plots import (
    plot_boxplot_by_month,
    plot_trend_with_ci,
)


def create_rainfall_dashboard(
    ds: xr.Dataset,
    output_dir: str | Path,
    lon: float = 38.5,
    lat: float = 8.5,
    time_idx: int = -1,
    dpi: int = 150,
    fmt: str = "png",
) -> dict[str, Path]:
    """Generate a multi-panel dashboard figure and save individual panels.

    The dashboard contains:
      - Rainfall map for a selected time step
      - Time series at a point
      - Monthly climatology
      - Box plot by month
      - Rainfall histogram
      - Annual trend with CI

    Parameters
    ----------
    ds : xr.Dataset
        CHIRPS dataset.
    output_dir : str or Path
        Directory to save figures.
    lon, lat : float
        Point location for time series and trend.
    time_idx : int
        Time index for the map panel.
    dpi : int
        Output resolution.
    fmt : str
        Image format (png, pdf, svg, etc.).

    Returns
    -------
    dict of str -> Path
        Mapping of panel names to file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(20, 14))
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

    # --- Map ---
    ax_map = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
    _, _, mesh = create_rainfall_map(
        ds,
        time_idx=time_idx,
        ax=ax_map,
        vmin=0,
        vmax=np.nanpercentile(ds["precip"].isel(time=time_idx).values, 98),
    )
    add_colorbar(fig, mesh, ax=ax_map, label="Rainfall (mm)")

    # --- Time series ---
    ax_ts = fig.add_subplot(gs[0, 1])
    plot_time_series(ds, lon, lat, ax=ax_ts)

    # --- Climatology ---
    ax_clim = fig.add_subplot(gs[0, 2])
    plot_monthly_climatology(ds, ax=ax_clim)

    # --- Box plot ---
    ax_box = fig.add_subplot(gs[1, 0])
    plot_boxplot_by_month(ds, ax=ax_box)

    # --- Histogram ---
    ax_hist = fig.add_subplot(gs[1, 1])
    plot_rainfall_histogram(ds, ax=ax_hist)

    # --- Trend ---
    ax_trend = fig.add_subplot(gs[1, 2])
    plot_trend_with_ci(ds, lon, lat, ax=ax_trend)

    # --- Summary text ---
    ax_text = fig.add_subplot(gs[2, :])
    ax_text.axis("off")
    summary = _build_summary_text(ds, lon, lat, time_idx)
    ax_text.text(
        0.5,
        0.5,
        summary,
        transform=ax_text.transAxes,
        ha="center",
        va="center",
        fontfamily="monospace",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=1", facecolor="whitesmoke"),
    )

    fig.suptitle(
        "CHIRPS Rainfall Analysis Dashboard",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    dashboard_path = output_dir / f"dashboard.{fmt}"
    fig.savefig(dashboard_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)

    paths = {"dashboard": dashboard_path}
    print(f"Dashboard saved: {dashboard_path}")
    return paths


def _build_summary_text(
    ds: xr.Dataset,
    lon: float,
    lat: float,
    time_idx: int,
) -> str:
    data = ds["precip"]
    total_precip = float(data.sum().values)
    mean_precip = float(data.mean().values)
    max_precip = float(data.max().values)
    time_range = f"{str(data.time.values[0])[:10]} to {str(data.time.values[-1])[:10]}"
    map_time = str(data.time.values[time_idx])[:10]

    lines = [
        f"Dataset: CHIRPS Daily Rainfall",
        f"Period:  {time_range}",
        f"Shape:   {dict(data.sizes)}",
        f"Map at:  {map_time}",
        f"Point:   ({lon:.2f}, {lat:.2f})",
        f"",
        f"Mean rainfall:  {mean_precip:.1f} mm",
        f"Max rainfall:   {max_precip:.1f} mm",
        f"Total rainfall: {total_precip:.1f} mm",
    ]
    return "\n".join(lines)


def save_all_figures(
    figures: dict[str, plt.Figure],
    output_dir: str | Path,
    dpi: int = 300,
    fmt: str = "png",
) -> dict[str, Path]:
    """Save a dictionary of named figures to a directory.

    Parameters
    ----------
    figures : dict of str -> Figure
        Figures to save.
    output_dir : str or Path
        Output directory.
    dpi : int
        Resolution.
    fmt : str
        Image format.

    Returns
    -------
    dict of str -> Path
        Mapping of names to saved file paths.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    saved = {}
    for name, fig in figures.items():
        path = output_dir / f"{name}.{fmt}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        saved[name] = path
        print(f"Saved: {path}")

    return saved


def generate_report(
    data: dict,
    figures: dict[str, Path],
    output_path: str | Path,
) -> str:
    """Generate a Markdown report summarising the analysis.

    Parameters
    ----------
    data : dict
        Arbitrary metadata key-value pairs (e.g. mean, max, total).
    figures : dict of str -> Path
        Figure paths relative to the report.
    output_path : str or Path
        Path to write the Markdown file.

    Returns
    -------
    str
        The rendered Markdown text.
    """
    output_path = Path(output_path)

    lines = [
        "# CHIRPS Rainfall Analysis Report",
        "",
        "## Summary Statistics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
    ]
    for key, value in data.items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "## Figures", ""])
    for name, path in figures.items():
        rel = path.resolve()
        lines.append(f"### {name.replace('_', ' ').title()}")
        lines.append("")
        lines.append(f"![]({rel})")
        lines.append("")

    text = "\n".join(lines)
    output_path.write_text(text, encoding="utf-8")
    print(f"Report written to {output_path}")
    return text


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CHIRPS dashboard and report")
    parser.add_argument("path", type=Path, help="CHIRPS NetCDF")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("_dashboard"),
    )
    parser.add_argument("--lon", type=float, default=38.5)
    parser.add_argument("--lat", type=float, default=8.5)
    parser.add_argument("--time-idx", type=int, default=-1)
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--fmt", default="png")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    ds = dl.load_chirps(args.path)
    paths = create_rainfall_dashboard(
        ds,
        output_dir=args.output_dir,
        lon=args.lon,
        lat=args.lat,
        time_idx=args.time_idx,
        dpi=args.dpi,
        fmt=args.fmt,
    )

    data = {
        "mean_rainfall_mm": f"{float(ds['precip'].mean().values):.2f}",
        "max_rainfall_mm": f"{float(ds['precip'].max().values):.2f}",
        "total_rainfall_mm": f"{float(ds['precip'].sum().values):.2f}",
    }
    report_path = args.output_dir / "report.md"
    generate_report(data, paths, report_path)

    ds.close()


if __name__ == "__main__":
    main()
