#import "../macros.typ": note-box, warning-box, info-box
= Real-World Projects

This chapter presents three real-world projects that combine all the skills you have learned. Each project includes objectives, data sources, step-by-step instructions, and expected outputs.

== Project 1: Climate Report Dashboard

=== Objective

Create a multi-panel dashboard summarizing monthly climate data for a selected region.

=== Data

Use the provided CHIRPS sample data or download fresh data:

```python
import xarray as xr
import numpy as np

ds = xr.open_dataset('datasets/chirps_ethiopia.nc')
precip = ds['precip'].squeeze()
```

=== Requirements

1. A 2x2 subplot layout:
   - *Top-left*: Map of monthly precipitation (Robinson projection)
   - *Top-right*: Regional zoom showing high-resolution detail
   - *Bottom-left*: Time series of regional mean precipitation
   - *Bottom-right*: Histogram of precipitation distribution

2. Consistent color palette across all panels
3. Professional labeling and titles
4. Colorbar with appropriate label and ticks

=== Step-by-Step

1. Load and clean the CHIRPS data
2. Create the figure with GridSpec for custom layout
3. Create each panel using appropriate plot types
4. Add a shared colorbar for the map panels
5. Add panel labels (a, b, c, d)
6. Save at 300 DPI as both PNG and PDF

=== Hints

- Use `layout='constrained'` for automatic spacing
- Mask negative values with `precip.where(precip >= 0)`
- Use `Robinson` projection for the global map and `PlateCarree` for the regional zoom

== Project 2: Time Series Anomaly Analysis

=== Objective

Analyze and visualize precipitation anomalies over a multi-year period.

=== Data

Multi-year CHIRPS data (provided in `datasets/`):

```python
# Load multiple files
files = sorted(glob('datasets/chirps_*.nc'))
ds = xr.open_mfdataset(files, combine='by_coords')
precip = ds['precip']
```

=== Requirements

1. Compute the monthly climatology (1981-2010 base period)
2. Calculate monthly anomalies relative to climatology
3. Visualize:

   a. Time series of anomalies with a horizontal zero line
   b. Heatmap of monthly anomalies (months × years)
   c. Map of mean annual anomaly
   d. Box plot comparing anomalies by season

=== Expected Output

A 2x2 figure showing all four visualizations with:
- Red/blue color scale for positive/negative anomalies
- Clear labeling of El Niño / La Niña periods
- Seasonal aggregation in the box plot

=== Hints

```python
# Compute climatology
clim = precip.groupby('time.month').mean('time')

# Compute anomaly
anomaly = precip.groupby('time.month') - clim
```

== Project 3: Interactive Data Explorer

=== Objective

Build an interactive widget-based dashboard for exploring CHIRPS data.

=== Requirements

1. Dropdown to select date
2. Slider to control map opacity
3. Dropdown to select color palette
4. Button to toggle coastlines/features
5. Interactive map with click-to-inspect

=== Tools

```python
import ipywidgets as widgets
from IPython.display import display

@widgets.interact
def explore(date=widgets.DatePicker(...),
            cmap=['Blues', 'RdBu', 'viridis', 'plasma'],
            opacity=(0.1, 1.0, 0.1),
            show_coastlines=True):
    # Replot with selected parameters
    pass
```

=== Expected Output

A Jupyter Notebook cell with interactive controls that update the map in real-time.

== Project Rubric

| *Criteria* | *Excellent (10)* | *Good (7)* | *Needs Work (4)* |
|---|---|---|---|
| Data handling | Efficient loading, cleaning, transformation | Basic loading, some cleaning | Manual or incorrect processing |
| Visual design | Professional, consistent, accessible | Good, minor inconsistencies | Default styles, poor choices |
| Code quality | Well-structured, reusable functions | Organized but not modular | Single monolithic script |
| Publication readiness | 300 DPI, vector format, proper fonts | Good but minor issues | Low resolution, missing labels |
| Innovation | Goes beyond requirements | Meets all requirements | Missing some elements |

== Tips for All Projects

1. *Start simple*: Get a working version first, then refine
2. *Plan the layout*: Sketch your figure before coding
3. *Use functions*: Each panel should be a separate function
4. *Save early, save often*: Incremental backups of your work
5. *Document*: Add comments explaining your design choices

== Summary

These three projects consolidate everything you have learned: basic to advanced plotting, geographic visualization, time series analysis, interactivity, and publication-quality design. Choose one or complete all three to build your portfolio. In the next chapter, we present the capstone project.


