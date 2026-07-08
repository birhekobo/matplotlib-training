---
title: Week 3 Exercises
---

# Week 3 Exercises

These exercises cover Modules 9-12 of the Matplotlib Training Course.

---

## Exercise 3.1: Box Plot by Month

Create a box plot showing the monthly rainfall distribution for Addis Ababa.

**Requirements:**
- 12 box plots (one per month)
- Use the full CHIRPS dataset
- Colour boxes using the viridis colormap
- Add a grid, labels, and title

```python
# Your code here
```

---

## Exercise 3.2: Trend Analysis with Confidence Intervals

Analyse the annual rainfall trend at a location in Ethiopia.

**Requirements:**
- Aggregate monthly rainfall to annual totals
- Fit a linear regression using `scipy.stats.linregress`
- Plot the data points, trend line, and 95% confidence band
- Display the trend slope and p-value in the legend

```python
# Your code here
```

---

## Exercise 3.3: Correlation Heatmap

Create a correlation heatmap of rainfall between multiple Ethiopian cities.

**Requirements:**
- Extract time series for 6 cities
- Compute the correlation matrix
- Use seaborn heatmap with RdBu_r colormap
- Annotate cells with correlation values

```python
# Your code here
```

---

## Exercise 3.4: Contour Map

Create a filled contour map of CHIRPS rainfall.

**Requirements:**
- Use `contourf` with 20 levels
- Add contour lines with `contour` in black
- Label contour lines
- Use an appropriate colormap

```python
# Your code here
```

---

## Exercise 3.5: Global Map with Cartopy

Create a global precipitation map using Cartopy with a Robinson projection.

**Requirements:**
- Use `ccrs.Robinson()` projection
- Add coastlines and borders
- Colour mesh of precipitation data
- Add gridlines with labels
- Add a colour bar

```python
# Your code here
```

---

## Exercise 3.6: Rolling Statistics

Compute and visualise rolling statistics for the CHIRPS time series.

**Requirements:**
- 12-month rolling mean
- 12-month rolling standard deviation
- Plot original data, rolling mean, and fill between mean+/-std
- Export the figure at 300 DPI

```python
# Your code here
```
