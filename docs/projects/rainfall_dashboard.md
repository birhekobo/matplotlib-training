---
title: Rainfall Dashboard Project
---

# Rainfall Dashboard Project

Create a comprehensive rainfall visualization dashboard using the CHIRPS dataset.

---

## Objective

Build a multi-panel dashboard that visualizes satellite-derived precipitation data from the CHIRPS dataset. The final product should be a publication-quality figure suitable for inclusion in a climate report or research presentation.

---

## Requirements

### Technical Requirements

| Requirement | Specification |
|-------------|---------------|
| Python version | 3.11+ |
| Core libraries | matplotlib, numpy, xarray, cartopy |
| Data format | NetCDF (CHIRPS) |
| Output format | PNG (300 DPI) + PDF |
| Figure size | 16×12 inches |

### Functional Requirements

1. Load and process CHIRPS NetCDF data using xarray
2. Create a 2×2 dashboard layout with:
   - **Top-left**: Global precipitation map (Robinson projection)
   - **Top-right**: Regional zoom (e.g., East Africa, PlateCarree)
   - **Bottom-left**: Time series of zonal mean precipitation
   - **Bottom-right**: Precipitation anomaly histogram
3. Consistent color palette across all panels
4. Professional labels, titles, and colorbars
5. Gridlines and geographic features on maps

---

## CHIRPS Data Access

Sample data is provided in the `datasets/` directory. To download fresh data:

```python
import urllib.request
import xarray as xr

# Download daily CHIRPS data
url = (
    "https://data.chc.ucsb.edu/products/CHIRPS-2.0/"
    "global_daily/netcdf/p05/"
    "chirps-v2.0.2024.01.01.nc"
)
urllib.request.urlretrieve(url, "chirps-v2.0.2024.01.01.nc")

# Open with xarray
ds = xr.open_dataset("chirps-v2.0.2024.01.01.nc")
print(ds)
```

---

## Step-by-Step Instructions

### Step 1: Load and Explore the Data

```python
import xarray as xr
import numpy as np

ds = xr.open_dataset('../datasets/chirps_ethiopia.nc')
precip = ds['precip'].squeeze()  # Remove time dimension

# Basic statistics
print(f"Shape: {precip.shape}")
print(f"Min: {precip.min().values:.2f}, Max: {precip.max().values:.2f}")
print(f"Mean: {precip.mean().values:.2f}, Std: {precip.std().values:.2f}")

# Handle NaNs (CHIRPS uses -9999 for missing)
precip = precip.where(precip >= 0)
```

### Step 2: Create the Dashboard Layout

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig = plt.figure(figsize=(16, 12))

# Define grid: 2 rows, 2 columns
# Using GridSpec for precise control
gs = fig.add_gridspec(2, 2, hspace=0.15, wspace=0.15,
                      width_ratios=[1, 1], height_ratios=[1, 1])

# Create axes with different projections
ax_global = fig.add_subplot(gs[0, 0], projection=ccrs.Robinson())
ax_regional = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree(
    central_longitude=35))
ax_timeseries = fig.add_subplot(gs[1, 0])
ax_hist = fig.add_subplot(gs[1, 1])
```

### Step 3: Global Precipitation Map (Top-Left)

```python
ax = ax_global
ax.set_global()

# Plot precipitation
pcm = ax.pcolormesh(ds.lon, ds.lat, precip, transform=ccrs.PlateCarree(),
                    cmap='Blues', shading='auto')

# Features
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)
ax.add_feature(cfeature.OCEAN, color='lightgray', alpha=0.3)

ax.set_title('Global Precipitation', fontsize=12, fontweight='bold')
gl = ax.gridlines(linestyle='--', alpha=0.3, draw_labels=True)
gl.top_labels = False
gl.right_labels = False
```

### Step 4: Regional Zoom (Top-Right)

```python
ax = ax_regional
ax.set_extent([20, 55, -15, 25])  # East Africa

pcm_reg = ax.pcolormesh(ds.lon, ds.lat, precip, transform=ccrs.PlateCarree(),
                        cmap='Blues', shading='auto')
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.7)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS, alpha=0.3)

