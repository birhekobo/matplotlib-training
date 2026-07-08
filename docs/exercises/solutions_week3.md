---
title: Week 3 Solutions
---

# Week 3 Solutions

---

## Solution 3.1: Box Plot by Month

```python
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('../chirps_1981_2022.nc')
flat = ds.precip.values.reshape(len(ds.time), -1)
months = ds.time.dt.month.values

monthly_groups = {m: [] for m in range(1, 13)}
for i, m in enumerate(months):
    vals = flat[i][~np.isnan(flat[i])]
    monthly_groups[m].extend(vals.tolist())

month_data = [monthly_groups[m] for m in range(1, 13)]
month_labels = ['Jan','Feb','Mar','Apr','May','Jun',
                'Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax = plt.subplots(figsize=(12, 6))
bp = ax.boxplot(month_data, labels=month_labels, patch_artist=True)

colors = plt.cm.viridis(np.linspace(0.2, 0.9, 12))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xlabel('Month')
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Monthly Rainfall Distribution')
ax.grid(True, alpha=0.3, axis='y')
plt.show()
```

---

## Solution 3.2: Trend Analysis

```python
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
annual = ts_df.groupby(ts_df.index.year)['precip'].sum()

years = annual.index.values
rainfall = annual.values
slope, intercept, r, p, se = stats.linregress(years, rainfall)
trend = slope * years + intercept

n = len(years)
y_pred = trend
resid = rainfall - y_pred
mse = np.sum(resid**2) / (n - 2)
se_fit = np.sqrt(mse * (1/n + (years - np.mean(years))**2 / np.sum((years - np.mean(years))**2)))
ci = stats.t.ppf(0.975, n-2) * se_fit

fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(years, y_pred - ci, y_pred + ci, alpha=0.2, color='steelblue', label='95% CI')
ax.plot(years, y_pred, color='crimson', linewidth=2,
        label='Trend: {:.1f} mm/yr (p={:.3f}, R^2={:.2f})'.format(slope, p, r**2))
ax.scatter(years, rainfall, s=40, color='steelblue', edgecolor='black', alpha=0.8)
ax.set_xlabel('Year')
ax.set_ylabel('Annual Rainfall (mm)')
ax.set_title('Annual Rainfall Trend at Addis Ababa')
ax.legend()
ax.grid(True, alpha=0.3)
plt.show()
```

---

## Solution 3.3: Correlation Heatmap

```python
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import seaborn as sns

ds = xr.open_dataset('../chirps_1981_2022.nc')
cities = {
    'Addis Ababa': (180, 174),
    'Gondar': (252, 150),
    'Mekelle': (270, 190),
    'Dire Dawa': (192, 237),
    'Jimma': (8, 144),
    'Bahir Dar': (235, 140),
}

data = {}
for name, (li, lo) in cities.items():
    data[name] = ds.precip.isel(latitude=li, longitude=lo).values

df = pd.DataFrame(data)
corr = df.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='RdBu_r', vmin=-1, vmax=1,
            square=True, ax=ax, cbar_kws={'label': 'Pearson r'})
ax.set_title('Rainfall Correlation Between Ethiopian Cities')
plt.show()
```

---

## Solution 3.4: Contour Map

```python
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

ds = xr.open_dataset('../chirps_1981_2022.nc')
precip = ds.precip.isel(time=0)

lon, lat = np.meshgrid(ds.longitude, ds.latitude)

fig, ax = plt.subplots(figsize=(12, 8))
filled = ax.contourf(lon, lat, precip, levels=20, cmap='Blues')
contours = ax.contour(lon, lat, precip, levels=10, colors='black', linewidths=0.5)
ax.clabel(contours, inline=True, fontsize=8)
fig.colorbar(filled, ax=ax, label='Precipitation (mm)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('CHIRPS Precipitation Contour Map')
plt.show()
```

---

## Solution 3.5: Global Map with Cartopy

```python
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds = xr.open_dataset('../chirps_1981_2022.nc')
precip = ds.precip.isel(time=0)

fig, ax = plt.subplots(figsize=(14, 8), subplot_kw={'projection': ccrs.Robinson()})
ax.set_global()

pcm = ax.pcolormesh(ds.longitude, ds.latitude, precip,
                     transform=ccrs.PlateCarree(), cmap='Blues')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)

gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
gl.top_labels = False
gl.right_labels = False

fig.colorbar(pcm, ax=ax, label='Precipitation (mm)', shrink=0.6)
ax.set_title('Global CHIRPS Precipitation - Robinson Projection')
plt.show()
```

---

## Solution 3.6: Rolling Statistics

```python
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('../chirps_1981_2022.nc')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))

ts_df['rolling_mean'] = ts_df['precip'].rolling(window=12, center=True).mean()
ts_df['rolling_std'] = ts_df['precip'].rolling(window=12).std()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(ts_df.index, ts_df['precip'], alpha=0.3, linewidth=0.5, label='Monthly')
ax.plot(ts_df.index, ts_df['rolling_mean'], color='crimson', linewidth=1.5, label='12-month MA')
ax.fill_between(ts_df.index,
                ts_df['rolling_mean'] - ts_df['rolling_std'],
                ts_df['rolling_mean'] + ts_df['rolling_std'],
                alpha=0.15, color='crimson', label='+/-1 Std')
ax.set_xlabel('Year')
ax.set_ylabel('Precipitation (mm/month)')
ax.set_title('CHIRPS Rainfall - Rolling Statistics')
ax.legend()
fig.savefig('rolling_stats.png', dpi=300, bbox_inches='tight')
plt.show()
```
