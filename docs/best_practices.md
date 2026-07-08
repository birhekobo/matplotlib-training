---
title: Best Practices Guide
---

# Best Practices Guide

Guidelines for creating publication-quality, accessible, and reproducible visualizations with Matplotlib.

---

## 1. Figure Sizing

### Publications

| Venue | Column Width | Figure Width | Aspect Ratio |
|-------|-------------|--------------|--------------|
| Single column (journal) | ~3.5 in (89 mm) | 3.2–3.5 in | 4:3 or 16:9 |
| Double column (journal) | ~7.2 in (183 mm) | 6.8–7.2 in | 2:1 or 5:3 |
| Presentation | Full slide | 10–12 in | 4:3 or 16:9 |
| Poster | Variable | 8–12 in | Varies |

```python
fig, ax = plt.subplots(figsize=(3.5, 2.625))  # Single column, 4:3
fig, ax = plt.subplots(figsize=(7.0, 3.5))    # Double column, 2:1
```

### Font Sizes

| Element | Single Column | Double Column |
|---------|---------------|---------------|
| Title | 10–11 pt | 11–12 pt |
| Axis labels | 9–10 pt | 10–11 pt |
| Tick labels | 8–9 pt | 9–10 pt |
| Legend | 8–9 pt | 9 pt |
| Annotation | 7–8 pt | 8–9 pt |

```python
plt.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
})
```

### Resolution

```python
fig.savefig('figure.png', dpi=300)        # Print publication
fig.savefig('figure.png', dpi=72)          # Web
fig.savefig('figure.pdf')                  # Vector for publication
fig.savefig('figure.svg')                  # Vector for web
```

:::{note}
Always use vector formats (PDF/SVG) for publications. Use PNG with 300+ DPI only when vector is not accepted.
:::

---

## 2. Color Palette Selection

### Sequential Palettes (ordered data)

```python
# Use when values go from low to high (e.g., precipitation)
cmap = plt.cm.Blues
cmap = plt.cm.YlOrRd
cmap = plt.cm.viridis     # Perceptually uniform
cmap = plt.cm.plasma      # Perceptually uniform
```

### Diverging Palettes (data with a meaningful midpoint)

```python
# Use for anomalies, differences (e.g., temperature anomalies)
cmap = plt.cm.RdBu
cmap = plt.cm.RdYlBu
cmap = plt.cm.coolwarm
```

### Qualitative Palettes (categorical data)

```python
# Use for distinct categories (e.g., land cover types)
colors = plt.cm.Set2.colors
colors = plt.cm.Paired.colors
colors = plt.cm.tab10.colors  # Default matplotlib
```

### ColorBrewer Reference

| Type | Palette | Best For |
|------|---------|----------|
| Sequential | Blues, Greens, Oranges, Purples | Ordered data |
| Qualitative | Set1, Set2, Set3, Pastel1 | Categories |
| Diverging | RdBu, RdYlBu, PuOr, PRGn | Anomalies |

### Accessibility

```python
# Use colorblind-friendly palettes
COLORBLIND_SAFE = {
    'blue': '#0077BB',
    'cyan': '#33BBEE',
    'teal': '#009988',
    'orange': '#EE7733',
    'red': '#CC3311',
    'magenta': '#EE3377',
    'grey': '#BBBBBB',
}

# Verify contrast: ensure text is legible against background
# Use perceptually uniform colormaps (viridis, plasma, inferno, magma)
```

:::{warning}
Avoid red-green combinations — approximately 8% of males have red-green color blindness. Use patterns, shapes, or redundant encoding when possible.
:::

---

## 3. Accessibility

### Color Vision Deficiency

- Use color + shape/pattern to encode information redundantly
- Avoid red-green comparisons
- Use perceptually uniform colormaps (`viridis`, `cividis`)
- Test with color blindness simulators

### Font and Contrast

- Minimum 9 pt font for annotation, 10 pt for body labels
- High contrast: black text on white background
- Avoid light gray text on white background
- Use `plt.style.use('seaborn-v0_8-whitegrid')` for accessible defaults

### Figure Readability

```python
# Good: high contrast, clear labels
ax.plot(x, y, color='black', linewidth=2, label='Signal')
ax.scatter(x, y, color='black', marker='o', s=20)

# Avoid: low contrast, small markers
ax.plot(x, y, color='#cccccc', linewidth=0.5, label='Signal')
```

---

## 4. Code Organization

### Recommended Structure

```python
# 1. Imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 2. Plotting parameters (at top of script)
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# 3. Data loading / generation
def load_data(path):
    """Load and preprocess data."""
    pass

# 4. Plotting functions
def create_figure(data, output_path):
    """Create and save a figure."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(...)
    fig.savefig(output_path)
    plt.close(fig)  # Important in scripts!
    return fig

# 5. Main execution
if __name__ == '__main__':
    data = load_data('data.csv')
    create_figure(data, 'output.png')
```

### Function Design

```python
def plot_timeseries(
    dates, values,
    title=None, xlabel='Date', ylabel='Value',
    color='#1f77b4', figsize=(10, 5),
    save_path=None
):
    """Create a publication-quality time series plot."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(dates, values, color=color, linewidth=1.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    return fig, ax
```

---

## 5. File Naming Conventions

### Figure Files

```
figure_descriptive_name.png
figure_comparison_method_a_vs_b.png
figure_YYYY_MM_DD_parameter.png
```

| Good | Bad |
|------|-----|
| `figure_precipitation_seasonal.png` | `fig1.png` |
| `figure_map_east_africa_chirps.pdf` | `MyFigure_v2_final.pdf` |
| `figure_comparison_method_abc.pdf` | `untitled.png` |

### Script and Notebook Files

```
01_data_loading.py
02_exploratory_analysis.ipynb
03_visualization_dashboard.py
04_report_figures.py
```

### Version Control

```text
project/
├── data/
│   ├── raw/           # Unprocessed data
│   └── processed/     # Cleaned/transformed data
├── figures/           # Generated visualizations
├── notebooks/         # Jupyter notebooks
├── scripts/           # Python scripts
├── report/           # Final report materials
└── requirements.txt   # Dependencies
```

---

## Summary Checklist

- [ ] Figure size matches publication venue
- [ ] Font sizes are legible (≥ 9 pt)
- [ ] Color palette is colorblind-friendly
- [ ] Redundant encoding (color + shape/pattern)
- [ ] Vector format for publication (PDF)
- [ ] `bbox_inches='tight'` on save
- [ ] Code follows standard structure
- [ ] File names are descriptive and consistent
- [ ] Data and figures are in organized directories
- [ ] Plot confirmed with `plt.close(fig)` to avoid memory leaks