ax.set_title('East Africa Precipitation', fontsize=12, fontweight='bold')
gl = ax.gridlines(linestyle='--', alpha=0.3, draw_labels=True)
gl.top_labels = False
gl.right_labels = False
```

### Step 5: Time Series (Bottom-Left)

```python
ax = ax_timeseries

# Compute zonal mean (average over longitude)
zonal_mean = precip.mean(dim='lon')
# Average over latitude bands (e.g., tropics 23.5°S–23.5°N)
lat_mask = (ds.lat >= -23.5) & (ds.lat <= 23.5)
tropical_precip = precip.where(lat_mask).mean(dim=['lat', 'lon'])

# For multi-day data, compute daily means
# (Using synthetic time series for demo)
days = np.arange(1, 32)
daily_means = np.random.gamma(2, 3, 31)  # Replace with real multi-day data

ax.plot(days, daily_means, color='#1f77b4', linewidth=2, marker='o')
ax.fill_between(days, daily_means, alpha=0.2, color='#1f77b4')
ax.set_xlabel('Day')
ax.set_ylabel('Mean Precipitation (mm/day)')
ax.set_title('Daily Precipitation — January 2024')
ax.grid(alpha=0.3, axis='y')
```

### Step 6: Anomaly Histogram (Bottom-Right)

```python
ax = ax_hist

# Flatten precipitation values and remove NaNs
precip_flat = precip.values.flatten()
precip_flat = precip_flat[~np.isnan(precip_flat)]
precip_flat = precip_flat[precip_flat > 0]  # Rainy pixels only

# Log transform for better visualization
log_precip = np.log10(precip_flat)

ax.hist(log_precip, bins=50, color='steelblue', edgecolor='white',
        alpha=0.8, density=True)
ax.set_xlabel('log₁₀(Precipitation) (mm/day)')
ax.set_ylabel('Density')
ax.set_title('Precipitation Distribution')
ax.grid(alpha=0.3, axis='y')

# Add statistics as text
stats_text = (
    f"N = {len(precip_flat):,}\n"
    f"Mean = {np.mean(precip_flat):.2f} mm/day\n"
    f"Median = {np.median(precip_flat):.2f} mm/day\n"
    f"Std = {np.std(precip_flat):.2f} mm/day"
)
ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
        fontsize=9, verticalalignment='top', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
```

### Step 7: Colorbar and Final Touches

```python
# Shared colorbar for map panels
cbar_ax = fig.add_axes([0.25, 0.52, 0.5, 0.02])
cbar = fig.colorbar(pcm, cax=cbar_ax, orientation='horizontal',
                    label='Precipitation (mm/day)')

# Main title
fig.suptitle('CHIRPS Rainfall Dashboard — January 2024',
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig('rainfall_dashboard.png', dpi=300, bbox_inches='tight')
plt.savefig('rainfall_dashboard.pdf', bbox_inches='tight')
plt.show()
```

---

## Expected Output

The final dashboard should look like this schematic:

```
+----------------------------------+----------------------------------+
|        GLOBAL PRECIP             |      EAST AFRICA ZOOM            |
|    [Robinson projection]         |    [PlateCarree projection]      |
|    World map with precip         |    Regional detail with          |
|    color overlay                 |    lakes and rivers              |
+----------------------------------+----------------------------------+
|        TIME SERIES               |      DISTRIBUTION                |
|    Daily mean precipitation      |    Log-transformed histogram     |
|    Line + fill under curve       |    Statistics box                |
+----------------------------------+----------------------------------+
          [Shared colorbar at top of bottom panels]
```

---

## Evaluation Criteria

| Criterion | Points | Description |
|-----------|--------|-------------|
| Data loading | 10 | Correctly loads and processes CHIRPS NetCDF |
| Layout | 15 | Proper 2×2 grid with appropriate projections |
| Map panels | 25 | Geographic features, color mapping, gridlines |
| Time series | 15 | Correct zonal mean, labeled axes, fill |
| Histogram | 15 | Appropriate transformation, statistics, styling |
| Colorbar | 10 | Shared colorbar with proper label |
| Publication quality | 10 | 300 DPI, proper fonts, layout, PDF output |
| **Total** | **100** | |

---

## Submission

Submit your dashboard as:

1. `rainfall_dashboard.py` — The complete Python script
2. `rainfall_dashboard.png` — The output figure (300 DPI)
3. A brief report (paragraph or bullet points) explaining your design choices
