---
title: Module 6 — Styling Plots
---

# Module 6: Styling Plots

Transform functional plots into publication-ready graphics through colours, markers, line styles, fonts, legends, and style sheets.

---

## Learning Objectives

- Use named colours, hex codes, RGB tuples, and colormaps
- Customise markers and line styles
- Control fonts, labels, and legends
- Apply built-in style sheets
- Create consistent, professional-looking figures

---

## Colours

Matplotlib supports multiple colour specifications:

```python
# Named colour
ax.plot(x, y, color='firebrick')

# Hex code
ax.plot(x, y, color='#1f77b4')

# RGB tuple
ax.plot(x, y, color=(0.2, 0.6, 0.4))

# Colormap
scatter = ax.scatter(x, y, c=values, cmap='viridis')
```

---

## Markers and Line Styles

```python
ax.plot(x, y, marker='o', markersize=8, markerfacecolor='gold',
        markeredgecolor='darkgoldenrod', linewidth=2,
        linestyle='--', color='steelblue')
```

Common markers: 'o', 's', '^', 'D', '*', 'x', '.', 'p'

Common line styles: '-' solid, '--' dashed, ':' dotted, '-.' dash-dot

---

## Style Sheets

```python
plt.style.use('seaborn-v0_8')
plt.style.use('ggplot')
plt.style.use('dark_background')
plt.style.use('fivethirtyeight')

# Temporary style
with plt.style.context('ggplot'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```

---

## Fonts

```python
fig, ax = plt.subplots()
ax.set_title('Title', fontfamily='serif', fontsize=14, fontweight='bold')
ax.set_xlabel('X Axis', fontfamily='sans-serif', fontsize=11)
ax.set_ylabel('Y Axis', fontstyle='italic')
```

---

## Exercises

1. Create a plot with custom colours and markers for the CHIRPS climatology
2. Apply the 'seaborn-v0_8' style to a multi-panel figure
3. Create a custom legend with Patch objects
4. Build a publication-ready plot with serif fonts and custom gridlines

---

## Next Steps

Proceed to {doc}`module07` to learn axes customisation.
