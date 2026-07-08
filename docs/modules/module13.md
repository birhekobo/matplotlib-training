---
title: Module 13 — Working with NumPy and Pandas
---

# Module 13: Working with NumPy and Pandas

Integrate Matplotlib with NumPy and Pandas for efficient data manipulation and visualisation.

---

## Learning Objectives

- Use NumPy arrays directly with Matplotlib
- Leverage Pandas built-in plotting methods
- Create visualisations from DataFrame groupby operations
- Combine xarray with Matplotlib for geospatial data
- Build visualisation pipelines

---

## Pandas Plotting

```python
df['precip'].plot(figsize=(14, 4), title='CHIRPS Rainfall')
df.groupby(df.index.month)['precip'].mean().plot(kind='bar')
df.plot.scatter(x='var1', y='var2', alpha=0.5)
```

---

## NumPy Integration

```python
data = np.random.randn(1000)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(data, bins=30)
axes[1].plot(np.cumsum(data))
```

---

## xarray Integration

```python
import xarray as xr

ds = xr.open_dataset('../datasets/chirps_ethiopia.nc')
ds['precip'].mean(dim=['latitude', 'longitude']).plot()
```

---

## Exercises

1. Use Pandas .plot() to create a line plot of CHIRPS data
2. Create a scatter matrix with pd.plotting.scatter_matrix
3. Use xarray's built-in .plot() method
4. Combine NumPy statistics with a Matplotlib annotation

---

## Next Steps

Proceed to {doc}`module14` for advanced Matplotlib techniques.
