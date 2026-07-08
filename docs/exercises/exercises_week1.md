---
title: Week 1 Exercises
---

# Week 1 Exercises

These exercises cover Modules 1–4 of the Matplotlib Training Course.

---

## Exercise 1.1: Basic Line Plot

Create a line plot of the function $y = x^3 - 3x^2 + 2x + 1$ over the range $[-2, 3]$.

**Requirements:**
- Use the object-oriented API
- 100 evenly spaced points
- Blue solid line, 2 pt width
- Label axes and add a title
- Add a light grid

```python
# Your code here
```

---

## Exercise 1.2: Multiple Curves

Plot the following three functions on the same axes:

- $y_1 = \sin(x)$ in red
- $y_2 = \cos(x)$ in blue, dashed
- $y_3 = \sin(x) \cdot \cos(x)$ in green, dotted

**Requirements:**
- Range $[0, 4\pi]$
- Legend identifying each curve
- Axis labels and title
- Save the figure as `curves.png` at 150 DPI

```python
# Your code here
```

---

## Exercise 1.3: Scatter Plot Matrix

Generate 200 random 3D points and create a 3×3 scatter plot matrix.

**Requirements:**
- NumPy random seed 42
- Each off-diagonal shows a scatter plot
- Diagonal shows a histogram
- Shared axes for row/column alignment

:::{tip}
Use `plt.subplots(3, 3, sharex='col', sharey='row')` and iterate.
:::

```python
# Your code here
```

---

## Exercise 1.4: Bar Chart with Error Bars

Create a bar chart showing mean monthly rainfall for your city.

**Requirements:**
- 12 months (Jan–Dec)
- Error bars showing standard deviation
- Color bars by season (DJF, MAM, JJA, SON)
- Value labels on top of bars

```python
# Your code here
```

---

## Exercise 1.5: Histogram and KDE

Generate 1000 random samples from a normal distribution ($\mu=5$, $\sigma=2$) and plot:

1. A histogram with 30 bins, density=True
2. Overlay the theoretical normal PDF as a red line
3. Add a second histogram from a uniform distribution [0, 10] for comparison

```python
# Your code here
```

---

## Exercise 1.6: Customizing Colormaps

Create a 2D color plot (pcolormesh) of the function $z = \sin(x) \cdot \cos(y)$.

**Requirements:**
- Grid from $[-\pi, \pi]$ in both dimensions
- Use the `'RdBu_r'` colormap
- Add a colorbar
- Contour lines overlaid in black at 10 levels

```python
# Your code here
```

---

## Exercise 1.7: Figure Composition

Recreate this figure composition:

```
+-------------------+-------------------+
|                   |                   |
|    Line Plot      |   Scatter Plot    |
|                   |                   |
+-------------------+-------------------+
|                   |                   |
|    Bar Chart      |   Histogram       |
|                   |                   |
+-------------------+-------------------+
```

**Requirements:**
- 2×2 subplot layout, figsize=(12, 10)
- Different random data in each
- Shared y-axis for left column, shared x-axis for bottom row
- Suptitle "Week 1 Dashboard"

```python
# Your code here
```
