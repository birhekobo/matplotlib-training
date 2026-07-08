---
title: Module 7 — Axes Customisation
---

# Module 7: Axes Customisation

Fine-tune every aspect of your plot axes: limits, ticks, scales, secondary axes, aspect ratios, and spines.

---

## Learning Objectives

- Control axis limits and scales
- Customise tick locators and formatters
- Create logarithmic scales
- Add secondary axes (twinx / twiny)
- Manage aspect ratios
- Style spines and borders

---

## Axis Limits

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlim(0, 100)       # Zoom x-axis
ax.set_ylim(0, 50)        # Zoom y-axis
```

---

## Tick Locators and Formatters

```python
from matplotlib.ticker import LinearLocator, FormatStrFormatter

ax.yaxis.set_major_locator(MultipleLocator(50))
ax.yaxis.set_minor_locator(MultipleLocator(10))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f mm'))
```

---

## Logarithmic Scale

```python
ax.set_yscale('log')
ax.set_xscale('log')
# or
ax.semilogy(x, y)
ax.loglog(x, y)
```

---

## Secondary Axes

```python
ax2 = ax.twinx()                    # Shared x, independent y
ax2.plot(x, y2, color='darkorange')
ax2.set_ylabel('Alternative Unit')

ax3 = ax.secondary_yaxis('right', functions=(mm_to_inches, inches_to_mm))
```

---

## Spines

```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10))
ax.spines['bottom'].set_color('steelblue')
```

---

## Exercises

1. Create a plot with ticks every 25 mm and minor ticks every 5 mm
2. Add a secondary y-axis converting mm to inches
3. Use a log scale for a histogram of CHIRPS data
4. Create a polished plot with offset spines and no top/right borders

---

## Next Steps

Proceed to {doc}`module08` to learn about multiple plots and layouts.
