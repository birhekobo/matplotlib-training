#import "../macros.typ": note-box, warning-box, info-box
= Time Series Visualization

Time series data records measurements at regular or irregular time intervals. This chapter covers plotting trends, seasonality, anomalies, and xarray integration.

== Basic Time Series Plot

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create sample time series
dates = pd.date_range('2024-01-01', periods=365, freq='D')
values = 20 + 10 * np.sin(2 * np.pi * dates.dayofyear / 365) + np.random.randn(365) * 3

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(dates, values, color='#1f77b4', linewidth=1, alpha=0.8)
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Daily Temperature Time Series')
ax.grid(alpha=0.3)
fig.autofmt_xdate()
plt.show()
```

=== Plotting with Pandas

```python
# Using pandas built-in plotting
ts = pd.Series(values, index=dates, name='Temperature')
fig, ax = plt.subplots(figsize=(12, 4))
ts.plot(ax=ax, color='#1f77b4')
ax.set_title('Pandas Time Series')
ax.set_ylabel('°C')
ax.grid(alpha=0.3)
plt.show()
```

=== Plotting with xarray

```python
import xarray as xr

# Create xarray DataArray
da = xr.DataArray(
    values,
    dims=['time'],
    coords={'time': dates},
    name='temperature'
)

fig, ax = plt.subplots(figsize=(12, 4))
da.plot(ax=ax, color='#d62728')
ax.set_title('xarray Time Series')
ax.grid(alpha=0.3)
plt.show()
```

== Rolling Statistics and Smoothing

```python
rolling_mean = ts.rolling(window=30).mean()
rolling_std = ts.rolling(window=30).std()

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(dates, values, alpha=0.3, color='gray', label='Daily')
ax.plot(dates, rolling_mean, color='#d62728', linewidth=2, label='30-day mean')
ax.fill_between(dates, rolling_mean - rolling_std, rolling_mean + rolling_std,
                alpha=0.2, color='#d62728', label='±1σ')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Time Series with Rolling Statistics')
ax.legend()
ax.grid(alpha=0.3)
fig.autofmt_xdate()
plt.show()
```

== Seasonal Decomposition

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Create data with trend + seasonality + noise
trend = np.linspace(20, 25, 365 * 3)
seasonal = 10 * np.sin(2 * np.pi * np.arange(365 * 3) / 365)
noise = np.random.randn(365 * 3) * 2
data = trend + seasonal + noise

dates_3y = pd.date_range('2022-01-01', periods=365 * 3, freq='D')
ts_3y = pd.Series(data, index=dates_3y)

# Decompose
result = seasonal_decompose(ts_3y, model='additive', period=365)

fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
ts_3y.plot(ax=axes[0], color='#1f77b4')
axes[0].set_title('Original')
axes[0].set_ylabel('Value')

result.trend.plot(ax=axes[1], color='#d62728')
axes[1].set_title('Trend')
axes[1].set_ylabel('Trend')

result.seasonal.plot(ax=axes[2], color='#2ca02c')
axes[2].set_title('Seasonal')
axes[2].set_ylabel('Seasonal')

result.resid.plot(ax=axes[3], color='gray', marker='o', linestyle='none', markersize=2)
axes[3].set_title('Residual')
axes[3].set_ylabel('Residual')

for ax in axes:
    ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

== Anomaly Visualization

=== Computing Anomalies

```python
# Create monthly climatology
monthly_mean = ts.groupby(ts.index.month).mean()
climatology = ts.copy()
for month in range(1, 13):
    climatology[climatology.index.month == month] = monthly_mean[month]

anomaly = ts - climatology

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].plot(dates, ts, color='#1f77b4', label='Observed')
axes[0].plot(dates, climatology, color='#d62728', linestyle='--', label='Climatology')
axes[0].set_ylabel('Temperature (°C)')
axes[0].legend()
axes[0].grid(alpha=0.3)
axes[0].set_title('Observed vs. Climatology')

colors = ['#d73027' if a > 0 else '#4575b4' for a in anomaly]
axes[1].bar(dates, anomaly, width=1, color=colors, alpha=0.7)
axes[1].axhline(y=0, color='black', linewidth=0.5)
axes[1].set_ylabel('Anomaly (°C)')
axes[1].set_title('Temperature Anomaly')
axes[1].grid(axis='y', alpha=0.3)

fig.autofmt_xdate()
plt.tight_layout()
plt.show()
```

== Multiple Time Series

```python
# Create multiple series
components = {
    'Temperature': values,
    'Precipitation': np.random.gamma(2, 5, 365),
    'Humidity': 60 + 20 * np.sin(2 * np.pi * dates.dayofyear / 365 + 1) + np.random.randn(365) * 5,
}

fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

colors = ['#d62728', '#1f77b4', '#2ca02c']
for ax, (name, data), color in zip(axes, components.items(), colors):
    ax.plot(dates, data, color=color, linewidth=1)
    ax.set_ylabel(name)
    ax.grid(alpha=0.3)
    ax.set_title(f'Daily {name}')

fig.autofmt_xdate()
fig.suptitle('Multi-Variable Time Series', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

== CHIRPS Time Series

```python
# CHIRPS time series with xarray
import xarray as xr

ds = xr.open_dataset('datasets/chirps_ethiopia.nc')
precip = ds['precip'].squeeze()

# Spatial average over East Africa
lat_slice = slice(-15, 25)
lon_slice = slice(20, 55)
precip_ea = precip.sel(lat=lat_slice, lon=lon_slice).mean(dim=['lat', 'lon'])

fig, ax = plt.subplots(figsize=(12, 4))
precip_ea.plot(ax=ax, color='#1f77b4', linewidth=2)
ax.set_xlabel('Time')
ax.set_ylabel('Mean Precipitation (mm/day)')
ax.set_title('CHIRPS East Africa — Mean Daily Precipitation')
ax.grid(alpha=0.3)
plt.show()
```

#note-box[
  xarray's `.plot()` method provides convenient time series plotting. For more customization, use matplotlib directly with the xarray data: `ax.plot(da.time, da.values)`.
]

== Summary

Time series visualization is essential for working with CHIRPS and other climate data. You learned how to plot daily data, compute rolling statistics, decompose seasonal patterns, visualize anomalies, and use pandas and xarray integration. In the next chapter, we explore geographic visualization with Cartopy.







