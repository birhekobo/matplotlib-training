#import "../macros.typ": note-box, warning-box, info-box
= Capstone Project: Rainfall Visualization Dashboard

The capstone project brings together all the skills from this course to create a comprehensive rainfall visualization dashboard using the CHIRPS dataset.

== Project Overview

Create a publication-quality, multi-panel dashboard that visualizes satellite-derived precipitation data. The final product should be suitable for inclusion in a climate report, research paper, or professional presentation.

== Learning Objectives

- Process real-world climate data (NetCDF format)
- Design a complex multi-panel figure layout
- Apply Cartopy for geographic visualization
- Create publication-ready output with proper formatting
- Demonstrate understanding of color theory and accessibility
- Write clean, reusable, documented code

== Dataset

You will use the Climate Hazards Group InfraRed Precipitation with Station Data (CHIRPS), a quasi-global rainfall dataset available from 1981 to the present.

=== Data Access

Sample data files are provided in the `datasets/` directory:

```python
import xarray as xr

# Load the CHIRPS dataset
ds = xr.open_dataset('datasets/chirps_ethiopia.nc')
```

=== Dataset Structure

```python
print(ds_daily)
"""
Dimensions:    (lat: 2000, lon: 7200, time: 1)
Coordinates:
  * lat        (lat) float32 -49.975 49.925 ... 49.975
  * lon        (lon) float32 -179.975 -179.875 ... 179.975
  * time       (time) datetime64[ns] 2024-01-01
Data variables:
    precip     (time, lat, lon) float32 ...
"""
```

== Dashboard Requirements

=== Panel Layout

Create a 2×2 dashboard with the following panels:

*Panel 1 (Top-Left): Global Precipitation Map*
- Robinson projection
- Full global extent
- CHIRPS precipitation as a color overlay
- Coastlines and country borders
- Gridlines with labels

*Panel 2 (Top-Right): Regional Zoom*
- Focus on East Africa (20°E–55°E, 15°S–25°N)
- PlateCarree projection
- High-resolution features (lakes, rivers)
- City markers for key locations

*Panel 3 (Bottom-Left): Time Series*
- Regional mean precipitation over time
- Rolling 30-day mean overlay
- Shaded ±1σ confidence interval
- Proper date formatting

*Panel 4 (Bottom-Right): Distribution Analysis*
- Log-transformed histogram of precipitation values
- Density curve overlay
- Statistics box (N, mean, median, std)
- Proper bin selection

=== Technical Specifications

| *Parameter* | *Requirement* |
|---|---|
| Figure size | 16 × 12 inches |
| Output format | PNG (300 DPI) + PDF |
| Font family | Serif (Times New Roman or similar) |
| Font size | 8-10 pt for labels, 10-12 pt for titles |
| Color palette | Perceptually uniform, colorblind-friendly |
| DPI | 300 for print output |
| Coordinate system | WGS84 (EPSG:4326) |

=== Non-Functional Requirements

- Code must be reusable (functions for each panel)
- All parameters should be configurable (date, region, colors)
- Script must run end-to-end without errors
- Comments explaining design decisions

== Design Considerations

=== Color Palette

```python
# Recommended: perceptually uniform and colorblind-friendly
PRECIP_CMAP = plt.cm.Blues  # Sequential for precipitation
ANOMALY_CMAP = plt.cm.RdBu  # Diverging for anomalies

# Or use a custom diverging palette
EAST_AFRICA_COLORS = ['#313695', '#4575b4', '#74add1', '#abd9e9',
                       '#fee090', '#fdae61', '#f46d43', '#d73027']
```

=== Figure Layout

Use `GridSpec` for precise control:

```python
gs = fig.add_gridspec(2, 2, hspace=0.15, wspace=0.15,
                      width_ratios=[1, 1], height_ratios=[1, 1])
```

=== Panel Labeling

```python
for label, ax in zip(['(a)', '(b)', '(c)', '(d)'], axes_flat):
    ax.text(0.02, 0.98, label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='top',
            bbox=dict(boxstyle='square', facecolor='white', alpha=0.8))
```

=== Shared Colorbar

```python
cbar_ax = fig.add_axes([0.25, 0.52, 0.5, 0.02])
cbar = fig.colorbar(pcm, cax=cbar_ax, orientation='horizontal',
                    label='Precipitation (mm/day)')
```

== Implementation Plan

=== Step 1: Data Loading and Preprocessing

```python
def load_chirps_data(filepath):
    """Load and preprocess CHIRPS data."""
    ds = xr.open_dataset(filepath)
    precip = ds['precip'].squeeze()
    precip = precip.where(precip >= 0)  # Mask fill values
    return precip, ds.lon, ds.lat
```

=== Step 2: Create Figure Layout

