#import "../macros.typ": note-box, warning-box, info-box
= Basic Chart Types

This chapter covers the fundamental chart types in Matplotlib: line plots, scatter plots, bar charts, histograms, and more. Each section shows the use case and complete code example.

== Line Plots

Line plots are the most common chart type for showing trends over time or continuous relationships.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y1 = np.exp(-x/3) * np.sin(x * 2)
y2 = np.exp(-x/3) * np.cos(x * 2)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y1, label='Damped sin', color='#1f77b4', linewidth=2)
ax.plot(x, y2, label='Damped cos', color='#d62728', linewidth=2, linestyle='--')
ax.fill_between(x, y1, alpha=0.2, color='#1f77b4')
ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Amplitude', fontsize=12)
ax.set_title('Damped Oscillations', fontsize=14)
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

#note-box[
  Use `fill_between` to add visual weight to areas under curves. This is especially effective for confidence intervals or ranges.
]

== Scatter Plots

Scatter plots show the relationship between two variables. They can encode up to five dimensions: x, y, color, size, and marker style.

```python
np.random.seed(42)
n = 200
x = np.random.randn(n)
y = x * 0.5 + np.random.randn(n) * 0.3
colors = np.random.rand(n)
sizes = np.random.randint(20, 300, n)

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.7,
                     cmap='viridis', edgecolors='black', linewidth=0.5)
cbar = fig.colorbar(scatter, ax=ax, label='Color scale')
ax.set_xlabel('Variable X', fontsize=12)
ax.set_ylabel('Variable Y', fontsize=12)
ax.set_title('Scatter Plot with Encoded Dimensions', fontsize=14)
ax.grid(alpha=0.3)
plt.show()
```

=== Scatter vs. Plot with Markers

```python
# Use plot() for connected markers
ax.plot(x, y, 'o-')   # Lines + markers

# Use scatter() for unconnected markers with variable properties
ax.scatter(x, y, c=z, s=size)  # Variable color and size
```

== Bar Charts

Bar charts are ideal for comparing values across categories.

```python
categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
values = [120, 95, 110, 85, 130, 105]
errors = [8, 6, 7, 5, 9, 7]

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(categories, values, yerr=errors,
              color='#2c7bb6', edgecolor='black',
              capsize=5, width=0.6)
ax.bar_label(bars, padding=3, fmt='%.0f')
ax.set_ylabel('Rainfall (mm)', fontsize=12)
ax.set_title('Monthly Rainfall Totals', fontsize=14)
ax.grid(axis='y', alpha=0.3)
plt.show()
```

=== Horizontal Bar Chart

```python
ax.barh(categories, values, xerr=errors, color='#d7191c')
ax.set_xlabel('Rainfall (mm)')
```

== Histograms

Histograms show the distribution of a single variable.

```python
data = np.random.gamma(shape=2, scale=2, size=1000)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(data, bins=40, density=True, alpha=0.7,
        color='steelblue', edgecolor='white', linewidth=0.5)

# Overlay KDE
from scipy import stats
x_kde = np.linspace(data.min(), data.max(), 200)
kde = stats.gaussian_kde(data)
ax.plot(x_kde, kde(x_kde), 'r-', linewidth=2, label='KDE')

ax.set_xlabel('Value', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Distribution with KDE Overlay', fontsize=14)
ax.legend()
ax.grid(axis='y', alpha=0.3)
plt.show()
```

=== Histogram Parameters

| *Parameter* | *Options* | *Effect* |
|---|---|---|
| `bins` | int or sequence | Number or edges of bins |
| `density` | True/False | Normalized to area = 1 |
| `cumulative` | True/False | Cumulative distribution |
| `histtype` | 'bar', 'step', 'stepfilled' | Visual style |
| `orientation` | 'vertical', 'horizontal' | Direction |

== Pie Charts (Use Sparingly)

```python
sizes = [35, 25, 20, 15, 5]
labels = ['Africa', 'Asia', 'Europe', 'Americas', 'Oceania']
explode = (0.05, 0, 0, 0, 0)

fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, autopct='%1.0f%%',
    explode=explode, startangle=90,
    colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
)
plt.show()
```

#warning-box[
  Pie charts are difficult to read when there are more than 4-5 categories. Consider bar charts or stacked bar charts instead for most applications.
]

== Stacked Bar and Area Charts

```python
categories = ['Q1', 'Q2', 'Q3', 'Q4']
product_a = [30, 45, 35, 50]
product_b = [20, 25, 30, 35]
product_c = [10, 15, 20, 25]

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(categories, product_a, label='Product A', color='#1f77b4')
ax.bar(categories, product_b, bottom=product_a, label='Product B', color='#ff7f0e')
ax.bar(categories, product_c, bottom=[a+b for a,b in zip(product_a, product_b)],
       label='Product C', color='#2ca02c')
ax.set_ylabel('Revenue', fontsize=12)
ax.set_title('Stacked Bar Chart', fontsize=14)
ax.legend()
plt.show()
```

== Summary

You have learned the most common chart types: line plots for trends, scatter plots for relationships, bar charts for comparison, histograms for distributions, and pie/stacked charts for composition. Each type has specific use cases and customization options. In the next chapter, we explore how to style and customize these charts in detail.








