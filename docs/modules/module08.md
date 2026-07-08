---
title: Module 8 — Multiple Plots and Layouts
---

# Module 8: Multiple Plots and Layouts

Combine multiple views of the same dataset in a single figure using subplots, GridSpec, inset axes, and twin axes.

---

## Learning Objectives

- Create basic subplot grids
- Use GridSpec for complex layouts
- Share axes across subplots
- Add inset plots for zoomed detail
- Manage figure layout with tight_layout and constrained_layout

---

## Basic Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0,0].plot(x, y)
axes[0,1].scatter(x, y)
axes[1,0].bar(categories, values)
axes[1,1].hist(data, bins=30)
```

---

## GridSpec

```python
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(3, 3, figure=fig, width_ratios=[2, 1, 1])

ax0 = fig.add_subplot(gs[0, :])    # Span full width
ax1 = fig.add_subplot(gs[1, 0])     # Single cell
ax2 = fig.add_subplot(gs[1, 1:])    # Span 2 columns
```

---

## Shared Axes

```python
fig, axes = plt.subplots(2, 1, sharex=True, sharey=True)
# Or: sharex='col', sharey='row' for mixed sharing
```

---

## Inset Plots

```python
ax_inset = ax.inset_axes([0.15, 0.55, 0.25, 0.35])
ax_inset.plot(x_subset, y_subset)
ax.indicate_inset_zoom(ax_inset, edgecolor='gray')
```

---

## Layout Management

```python
plt.tight_layout()
# or
fig, ax = plt.subplots(constrained_layout=True)
```

---

## Exercises

1. Create a 2x2 dashboard of CHIRPS analysis (map, time series, climatology, histogram)
2. Use GridSpec to create a layout with a wide top panel
3. Add an inset plot showing a zoomed region of the time series
4. Create a figure with shared axes showing multiple locations

---

## Next Steps

Proceed to {doc}`module09` to learn statistical visualisation.
