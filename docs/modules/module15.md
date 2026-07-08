---
title: Module 15 — Publication-Quality Figures
---

# Module 15: Publication-Quality Figures

Create figures that meet the standards of scientific journals, reports, and presentations.

---

## Learning Objectives

- Configure figure size, DPI, and font settings for publication
- Use vector formats (PDF, SVG, EPS)
- Manage colour blindness accessible palettes
- Create multi-panel publication figures
- Export at appropriate resolutions

---

## Figure Configuration

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'figure.dpi': 300,
    'font.family': 'serif',
    'font.size': 10,
    'axes.linewidth': 0.8,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
})

fig, ax = plt.subplots(figsize=(6.4, 4.8))  # Standard journal size
```

---

## Colour Accessibility

```python
# Colour-blind friendly palettes
colors = ['#0077BB', '#EE7733', '#009988', '#CC3311']
# Use viridis / cividis / colorblind-friendly colormaps
```

---

## Saving Figures

```python
fig.savefig('figure.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figure.svg')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
```

---

## Exercises

1. Configure rcParams for a journal-style figure
2. Create a multi-panel figure with panel labels (a, b, c, d)
3. Export as PDF and SVG
4. Verify colour accessibility with a colour blindness simulator

---

## Next Steps

Proceed to {doc}`module16` for real-world projects.
