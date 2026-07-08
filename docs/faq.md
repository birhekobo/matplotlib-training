---
title: Frequently Asked Questions
---

# Frequently Asked Questions

---

## Common Errors

### `RuntimeError: main thread is not in main loop` (Jupyter)

**Cause**: Using `plt.show()` inside a script that's not running in the main thread.

**Solution**:

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3])
fig.savefig('output.png')
```

### `ValueError: to_rgba: Invalid rgba arg`

**Cause**: Using an invalid color specification.

**Solution**: Verify color string:

```python
# Use valid color names, hex codes, or RGB tuples
colors = ['red', '#ff5733', (0.3, 0.7, 0.2)]
```

### `UserWarning: Attempting to set identical low and high`

**Cause**: Plotting data where min == max (e.g., all points have same value).

**Solution**: Check your data for constant values:

```python
# Add small noise or skip constant data
if data.min() == data.max():
    print("Warning: constant data detected, skipping plot")
else:
    ax.plot(data)
```

### `KeyError: 'precip'` when opening CHIRPS data

**Cause**: Variable name differs from expected.

**Solution**: Check available variables:

```python
import xarray as xr
ds = xr.open_dataset('chirps_data.nc')
print(list(ds.data_vars))  # List all variables
print(ds)                  # Full dataset info
```

### Cartopy `ValueError: Image size is too small`

**Cause**: Using `pcolormesh` with a tiny figure or large data extent.

**Solution**: Increase figure size or subsample data:

```python
fig, ax = plt.subplots(figsize=(12, 6))  # Larger figure
# Or subsample
precip_sampled = precip[::5, ::5]        # Every 5th point
```

---

## Troubleshooting Tips

### Plots Not Showing in Jupyter Notebook

```python
# Try these in order:
%matplotlib inline        # Static plots
%matplotlib notebook      # Interactive plots
%matplotlib widget        # Jupyter Widgets (requires ipympl)
```

### Fonts Rendering Incorrectly

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# List available fonts
fonts = [f.name for f in fm.fontManager.ttflist]
print(sorted(set(fonts)))

# Set a specific font
plt.rcParams['font.family'] = 'Times New Roman'
```

### Large Figures Are Slow

```python
# Reduce resolution
fig, ax = plt.subplots(dpi=72)  # Default is 100

# Use simpler rendering
ax.pcolormesh(x, y, z, shading='auto')  # Faster than imshow for large grids

# Subsampling
x_sampled = x[::2, ::2]
y_sampled = y[::2, ::2]
z_sampled = z[::2, ::2]
```

### Saving Transparent Figures

```python
fig.savefig('figure.png', transparent=True)
fig.savefig('figure.pdf', transparent=True)
```

### Memory Not Released After Plotting

```python
# In scripts, close figures explicitly
fig, ax = plt.subplots()
ax.plot(data)
fig.savefig('output.png')
plt.close(fig)  # Critical in loops!

# Or clear all figures
plt.close('all')
```

---

## Performance Optimization

### Use `plt.close()` in Loops

```python
for idx, dataset in enumerate(datasets):
    fig, ax = plt.subplots()
    ax.plot(dataset)
    fig.savefig(f'figure_{idx:03d}.png')
    plt.close(fig)  # Prevents memory leak
```

### Aggregate Instead of Iterating

```python
# Slow: one scatter call per point
for x, y in zip(xs, ys):
    ax.scatter(x, y)

# Fast: one call for all data
ax.scatter(xs, ys)
```

### Use Blitting for Animations

```python
import matplotlib.animation as animation

fig, ax = plt.subplots()
line, = ax.plot([], [])

def init():
    line.set_data([], [])
    return line,

def animate(frame):
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + frame * 0.1)
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(fig, animate, frames=100,
                              init_func=init, blit=True)
```

### Vectorize with NumPy

```python
# Slow: Python loop
for i in range(len(y)):
    y[i] = np.sin(x[i])

# Fast: vectorized
y = np.sin(x)
```

### Use `rasterized=True` for Large Scatter Plots

```python
ax.scatter(x, y, s=1, rasterized=True)
# Rasterizes the marker layer while keeping text/axes as vectors
```

---

## Cartopy-Specific Issues

### Missing Shapefiles on Linux

```bash
conda install -c conda-forge cartopy
# Or manually download naturalearth data
python -c "import cartopy; cartopy.io.shapereader.natural_earth(resolution='110m', category='physical', name='coastline')"
```

### Gridlines Not Visible

```python
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray',
                  linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False
```

### Incorrect Map Extent

```python
# PlateCarree extent uses (lon_min, lon_max, lat_min, lat_max)
ax.set_extent([-20, 60, -40, 40], crs=ccrs.PlateCarree())

# For other projections, specify the CRS of the extent coordinates
ax.set_extent([0, 50, 20, 60], crs=ccrs.PlateCarree())
```

---

## General Tips

| Issue | Quick Fix |
|-------|-----------|
| Plot not responding | `plt.close('all')` and rerun |
| Inline plots blurry | `plt.rcParams['figure.dpi'] = 150` |
| Labels overlapping | `plt.tight_layout()` |
| Legend outside plot | `ax.legend(bbox_to_anchor=(1.05, 1))` |
| Date labels rotated | `fig.autofmt_xdate()` |
| Colorbar too small | `fig.colorbar(..., shrink=0.8)` |
| Grid lines over data | Set `zorder` on data (higher = on top) |
