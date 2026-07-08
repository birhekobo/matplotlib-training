---
title: Module 1 — Introduction to Visualization
---

# Module 1: Introduction to Visualization

Welcome to the Matplotlib Training Course! This module introduces the fundamental principles of data visualization and sets the stage for the hands-on modules ahead.

---

## Why Data Visualization?

Data visualization is the graphical representation of information and data. It leverages the human visual system to detect patterns, trends, and outliers that would remain hidden in raw tabular data.

> {octicon}`quote` *"The greatest value of a picture is when it forces us to notice what we never expected to see."* — John Tukey

### Why Matplotlib?

- **Mature ecosystem**: First released in 2003 by John D. Hunter
- **Unmatched flexibility**: Control every element of a figure
- **Publication quality**: Output at 600+ DPI, vector formats (PDF/SVG)
- **Ecosystem integration**: Works seamlessly with NumPy, Pandas, xarray, Cartopy
- **Large community**: Extensive documentation, StackOverflow presence, active development

---

## Key Concepts

### Data — Ink Ratio

Introduced by Edward Tufte, this ratio measures the proportion of a graphic's ink devoted to displaying data versus decorative elements. **Maximize the data-ink ratio** by removing:

- Redundant grid lines
- 3D effects on 2D data
- Excessive labels
- Decorative gradients

### Pre-attentive Processing

The human brain processes certain visual properties almost instantly (< 250 ms):

- Position
- Size
- Color hue
- Color intensity
- Orientation
- Shape
- Movement

Use these attributes to guide the viewer's attention.

### Chart Type Selection

| Goal | Recommended Chart |
|------|-------------------|
| Compare categories | Bar chart |
| Show trends over time | Line chart |
| Distribution | Histogram / Box plot |
| Relationship | Scatter plot |
| Composition | Stacked bar / Pie chart (use sparingly) |
| Geographic | Choropleth / Contour map |

---

## Code Snippets

### Your First Matplotlib Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, color="steelblue", linewidth=2)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Sine Wave")
ax.grid(alpha=0.3)
plt.show()
```

### The Object-Oriented vs. Pyplot API

```python
# Pyplot style (quick, interactive)
plt.plot(x, y)
plt.xlabel("x")

# Object-oriented style (recommended for production)
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
```

:::{note}
Always prefer the **object-oriented API** for production code and complex figures. It gives you explicit control over each figure element.
:::

---

## References

- Tufte, E. (2001). *The Visual Display of Quantitative Information*. Graphics Press.
- Cairo, A. (2012). *The Functional Art: An Introduction to Information Graphics and Visualization*. New Riders.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*. O'Reilly Media.
- [Matplotlib Documentation](https://matplotlib.org/stable/users/index)

---

## Next Steps

Proceed to {doc}`module02` to set up your development environment.
