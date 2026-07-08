---
title: Module 5 — Basic Chart Types
---

# Module 5: Basic Chart Types

This module covers the fundamental chart types available in Matplotlib: line plots, scatter plots, bar charts, histograms, and more.

---

## Learning Objectives

- Create line plots for time series data
- Build scatter plots to explore relationships
- Use bar charts for categorical comparisons
- Generate histograms to understand distributions
- Create pie charts, stem plots, and step plots

---

## Line Plot

The most basic chart type — connects data points with straight line segments.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, color='steelblue', linewidth=1.5)
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
ax.set_title('Sine Wave')
ax.grid(True, alpha=0.3)
plt.show()
```

---

## Scatter Plot

Shows the relationship between two variables.

```python
np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(x, y, s=30, alpha=0.6, c='coral', edgecolor='black', linewidth=0.3)
ax.set_xlabel('X Variable')
ax.set_ylabel('Y Variable')
ax.set_title('Scatter Plot')
ax.grid(True, alpha=0.3)
plt.show()
```

---

## Bar Chart

```python
categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
values = [85, 92, 110, 130, 145, 160]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(categories, values, color='royalblue', edgecolor='navy')
ax.bar_label(bars, padding=3)
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Monthly Rainfall')
plt.show()
```

---

## Histogram

```python
data = np.random.gamma(2, 20, 1000)
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(data, bins=40, density=True, alpha=0.7, color='mediumseagreen', edgecolor='white')
ax.set_xlabel('Value')
ax.set_ylabel('Density')
ax.set_title('Histogram')
plt.show()
```

---

## Exercises

1. Create a line plot of 5 years of CHIRPS data at a location of your choice
2. Make a scatter plot comparing two Ethiopian cities' rainfall
3. Plot a monthly climatology as a bar chart with value labels
4. Create a 2x2 figure with four different chart types

---

## Next Steps

Proceed to {doc}`module06` to learn about styling plots.
