---
title: Week 4 Solutions
---

# Week 4 Solutions

---

## Solution 4.1: Pandas Built-in Plotting

```python
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ts_df['precip'].plot(ax=axes[0,0], title='Time Series', linewidth=0.5)
ts_df.groupby(ts_df.index.month)['precip'].mean().plot(
    ax=axes[0,1], kind='bar', title='Monthly Climatology')
ts_df['precip'].plot(ax=axes[1,0], kind='hist', bins=40,
                      title='Distribution', edgecolor='white')

precip = ts_df['precip'].values
ax = axes[1,1]
ax.scatter(precip[:-1], precip[1:], alpha=0.3, s=5)
ax.set_title('Lag-1 Scatter')
ax.set_xlabel('t (mm)')
ax.set_ylabel('t+1 (mm)')

plt.tight_layout()
plt.show()
```

---

## Solution 4.2: Custom Rain Gauge Artist

```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(4, 8))
ax.set_xlim(0, 1)
ax.set_ylim(0, 300)
ax.set_aspect('equal')

gauge = FancyBboxPatch((0.3, 0), 0.4, 250,
                        boxstyle="round,pad=0.02",
                        facecolor='lightblue', edgecolor='navy', linewidth=2)
ax.add_patch(gauge)

water = FancyBboxPatch((0.3, 0), 0.4, 150,
                        boxstyle="round,pad=0.02",
                        facecolor='steelblue', alpha=0.7, edgecolor='none')
ax.add_patch(water)

for val in range(0, 251, 50):
    ax.axhline(val, xmin=0.25, xmax=0.35, color='navy', linewidth=0.8)
    ax.text(0.2, val, str(val), ha='right', va='center', fontsize=9)

ax.set_title('Rain Gauge\n150 mm / 250 mm')
ax.axis('off')
plt.show()
```

---

## Solution 4.3: Publication Figure

```python
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd

plt.rcParams.update({
    'figure.dpi': 300,
    'font.family': 'serif',
    'font.size': 9,
    'axes.linewidth': 0.8,
})

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly = ts_df.groupby(ts_df.index.month)['precip'].mean()
months = ['J','F','M','A','M','J','J','A','S','O','N','D']

fig, axes = plt.subplots(2, 2, figsize=(7.5, 6))

axes[0,0].plot(ts_df.index, ts_df['precip'], linewidth=0.3, color='#1f77b4')
axes[0,0].set_title('(a) Time Series', fontweight='bold')
axes[0,0].set_ylabel('mm/month')

axes[0,1].bar(months, monthly, color='#1f77b4', width=0.7)
axes[0,1].set_title('(b) Climatology', fontweight='bold')

axes[1,0].hist(ts_df['precip'], bins=40, color='#2ca02c', edgecolor='white')
axes[1,0].set_title('(c) Distribution', fontweight='bold')
axes[1,0].set_xlabel('mm/month')

precip_vals = ts_df['precip'].values
axes[1,1].scatter(precip_vals[:-1], precip_vals[1:], s=2, alpha=0.3, color='#d62728')
axes[1,1].plot([0, 400], [0, 400], 'k--', linewidth=0.5)
axes[1,1].set_title('(d) Lag-1 Correlation', fontweight='bold')
axes[1,1].set_xlabel('t (mm)')
axes[1,1].set_ylabel('t+1 (mm)')
axes[1,1].set_aspect('equal')

plt.tight_layout()
fig.savefig('publication_figure.pdf', bbox_inches='tight')
plt.show()
```

---

## Solution 4.4: Complete Dashboard

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import xarray as xr
import numpy as np
import pandas as pd

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

fig = plt.figure(figsize=(18, 12))
gs = gridspec.GridSpec(2, 3, figure=fig)

ax_map = fig.add_subplot(gs[0, 0])
im = ax_map.pcolormesh(ds.longitude, ds.latitude, ds.precip.isel(time=0),
                        cmap='Blues', shading='auto')
ax_map.set_title('Rainfall Map')
plt.colorbar(im, ax=ax_map)

ax_ts = fig.add_subplot(gs[0, 1])
ax_ts.plot(ts_df.index, ts_df['precip'], linewidth=0.5)
ax_ts.set_title('Time Series')

ax_clim = fig.add_subplot(gs[0, 2])
ax_clim.bar(months, monthly_mean, color='royalblue')
ax_clim.set_title('Climatology')
ax_clim.tick_params(axis='x', rotation=45)