```python
def create_dashboard_layout():
    """Create the 2×2 figure layout with appropriate projections."""
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(2, 2, hspace=0.2, wspace=0.15)
    
    ax_global = fig.add_subplot(gs[0, 0], projection=ccrs.Robinson())
    ax_regional = fig.add_subplot(gs[0, 1],
        projection=ccrs.PlateCarree(central_longitude=35))
    ax_ts = fig.add_subplot(gs[1, 0])
    ax_hist = fig.add_subplot(gs[1, 1])
    
    return fig, (ax_global, ax_regional, ax_ts, ax_hist)
```

=== Step 3: Global Map Panel

```python
def plot_global_map(ax, lon, lat, precip, cmap='Blues'):
    """Plot global precipitation map."""
    pcm = ax.pcolormesh(lon, lat, precip, transform=ccrs.PlateCarree(),
                        cmap=cmap, shading='auto')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)
    ax.set_global()
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
    gl.top_labels = False
    gl.right_labels = False
    ax.set_title('(a) Global Precipitation', fontsize=12, fontweight='bold')
    return pcm
```

=== Step 4: Regional Zoom Panel

```python
def plot_regional_map(ax, lon, lat, precip, extent, cmap='Blues'):
    """Plot regional precipitation map."""
    ax.set_extent(extent)
    pcm = ax.pcolormesh(lon, lat, precip, transform=ccrs.PlateCarree(),
                        cmap=cmap, shading='auto')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.7)
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS, alpha=0.3)
    gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
    gl.top_labels = False
    gl.right_labels = False
    ax.set_title('(b) East Africa Zoom', fontsize=12, fontweight='bold')
    return pcm
```

=== Step 5: Time Series Panel

```python
def plot_timeseries(ax, precip, lon_range, lat_range):
    """Plot regional mean time series."""
    region = precip.sel(lon=slice(*lon_range), lat=slice(*lat_range))
    regional_mean = region.mean(dim=['lat', 'lon'])
    
    ax.plot(regional_mean, color='#1f77b4', linewidth=1.5, label='Daily')
    
    rolling_mean = regional_mean.rolling(time=30).mean()
    rolling_std = regional_mean.rolling(time=30).std()
    
    ax.plot(rolling_mean, color='#d62728', linewidth=2, label='30-day mean')
    ax.fill_between(rolling_mean.time.values,
                    rolling_mean - rolling_std,
                    rolling_mean + rolling_std,
                    alpha=0.2, color='#d62728')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Precipitation (mm/day)')
    ax.set_title('(c) East Africa Mean Precipitation')
    ax.legend()
    ax.grid(alpha=0.3)
```

=== Step 6: Histogram Panel

```python
def plot_histogram(ax, precip):
    """Plot precipitation distribution."""
    data = precip.values.flatten()
    data = data[~np.isnan(data)]
    data = data[data > 0]
    
    log_data = np.log10(data)
    ax.hist(log_data, bins=60, density=True, alpha=0.7,
            color='steelblue', edgecolor='white')
    
    # Statistics box
    stats_text = (f'N = {len(data):,}\n'
                  f'Mean = {np.mean(data):.2f} mm/day\n'
                  f'Median = {np.median(data):.2f} mm/day\n'
                  f'Std = {np.std(data):.2f} mm/day')
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
            fontsize=9, va='top', ha='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax.set_xlabel('log₁₀(Precipitation) (mm/day)')
    ax.set_ylabel('Density')
    ax.set_title('(d) Precipitation Distribution')
    ax.grid(alpha=0.3, axis='y')
```

== Evaluation Criteria

| *Category* | *Maximum Points* | *Criteria* |
|---|---|---|
| Data processing | 15 | Correct loading, cleaning, subsetting |
| Layout design | 15 | Proper grid, projections, spacing |
| Map panels | 20 | Geographic features, color mapping, labels |
| Time series | 15 | Correct aggregation, rolling stats, formatting |
| Histogram | 10 | Appropriate bins, transformation, statistics |
| Colorbar & labels | 10 | Shared colorbar, clear labels, panel labels |
| Code quality | 10 | Functions, documentation, configurability |
| Output quality | 5 | 300 DPI, correct size, PDF + PNG |
| *Total* | *100* | |

== Submission Requirements

Submit the following files:

1. `rainfall_dashboard.py` — Complete Python script
2. `rainfall_dashboard.png` — Output figure at 300 DPI
3. `rainfall_dashboard.pdf` — Output figure as vector PDF
4. `README.md` — Brief documentation (1-2 paragraphs)

== Suggested Extensions

For additional challenge:

- Add a date selector to change the displayed month
- Include El Niño / La Niña year comparison
- Add animation of monthly data through the year
- Include elevation data overlay (e.g., SRTM)
- Create an interactive version with ipywidgets

== Final Words

Congratulations on reaching the capstone project. This project is designed to showcase everything you have learned and produce a professional, portfolio-ready visualization. Take your time, iterate on the design, and produce something you are proud to show.



