---
title: Module 12 — Geographic Visualization
---

# Module 12: Geographic Visualization

This module explores geographic data visualization using Cartopy, xarray, and the CHIRPS rainfall dataset.

---

## Learning Objectives

- Understand map projections and coordinate reference systems
- Create choropleth and contour maps with Cartopy
- Overlay geographic features (coastlines, borders, rivers)
- Visualize CHIRPS rainfall data on maps
- Create map subplots with different projections

---

## Cartopy Basics

[Cartopy](https://scitools.org.uk/cartopy/) is a library for geospatial data processing and map production.

### Common Projections

```python
import cartopy.crs as ccrs

# Most common projections
ccrs.PlateCarree()        # Equirectangular (simple lat/lon)
ccrs.Mercator()           # Mercator (navigation)
ccrs.Robinson()           # Robinson (world maps, aesthetic)
ccrs.Orthographic()       # Globe from space
ccrs.LambertConformal()   # Mid-latitude regions
ccrs.NorthPolarStereo()   # Polar regions
```

:::{note}
`PlateCarree` treats longitude/latitude as Cartesian coordinates. Use it for simple plots, but switch to `Robinson` or `Orthographic` for world maps.
:::

---

## Basic Map

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

fig, ax = plt.subplots(figsize=(10, 6),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# Add geographic features
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.7)
ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
ax.add_feature(cfeature.LAND, color='lightgreen', alpha=0.3)

# Set extent (lon_min, lon_max, lat_min, lat_max)
ax.set_extent([-20, 50, -10, 50])

# Gridlines
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False

ax.set_title('Basic Map of Africa and Europe')
plt.show()
```

---

## Visualizing CHIRPS Rainfall Data

```python
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import numpy as np

# Load CHIRPS data (NetCDF format)
ds = xr.open_dataset('../datasets/chirps_ethiopia.nc')
precip = ds['precip'].squeeze()  # Remove time dimension

fig, ax = plt.subplots(figsize=(12, 6),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# Contour fill plot
pcm = ax.contourf(ds.lon, ds.lat, precip,
                  levels=20, cmap='Blues',
                  transform=ccrs.PlateCarree())

# Geographic features
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)

# Colorbar
cbar = fig.colorbar(pcm, ax=ax, orientation='horizontal',
                    pad=0.05, shrink=0.8, label='Precipitation (mm/day)')

# Gridlines
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
gl.top_labels = False
gl.right_labels = False

ax.set_title('CHIRPS Daily Precipitation — 01 Jan 2024')
plt.show()
```

---

## Multiple Projections

```python
projections = {
    'Plate Carrée': ccrs.PlateCarree(),
    'Robinson': ccrs.Robinson(),
    'Orthographic': ccrs.Orthographic(central_longitude=20, central_latitude=10),
    'Mercator': ccrs.Mercator(),
}

fig, axes = plt.subplots(2, 2, figsize=(12, 10),
                         subplot_kw={'projection': ccrs.Robinson()})

for ax, (name, proj) in zip(axes.flat, projections.items()):
    ax.projection = proj
    ax.set_title(name, fontsize=10)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.2)
    ax.add_feature(cfeature.LAND, color='lightgreen', alpha=0.2)
    ax.gridlines(linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Customizing Map Appearance

### Color Palettes for Precipitation

```python
import matplotlib.colors as mcolors

# Sequential palette for rainfall
cmap = plt.cm.Blues

# Diverging palette for anomaly
cmap_div = plt.cm.RdBu

# Custom normalization
norm = mcolors.LogNorm(vmin=0.1, vmax=100)
norm = mcolors.TwoSlopeNorm(vmin=-50, vcenter=0, vmax=50)
```

### Adding City Markers

```python
cities = {
    'Nairobi': [36.82, -1.29],
    'Addis Ababa': [38.74, 9.03],
    'Dakar': [-17.44, 14.69],
    'Cairo': [31.24, 30.04],
}

for city, (lon, lat) in cities.items():
    ax.plot(lon, lat, 'r*', markersize=10, transform=ccrs.PlateCarree())
    ax.text(lon + 1, lat, city, transform=ccrs.PlateCarree(),
            fontsize=9, fontweight='bold')
```

---

## Exercises

1. Create a map of Africa showing CHIRPS annual precipitation
2. Use a Robinson projection with country borders
3. Overlay major river features on the map
4. Create a 2×2 subplot with different projections of the same data
5. Add a colorbar with custom tick labels

---

## References

- [Cartopy Documentation](https://scitools.org.uk/cartopy/docs/latest/)
- [CHIRPS Dataset](https://www.chc.ucsb.edu/data/chirps)
- [xarray Documentation](https://docs.xarray.dev/en/stable/)

---

## Next Steps

Apply these skills in the {doc}`../projects/rainfall_dashboard` project.
