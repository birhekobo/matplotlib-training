---
title: Week 2 Solutions
---

# Week 2 Solutions

---

## Solution 2.1: Time Series with CHIRPS Data

```python
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(ts.time, ts.values, linewidth=0.6, color='steelblue')
ax.set_title('CHIRPS Monthly Rainfall at Addis Ababa (9.025N, 38.725E)')
ax.set_xlabel('Year')
ax.set_ylabel('Precipitation (mm/month)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## Solution 2.2: Multi-Panel Climatology

```python
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
monthly = ts.groupby('time.month').mean().values
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0,0].plot(months, monthly, 'o-', color='steelblue')
axes[0,0].set_title('Line Plot')

bars = axes[0,1].bar(months, monthly, color='royalblue')
axes[0,1].bar_label(bars, fmt='%.0f')
axes[0,1].set_title('Bar Chart')

sorted_idx = np.argsort(monthly)
axes[1,0].barh([months[i] for i in sorted_idx], monthly[sorted_idx], color='teal')
axes[1,0].set_title('Sorted Horizontal Bar')

markerline, stemlines, baseline = axes[1,1].stem(months, monthly)
axes[1,1].set_title('Stem Plot')

for ax in axes.flat:
    ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
```

---

## Solution 2.3: Styled Publication Plot

```python
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))

with plt.style.context('seaborn-v0_8'):
    fig, ax = plt.subplots(figsize=(14, 5))
    sub = ts_df.loc['2010':'2019']
    ax.fill_between(sub.index, sub['precip'], alpha=0.3, color='steelblue')
    ax.plot(sub.index, sub['precip'], linewidth=0.8, color='steelblue')
    ax.axhline(sub['precip'].mean(), color='crimson', linestyle='--',
               label="Mean = {:.1f} mm".format(sub['precip'].mean()))
    ax.set_title('CHIRPS Rainfall 2010-2019, Addis Ababa')
    ax.set_xlabel('Date')
    ax.set_ylabel('Precipitation (mm/month)')
    ax.legend()
    plt.tight_layout()
    fig.savefig('publication_plot.pdf', dpi=300, bbox_inches='tight')
    plt.show()
```

---

## Solution 2.4: GridSpec Layout

```python
import matplotlib.gridspec as gridspec
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(3, 2, figure=fig, width_ratios=[2, 1], height_ratios=[1, 1, 1.5])

ax0 = fig.add_subplot(gs[0, :])
ax0.plot(ts_df.index, ts_df['precip'], linewidth=0.5)
ax0.set_title('Full Time Series')

ax1 = fig.add_subplot(gs[1, 0])
ax1.bar(months, monthly_mean, color='royalblue')
ax1.tick_params(axis='x', rotation=45)

ax2 = fig.add_subplot(gs[1, 1])
ax2.hist(ts_df['precip'], bins=40, color='mediumseagreen', edgecolor='white')

ax3 = fig.add_subplot(gs[2, :])
lat_slice = ds.precip.isel(time=0)
im = ax3.pcolormesh(ds.longitude, ds.latitude, lat_slice, cmap='Blues')
plt.colorbar(im, ax=ax3, label='mm/month')

plt.tight_layout()
plt.show()
```

---

## Solution 2.5: Inset Zoom

```python
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(ts_df.index, ts_df['precip'], linewidth=0.6, color='steelblue')
ax.set_title('CHIRPS Addis Ababa - Full Record with Inset Zoom')

ax_inset = ax.inset_axes([0.15, 0.55, 0.25, 0.35])
year97 = ts_df.loc['1997']
ax_inset.plot(year97.index, year97['precip'], 'o-', color='coral', markersize=4)
ax_inset.set_title('1997 (El Nino)', fontsize=10)
ax.indicate_inset_zoom(ax_inset, edgecolor='gray')
plt.show()
```

---

## Solution 2.6: Twin Axes

```python
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
monthly_std = ts_df.groupby(ts_df.index.month)['precip'].std()
cv = monthly_std / monthly_mean * 100
months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.bar(months, monthly_mean, color='steelblue', alpha=0.6, label='Mean')
ax1.set_ylabel('Precipitation (mm/month)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

ax2 = ax1.twinx()
ax2.plot(months, cv, 'o-', color='darkred', linewidth=2, label='CV (%)')
ax2.set_ylabel('Coefficient of Variation (%)', color='darkred')
ax2.tick_params(axis='y', labelcolor='darkred')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax1.set_title('Mean Rainfall vs Coefficient of Variation')
ax1.tick_params(axis='x', rotation=45)
plt.show()
```
