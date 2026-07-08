#import "../macros.typ": note-box, warning-box, info-box
= NumPy and Pandas Integration

Matplotlib works best when integrated with NumPy and Pandas. This chapter covers transforming, aggregating, and visualizing data from these libraries.

== NumPy Integration

NumPy arrays are the native data format for Matplotlib. All plotting functions accept arrays.

=== Generating Data with NumPy

```python
import numpy as np
import matplotlib.pyplot as plt

# Linspace for smooth curves
x = np.linspace(0, 10, 1000)

# Random data
np.random.seed(42)
scatter_x = np.random.randn(500)
scatter_y = np.random.randn(500)

# Grid data for 2D plots
x_2d = np.linspace(-3, 3, 100)
y_2d = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x_2d, y_2d)
Z = np.sin(X) * np.cos(Y)
```

=== Statistical Operations

```python
# Compute statistics for error bars
data = np.random.randn(1000, 5)
means = data.mean(axis=0)
stds = data.std(axis=0)
medians = np.median(data, axis=0)

fig, ax = plt.subplots(figsize=(8, 5))
x_pos = np.arange(5)
ax.bar(x_pos, means, yerr=stds, capsize=5, color='steelblue',
       tick_label=['A', 'B', 'C', 'D', 'E'])
ax.set_ylabel('Mean Value')
ax.set_title('Group Means with Standard Deviations')
plt.show()
```

=== Masked Arrays

```python
# Handle missing data with masked arrays
data = np.random.randn(100)
data[20:30] = np.nan  # Missing values

# Option 1: Remove NaNs
clean_data = data[~np.isnan(data)]

# Option 2: Use masked array
masked_data = np.ma.masked_invalid(data)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(masked_data, 'o-', color='#1f77b4')
ax.axvspan(20, 30, alpha=0.2, color='red', label='Missing data')
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.legend()
ax.set_title('Time Series with Missing Data (Masked)')
plt.show()
```

== Pandas Integration

Pandas DataFrames are the standard data structure for tabular data.

=== Direct DataFrame Plotting

```python
import pandas as pd

# Create DataFrame
dates = pd.date_range('2024-01-01', periods=100, freq='D')
df = pd.DataFrame({
    'date': dates,
    'temperature': 25 + 10 * np.sin(2 * np.pi * dates.dayofyear / 365) + np.random.randn(100) * 2,
    'precipitation': np.random.gamma(2, 3, 100),
    'humidity': 60 + 20 * np.random.rand(100),
})

# Direct plotting with pandas
fig, ax = plt.subplots(figsize=(10, 4))
df.plot(x='date', y='temperature', ax=ax, color='#d62728',
        legend=False, linewidth=2)
ax.set_ylabel('Temperature (°C)')
ax.set_title('Pandas DataFrame Direct Plot')
ax.grid(alpha=0.3)
plt.show()
```

=== GroupBy and Aggregation

```python
# Add month and season columns
df['month'] = df['date'].dt.month
df['season'] = pd.cut(df['month'],
                       bins=[0, 3, 6, 9, 12],
                       labels=['DJF', 'MAM', 'JJA', 'SON'])

# Group by season
seasonal_stats = df.groupby('season')[['temperature', 'precipitation']].agg(['mean', 'std'])

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Temperature by season
seasonal_stats['temperature']['mean'].plot(
    kind='bar', ax=axes[0], color=['#4575b4', '#fee090', '#d73027', '#91bfdb'],
    yerr=seasonal_stats['temperature']['std'], capsize=5)
axes[0].set_ylabel('Mean Temperature (°C)')
axes[0].set_title('Temperature by Season')
axes[0].grid(axis='y', alpha=0.3)

# Precipitation by season
seasonal_stats['precipitation']['mean'].plot(
    kind='bar', ax=axes[1], color=['#4575b4', '#fee090', '#d73027', '#91bfdb'],
    yerr=seasonal_stats['precipitation']['std'], capsize=5)
axes[1].set_ylabel('Mean Precipitation (mm)')
axes[1].set_title('Precipitation by Season')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

=== Pivot Tables and Heatmaps

```python
# Create a pivot table (month × year)
df['year'] = df['date'].dt.year
pivot = df.pivot_table(values='temperature',
                       index=df['date'].dt.month,
                       columns=df['date'].dt.year,
                       aggfunc='mean')

fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(pivot.values, cmap='RdBu_r', aspect='auto')
ax.set_xticks(range(len(pivot.columns)))
ax.set_yticks(range(len(pivot.index)))
ax.set_xticklabels(pivot.columns)
ax.set_yticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
fig.colorbar(im, ax=ax, label='Temperature (°C)')
ax.set_title('Monthly Temperature Heatmap')
plt.show()
```

== xarray Integration

xarray extends Pandas to multi-dimensional labeled arrays, which is essential for CHIRPS and other climate data.

```python
import xarray as xr

# Open CHIRPS data
ds = xr.open_dataset('datasets/chirps_ethiopia.nc')
precip = ds['precip'].squeeze()

# Compute statistics along dimensions
zonal_mean = precip.mean(dim='lon')
tropical_mean = precip.sel(lat=slice(-23.5, 23.5)).mean(dim=['lat', 'lon'])

# Plot with xarray's built-in plotting
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Zonal mean profile
zonal_mean.plot(ax=axes[0], color='#1f77b4', linewidth=2)
axes[0].set_xlabel('Latitude')
axes[0].set_ylabel('Mean Precipitation (mm/day)')
axes[0].set_title('Zonal Mean Precipitation')
axes[0].grid(alpha=0.3)

# Map using xarray
precip.plot(ax=axes[1], cmap='Blues', cbar_kwargs={'label': 'mm/day'})
axes[1].set_title('CHIRPS Global Precipitation')
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')

plt.tight_layout()
plt.show()
```

== Using ggplot2 Style with Pandas

```python
# Simulate ggplot2-style plotting
plt.style.use('ggplot')

fig, ax = plt.subplots(figsize=(10, 5))
df.plot(kind='scatter', x='temperature', y='humidity',
        s=df['precipitation'] * 5, c='precipitation',
        cmap='viridis', ax=ax, alpha=0.6,
        colorbar=True)
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Humidity (%)')
ax.set_title('Bubble Chart: Weather Variables')
plt.show()
```

#note-box[
  The pandas `.plot()` method is convenient for quick exploration, but for publication-quality figures, extract the data and use Matplotlib's OO API directly for full control.
]

== Summary

You learned how to integrate NumPy, Pandas, and xarray with Matplotlib for efficient data manipulation and visualization. NumPy provides the array foundation, Pandas offers convenient DataFrame plotting, and xarray excels at multi-dimensional climate data. In the next chapter, we explore advanced Matplotlib techniques.