ax_box = fig.add_subplot(gs[1, 0])
flat = ds.precip.values.reshape(len(ds.time), -1)
month_groups = []
for m in range(1, 13):
    mask = ds.time.dt.month.values == m
    vals = flat[mask][~np.isnan(flat[mask])].flatten()
    month_groups.append(vals)
ax_box.boxplot(month_groups, labels=months, patch_artist=True)
ax_box.set_title('Box Plot')
ax_box.tick_params(axis='x', rotation=45)

ax_hist = fig.add_subplot(gs[1, 1])
ax_hist.hist(ts_df['precip'], bins=40, color='mediumseagreen', edgecolor='white')
ax_hist.set_title('Histogram')

ax_trend = fig.add_subplot(gs[1, 2])
annual = ts_df.groupby(ts_df.index.year)['precip'].sum()
ax_trend.plot(annual.index, annual.values, 'o-', color='coral')
ax_trend.set_title('Annual Trend')

fig.suptitle('CHIRPS Rainfall Analysis Dashboard', fontsize=16, fontweight='bold')
plt.tight_layout()
fig.savefig('dashboard.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Solution 4.5: Portfolio Piece

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import xarray as xr
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.style.use('seaborn-v0_8')

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
annual = ts_df.groupby(ts_df.index.year)['precip'].sum()
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
ax1.set_extent([32, 48, 3, 15])
im = ax1.pcolormesh(ds.longitude, ds.latitude, ds.precip.mean(dim='time'),
                     transform=ccrs.PlateCarree(), cmap='YlGnBu')
ax1.add_feature(cfeature.COASTLINE, linewidth=0.6)
ax1.add_feature(cfeature.BORDERS, linewidth=0.4)
fig.colorbar(im, ax=ax1, label='Mean Monthly Precip (mm)')

ax2 = fig.add_subplot(gs[0, 1])
ax2.fill_between(ts_df.index, ts_df['precip'], alpha=0.2, color='#1f77b4')
ax2.plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='#1f77b4')
ts_df['rolling'] = ts_df['precip'].rolling(12).mean()
ax2.plot(ts_df.index, ts_df['rolling'], color='crimson', linewidth=1.5)
ax2.set_title('Time Series with 12-Month MA')
ax2.set_ylabel('mm/month')

ax3 = fig.add_subplot(gs[1, 0])
bars = ax3.bar(months, monthly_mean, color='#1f77b4', alpha=0.8)
ax3.bar_label(bars, fmt='%.0f')

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(annual.index, annual.values, 'o-', color='#d62728', linewidth=1.5)
z = np.polyfit(annual.index, annual.values, 1)
p = np.poly1d(z)
ax4.plot(annual.index, p(annual.index), '--', color='navy', alpha=0.6)
ax4.set_title('Annual Trend')
ax4.set_ylabel('mm/yr')

fig.suptitle('Ethiopian Rainfall Analysis (1981-2022)', fontsize=16, fontweight='bold')
plt.show()
```

---

## Solution 4.6: Report Generator

```python
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from pathlib import Path

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))

output_dir = Path('_report')
output_dir.mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(ts_df.index, ts_df['precip'], linewidth=0.5)
ax.set_title('Time Series')
fig.savefig(output_dir / 'timeseries.png', dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5))
monthly = ts_df.groupby(ts_df.index.month)['precip'].mean()
ax.bar(range(1, 13), monthly.values)
ax.set_title('Climatology')
fig.savefig(output_dir / 'climatology.png', dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(ts_df['precip'], bins=40, edgecolor='white')
ax.set_title('Distribution')
fig.savefig(output_dir / 'histogram.png', dpi=150)
plt.close(fig)

report = """# CHIRPS Rainfall Analysis Report

## Summary Statistics
- Mean: {:.1f} mm/month
- Median: {:.1f} mm/month
- Max: {:.1f} mm/month
- Std: {:.1f} mm/month
- Records: {} months

## Figures

### Time Series
![Time Series](timeseries.png)

### Climatology
![Climatology](climatology.png)

### Distribution
![Distribution](histogram.png)

## Data Source
CHIRPS Version 2.0, Climate Hazards Center, UC Santa Barbara
""".format(ts_df['precip'].mean(), ts_df['precip'].median(),
           ts_df['precip'].max(), ts_df['precip'].std(), len(ts_df))

(output_dir / 'report.md').write_text(report)
print("Report generated in {}".format(output_dir))
```
