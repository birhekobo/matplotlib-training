#import "../macros.typ": note-box, warning-box, info-box
= Matplotlib Fundamentals

This chapter covers the core architecture of Matplotlib: how figures, axes, and artists work together, and how you create your first plots.

== The Matplotlib Architecture

Matplotlib has a three-layer architecture:

!TODO: [Figure showing the Matplotlib architecture]

=== Figure

The *Figure* is the top-level container that holds all plot elements. Think of it as the canvas. A figure can contain one or more axes.

```python
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8, 4))  # Creates a blank canvas
```

=== Axes

An *Axes* object is the actual plotting area with data coordinates. Despite the name, it represents a single plot (not multiple axes like in mathematics). Most plotting happens on axes objects.

```python
fig, ax = plt.subplots()  # Creates figure + one axes
ax.plot([1, 2, 3], [1, 4, 9])  # Plot on the axes
```

=== Artist

Everything visible in a figure is an *Artist*:

- Lines, markers, text, patches, images
- Even axes and figures are artists themselves

#note-box[
  Matplotlib's object-oriented API gives you explicit control. Compare:

  *Pyplot (implicit)*: `plt.plot(x, y)` — uses the "current" axes

  *OO API (explicit)*: `ax.plot(x, y)` — you specify the exact axes

  Use the OO API for all production code.
]

== Creating Figures and Axes

=== Method 1: subplots (Most Common)

```python
# Single plot
fig, ax = plt.subplots(figsize=(8, 4))

# Grid of plots
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
# axes[0, 0], axes[0, 1], ..., axes[1, 2]
```

=== Method 2: add_axes (Manual Placement)

```python
fig = plt.figure(figsize=(8, 4))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # [left, bottom, width, height]
```

=== Method 3: add_subplot (Grid Specification)

```python
fig = plt.figure(figsize=(8, 4))
ax1 = fig.add_subplot(2, 2, 1)  # Top-left
ax2 = fig.add_subplot(2, 2, 2)  # Top-right
ax3 = fig.add_subplot(2, 2, 3)  # Bottom-left (will span full width)
```

== Your First Plot

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 4))

# Plot
ax.plot(x, y, color='steelblue', linewidth=2)

# Labels
ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('Amplitude', fontsize=12)
ax.set_title('Sine Wave', fontsize=14)

# Grid
ax.grid(True, alpha=0.3)

# Display
plt.show()
```

== Understanding the Plotting Pipeline

Every Matplotlib plot follows the same pipeline:

1. *Prepare data*: Create or load your data (NumPy arrays, lists)
2. *Create figure*: Choose size and layout with `plt.subplots()`
3. *Plot data*: Call plotting methods on the axes object
4. *Customize*: Add labels, titles, legends, grid, colors
5. *Display or save*: `plt.show()` for interactive or `fig.savefig()` for files

== Basic Customization

=== Colors

```python
# Named colors
ax.plot(x, y, color='red')
ax.plot(x, y, color='darkblue')

# Hex codes
ax.plot(x, y, color='#ff5733')
ax.plot(x, y, color='#2c7bb6')

# RGB tuples (0–1 range)
ax.plot(x, y, color=(0.3, 0.7, 0.2))
```

=== Line Styles and Markers

```python
ax.plot(x, y,
        linestyle='--',       # '-', '--', '-.', ':', ''
        linewidth=2,
        marker='o',           # 'o', 's', '^', 'D', '*', 'x', '.'
        markersize=8,
        markerfacecolor='white',
        markeredgecolor='black',
        alpha=0.8)
```

=== Adding Multiple Lines

```python
x = np.linspace(0, 2*np.pi, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), label='sin(x)', color='#d62728')
ax.plot(x, np.cos(x), label='cos(x)', color='#1f77b4', linestyle='--')
ax.plot(x, np.sin(x) * np.cos(x), label='sin(x)cos(x)', color='#2ca02c', linestyle=':')
ax.legend()
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
```

== Saving Figures

```python
fig.savefig('figure.png', dpi=150, bbox_inches='tight')
fig.savefig('figure.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure.svg', bbox_inches='tight')
```

#warning-box[
  Always use `bbox_inches='tight'` when saving. This prevents labels and titles from being clipped at the figure boundaries.
]

== Summary

You now understand Matplotlib's core architecture: Figures are the container, Axes are the plotting area, and Artists are the visual elements. You can create basic plots with customized colors, line styles, labels, and titles. In the next chapter, we explore the full range of basic chart types.








