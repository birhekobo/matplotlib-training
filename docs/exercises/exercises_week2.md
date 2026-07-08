---
title: Week 2 Exercises
---

# Week 2 Exercises

These exercises cover Modules 5-8 of the Matplotlib Training Course.

---

## Exercise 2.1: Time Series with CHIRPS Data

Load the CHIRPS dataset and create a time series plot for Addis Ababa (9.025N, 38.725E).

**Requirements:**
- Use xarray to load `../chirps_1981_2022.nc`
- Extract the point nearest to Addis Ababa
- Plot the full time series as a line plot
- Add axis labels, title, and grid
- Use figsize=(14, 4)

```python
# Your code here
```

---

## Exercise 2.2: Multi-Panel Climatology Analysis

Create a 2x2 figure showing different aspects of the monthly climatology.

**Requirements:**
- Line plot of climatology with circle markers
- Bar chart of climatology with value labels
- Horizontal bar chart sorted by rainfall amount
- Stem plot of climatology values

```python
# Your code here
```

---

## Exercise 2.3: Styled Publication Plot

Create a publication-ready time series plot using the seaborn style.

**Requirements:**
- Use `plt.style.context('seaborn-v0_8')`
- Plot 10 years of CHIRPS data
- Add a filled area under the curve with alpha=0.3
- Add a horizontal line at the mean value with a label
- Custom legend, grid, and axis labels
- Export as PDF at 300 DPI

```python
# Your code here
```

---

## Exercise 2.4: GridSpec Layout

Create a complex layout using GridSpec with width and height ratios.

**Requirements:**
- 3 rows, 2 columns with width_ratios=[2, 1] and height_ratios=[1, 1, 1.5]
- Top row: time series spanning both columns
- Middle row: climatology bar chart and histogram
- Bottom row: map spanning both columns

```python
# Your code here
```

---

## Exercise 2.5: Inset Zoom

Create a time series with an inset plot showing a zoomed region.

**Requirements:**
- Full time series (1981-2022) as main plot
- Inset showing the 1997 El Nino year
- Connect the inset to the main plot with a rectangle
- Use `ax.indicate_inset_zoom()`

```python
# Your code here
```

---

## Exercise 2.6: Twin Axes

Create a plot with dual y-axes showing rainfall and coefficient of variation.

**Requirements:**
- Bar chart of monthly mean rainfall (left axis, blue)
- Line plot of coefficient of variation (right axis, red)
- Combined legend
- Proper axis colours and labels

```python
# Your code here
```
