---
title: Module 4 — Matplotlib Basics
---

# Module 4: Matplotlib Basics

This module covers the fundamental building blocks of Matplotlib: figures, axes, and the plotting pipeline.

---

## Learning Objectives

- Understand the Matplotlib architecture (Figure, Axes, Artist)
- Create figures and axes explicitly
- Use basic plotting functions (`plot`, `scatter`, `bar`, `hist`)
- Customize colors, line styles, and markers
- Add labels, titles, legends, and annotations
- Save figures in various formats

---

## Matplotlib Architecture

Matplotlib has three layers:

1. **Figure** — The top-level container holding all elements
2. **Axes** — The plotting area with data coordinates
3. **Artist** — Everything you see on the plot (lines, labels, etc.)

```python
import matplotlib.pyplot as plt

# Create a Figure and an Axes
fig, ax = plt.subplots(figsize=(8, 4))

# ax is the plotting area; all plotting is done on it
ax.plot([0, 1, 2], [0, 1, 4], label="quadratic")
ax.legend()
```

:::{note}
Think of `fig` as the canvas and `ax` as the easel. You can have multiple easels (subplots) on one canvas.
:::

---

## Core Plotting Functions

### Line Plot

```python
x = [0, 1, 2, 3, 4]
y = [0, 2, 4, 6, 8]

fig, ax = plt.subplots()
ax.plot(x, y, color='#1f77b4', linestyle='--', linewidth=2, marker='o')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_title('Line Plot Example')
```

### Scatter Plot

```python
import numpy as np
np.random.seed(42)
x = np.random.randn(100)
y = np.random.randn(100)
colors = np.random.rand(100)
sizes = np.random.randint(20, 200, 100)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
fig.colorbar(scatter, ax=ax, label='Color scale')
ax.set_title('Scatter Plot')
```

### Bar Chart

```python
categories = ['A', 'B', 'C', 'D']
values = [3, 7, 2, 5]
colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a']

fig, ax = plt.subplots()
bars = ax.bar(categories, values, color=colors, edgecolor='black', width=0.6)
ax.bar_label(bars, padding=3)
ax.set_ylabel('Values')
ax.set_title('Bar Chart')
```

### Histogram

```python
data = np.random.randn(1000)

fig, ax = plt.subplots()
ax.hist(data, bins=30, density=True, alpha=0.7,
        color='steelblue', edgecolor='white')
ax.set_xlabel('Value')
ax.set_ylabel('Density')
ax.set_title('Histogram')
```

---

## Customization

### Colors

```python
# Named colors
ax.plot(x, y, color='red')

# Hex codes
ax.plot(x, y, color='#ff5733')

# RGB tuples
ax.plot(x, y, color=(0.3, 0.7, 0.2))

# Colormaps
ax.scatter(x, y, c=z, cmap='plasma')
```

### Line Styles and Markers

```python
ax.plot(x, y,
        linestyle='--',        # '-', '--', '-.', ':', ''
        linewidth=2,
        marker='o',            # 'o', 's', '^', 'D', '*', '.'
        markersize=8,
        markerfacecolor='white',
        markeredgecolor='black')
```

### Labels and Titles

```python
ax.set_xlabel('Time (s)', fontsize=12, fontweight='bold')
ax.set_ylabel('Amplitude', fontsize=12)
ax.set_title('Signal Analysis', fontsize=14, pad=15)

# Legend
ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
```

---

## Saving Figures

```python
fig.savefig('figure.png', dpi=150, bbox_inches='tight')
fig.savefig('figure.pdf', dpi=300)
fig.savefig('figure.svg')
```

| Format | Use Case |
|--------|----------|
| PNG | Web, presentations |
| PDF | Publications, printing |
| SVG | Web (scalable), editing |
| EPS | LaTeX documents |

:::{warning}
Always use `bbox_inches='tight'` to avoid clipped labels when saving.
:::

---

## Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.linspace(0, 4 * np.pi, 200)
y1 = np.sin(x)
y2 = np.cos(x)

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 5))

# Plot
ax.plot(x, y1, label='sin(x)', color='#d62728', linewidth=2)
ax.plot(x, y2, label='cos(x)', color='#1f77b4', linewidth=2, linestyle='--')

# Labels
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_title('Sine and Cosine Waves', fontsize=14)

# Grid and legend
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

# Annotations
ax.annotate('sin(π) = 0', xy=(np.pi, 0), xytext=(np.pi + 0.5, 0.5),
            arrowprops=dict(arrowstyle='->', color='gray'))

plt.tight_layout()
plt.show()
```

---

## Exercises

1. Create a plot of $f(x) = x^2$ with labeled axes and a title
2. Make a scatter plot of 50 random points with varying sizes and colors
3. Create a horizontal bar chart of 5 categories
4. Save a figure as PDF with 300 DPI

---

## Next Steps

Proceed to {doc}`module05` to learn basic chart types.
