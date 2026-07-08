#import "../macros.typ": note-box, warning-box, info-box
= Geographic Visualization

Geographic visualization combines Matplotlib with Cartopy to create maps. This chapter focuses on visualizing CHIRPS rainfall data on maps with various projections.

== Cartopy Fundamentals

Cartopy is a library for geospatial data processing and map production. It provides:

- *Coordinate Reference Systems (CRS)*: Map projections
- *Geometric features*: Coastlines, borders, rivers
- *Transformations*: Convert between coordinate systems

=== Common Projections

```python
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Plate Carrée (simple lat/lon as Cartesian)
crs_plate = ccrs.PlateCarree()

# Robinson (aesthetic world maps)
crs_robinson = ccrs.Robinson()

# Mercator (navigation, shape-preserving)
crs_mercator = ccrs.Mercator()

# Orthographic (globe view)
crs_ortho = ccrs.Orthographic(central_longitude=20, central_latitude=10)

# Lambert Conformal (mid-latitude regions)
crs_lambert = ccrs.LambertConformal()

# Polar Stereographic (polar regions)
crs_polar = ccrs.NorthPolarStereo()
```

#note-box[
  Specify both the *axes projection* (how the map is drawn) and the *data transform* (how the data coordinates are interpreted). For lat/lon data, always use `transform=ccrs.PlateCarree()`.
]

== Basic Map

```python
fig, ax = plt.subplots(figsize=(10, 6),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# Geographic features
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.7)
ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.3)
ax.add_feature(cfeature.LAND, color='lightgreen', alpha=0.3)
ax.add_feature(cfeature.LAKES, color='lightblue', alpha=0.5)
ax.add_feature(cfeature.RIVERS, color='blue', alpha=0.3)

# Set extent (lon_min, lon_max, lat_min, lat_max)
ax.set_extent([-20, 50, -15, 40])

# Gridlines
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.5)
gl.top_labels = False
gl.right_labels = False

ax.set_title('Basic Map: Africa and Europe')
plt.show()
```

== CHIRPS Precipitation Map

```python
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load CHIRPS data
ds = xr.open_dataset('datasets/chirps_ethiopia.nc')
precip = ds['precip'].squeeze()
precip = precip.where(precip >= 0)  # Mask fill values

fig, ax = plt.subplots(figsize=(12, 6),
                       subplot_kw={'projection': ccrs.PlateCarree()})

# Plot precipitation
pcm = ax.pcolormesh(ds.lon, ds.lat, precip,
                    cmap='Blues', transform=ccrs.PlateCarree(),
                    shading='auto')

# Features
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)

# Colorbar
cbar = fig.colorbar(pcm, ax=ax, orientation='horizontal',
                    pad=0.05, shrink=0.8, label='Precipitation (mm/day)')

# Gridlines
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
gl.top_labels = False
gl.right_labels = False

ax.set_title('CHIRPS Daily Precipitation — January 2024', fontsize=14)
plt.show()
```

== Multiple Projections Subplot

```python
projections = {
    'Plate Carrée': ccrs.PlateCarree(),
    'Robinson': ccrs.Robinson(),
    'Orthographic': ccrs.Orthographic(central_longitude=20, central_latitude=10),
    'Mercator': ccrs.Mercator(),
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10),
                         subplot_kw={'projection': ccrs.PlateCarree()})

for ax, (name, proj) in zip(axes.flat, projections.items()):
    # Switch projection
    ax.projection = proj
    # Re-create the figure with this projection
    # Instead, we use a trick: remove old axes, add new
    fig.delaxes(ax)

# Better approach: create all axes at once
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

projs = [
    ccrs.PlateCarree(),
    ccrs.Robinson(),
    ccrs.Orthographic(central_longitude=20, central_latitude=10),
    ccrs.Mercator(),
]
titles = ['Plate Carrée', 'Robinson', 'Orthographic', 'Mercator']

for i, ax in enumerate(axes.flat):
    ax.remove()

# Add axes with projections
for i, (proj, title) in enumerate(zip(projs, titles)):
    ax = fig.add_subplot(2, 2, i + 1, projection=proj)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.OCEAN, color='lightblue', alpha=0.2)
    ax.add_feature(cfeature.LAND, color='lightgreen', alpha=0.2)
    if proj == ccrs.PlateCarree():
        ax.set_global()
    gl = ax.gridlines(linestyle='--', alpha=0.3, draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    ax.set_title(title, fontsize=11)

plt.tight_layout()
plt.show()
```

== Adding Point Data

```python
# Cities of interest
cities = {
    'Nairobi': (36.82, -1.29),
    'Addis Ababa': (38.74, 9.03),
    'Dakar': (-17.44, 14.69),
    'Cairo': (31.24, 30.04),
    'Cape Town': (18.42, -33.92),
    'Lagos': (3.38, 6.45),
}

fig, ax = plt.subplots(figsize=(12, 8),
                       subplot_kw={'projection': ccrs.Robinson()})

ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)
ax.set_global()

for city, (lon, lat) in cities.items():
    ax.plot(lon, lat, 'r*', markersize=12, transform=ccrs.PlateCarree())
    ax.text(lon + 2, lat, city, transform=ccrs.PlateCarree(),
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax.set_title('African Cities on CHIRPS Domain', fontsize=14)
gl = ax.gridlines(linestyle='--', alpha=0.3, draw_labels=True)
gl.top_labels = False
gl.right_labels = False
plt.show()
```

== Regional Zoom

```python
# East Africa focus
fig, ax = plt.subplots(figsize=(10, 10),
                       subplot_kw={'projection': ccrs.PlateCarree(
                           central_longitude=35)})

ax.set_extent([20, 55, -15, 25])

# High-resolution features
ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.8)
ax.add_feature(cfeature.LAKES, alpha=0.6, color='lightblue')
ax.add_feature(cfeature.RIVERS, alpha=0.4, color='blue')
ax.add_feature(cfeature.OCEAN, alpha=0.2, color='lightblue')

# CHIRPS data overlay
precip_slice = precip.sel(lat=slice(-15, 25), lon=slice(20, 55))
pcm = ax.pcolormesh(precip_slice.lon, precip_slice.lat, precip_slice,
                    cmap='Blues', transform=ccrs.PlateCarree(),
                    shading='auto')

cbar = fig.colorbar(pcm, ax=ax, orientation='horizontal',
                    pad=0.05, shrink=0.8, label='Precipitation (mm/day)')

gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
gl.top_labels = False
gl.right_labels = False

ax.set_title('East Africa — CHIRPS Precipitation', fontsize=14)
plt.show()
```

== Selecting Color Palettes for Maps

```python
# Sequential for precipitation
cmap_precip = plt.cm.Blues

# Sequential for elevation
cmap_elev = plt.cm.terrain

# Diverging for anomalies
cmap_anom = plt.cm.RdBu

# Qualitative for land cover
cmap_cover = plt.cm.Set3

# Custom norm for precipitation
import matplotlib.colors as mcolors
norm = mcolors.LogNorm(vmin=0.1, vmax=100)
norm = mcolors.PowerNorm(gamma=0.5, vmin=0, vmax=50)
```

#warning-box[
  Log and Power normalizations can make maps hard to interpret. Always include clear colorbar labels and tick values. Consider users who need to read precise values from the map.
]

== Summary

You can now create publication-quality geographic visualizations with Cartopy and Matplotlib. You learned about map projections, geographic features, CHIRPS data overlays, point data, regional zooms, and color palette selection. In the next chapter, we explore NumPy and Pandas integration.








