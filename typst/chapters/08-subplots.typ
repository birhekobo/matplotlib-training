#import "../macros.typ": note-box, warning-box, info-box
= Multiple Plots and Subplots

Real-world visualizations often require multiple plots in a single figure. This chapter covers subplot layouts, insets, and grid specifications.

== Basic Subplots

=== Regular Grids

```python
# 2 rows, 3 columns
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# Access by index
axes[0, 0].plot(x, y)   # Row 0, Column 0
axes[1, 2].scatter(x, z) # Row 1, Column 2
```

=== Shared Axes

```python
# Share x-axis across columns, y-axis across rows
fig, axes = plt.subplots(2, 2, figsize=(10, 8),
                         sharex='col', sharey='row')

# Share with specific axes
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)

# No sharing
fig, axes = plt.subplots(2, 2)
```

#note-box[
  Shared axes make comparisons easier and save space by reducing repeated labels. Use `sharex='col'` to share within columns and `sharey='row'` to share within rows.
]

== GridSpec: Advanced Layouts

`GridSpec` provides fine-grained control over subplot placement, including spanning multiple cells.

```python
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(3, 3, figure=fig,
                       hspace=0.3, wspace=0.3)

ax1 = fig.add_subplot(gs[0, :])    # Top row, full width
ax2 = fig.add_subplot(gs[1, 0])    # Middle left
ax3 = fig.add_subplot(gs[1, 1:])   # Middle right (2 cols)
ax4 = fig.add_subplot(gs[2, :2])   # Bottom left (2 cols)
ax5 = fig.add_subplot(gs[2, 2])    # Bottom right

# Layout:
# +--------------------+
# |        ax1         |
# +---------+----------+
# |   ax2   |   ax3    |
# +---------+----------+
# |     ax4      | ax5 |
# +--------------+-----+
```

=== Unequal Widths and Heights

```python
gs = gridspec.GridSpec(2, 2, figure=fig,
                       width_ratios=[2, 1],
                       height_ratios=[1, 2])
```

== Nested GridSpec

Combine multiple GridSpec objects for complex layouts:

```python
fig = plt.figure(figsize=(12, 8))
outer_gs = gridspec.GridSpec(2, 2, figure=fig)

# Top-left cell has a nested 2x1 grid
inner_gs = gridspec.GridSpecFromSubplotSpec(2, 1,
    subplot_spec=outer_gs[0, 0])

ax1 = fig.add_subplot(inner_gs[0])
ax2 = fig.add_subplot(inner_gs[1])
ax3 = fig.add_subplot(outer_gs[0, 1])
ax4 = fig.add_subplot(outer_gs[1, :])
```

== Subplot Spacing

```python
# Automatic spacing
plt.tight_layout()

# Explicit spacing
plt.subplots_adjust(left=0.1, right=0.95,
                    bottom=0.1, top=0.95,
                    wspace=0.25, hspace=0.3)

# Constrained layout (newer, preferred)
fig, axes = plt.subplots(2, 2, layout='constrained')
# Or:
fig.set_layout_engine('constrained')
```

#info-box[
  `layout='constrained'` (Matplotlib 3.6+) is the recommended approach for modern code. It handles colorbars, legends, and labels automatically better than `tight_layout`.
]

== Inset Axes

Place a smaller axes inside another axes:

```python
fig, ax = plt.subplots(figsize=(8, 5))

# Main plot
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=2)
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')

# Inset axes
ax_inset = ax.inset_axes([0.6, 0.6, 0.35, 0.35])
ax_inset.plot(x, np.sin(x), color='#d62728')
ax_inset.set_xlim(4.5, 5.5)
ax_inset.set_ylim(-1.05, -0.85)
ax_inset.set_title('Zoomed region', fontsize=10)
ax_inset.grid(alpha=0.3)

# Mark the zoom region on main plot
ax.indicate_inset_zoom(ax_inset, edgecolor='#d62728')
plt.show()
```

== Creating Small Multiples (Faceting)

Small multiples show the same chart type across different data subsets:

```python
categories = ['A', 'B', 'C', 'D']
months = ['Jan', 'Feb', 'Mar']

data = np.random.rand(4, 3)  # categories × months

fig, axes = plt.subplots(2, 2, figsize=(10, 8),
                         sharex=True, sharey=True)

for ax, category, values in zip(axes.flat, categories, data):
    ax.bar(months, values, color='steelblue')
    ax.set_title(f'Category {category}')
    ax.set_ylabel('Value')
    ax.grid(axis='y', alpha=0.3)

fig.suptitle('Small Multiples: Monthly Values by Category',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

== Removing Unused Axes

When creating grids with fewer plots than grid cells:

```python
fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# Hide the last axes
axes[1, 2].set_visible(False)

# Or remove it completely
fig.delaxes(axes[1, 2])
```

== Summary

You can now create complex figure layouts with regular grids, spanning cells via GridSpec, nested subplots, and insets. These techniques are essential for multi-panel figures common in scientific publications. In the next chapter, we apply these skills to statistical visualization.







