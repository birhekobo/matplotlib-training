#import "../macros.typ": note-box, warning-box, info-box
= Styling and Customization

A well-styled plot communicates more effectively than a default one. This chapter covers how to customize colors, fonts, styles, and create a consistent visual identity.

== Matplotlib Style System

Matplotlib provides built-in styles that change the default appearance of all elements:

```python
# List available styles
print(plt.style.available)

# Apply a style
plt.style.use('seaborn-v0_8-whitegrid')

# Or use a context manager for temporary styling
with plt.style.context('ggplot'):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```

=== Popular Built-in Styles

| *Style* | *Best For* |
|---|---|
| `default` | Matplotlib default |
| `seaborn-v0_8-whitegrid` | Statistical plots, clean look |
| `seaborn-v0_8-darkgrid` | Dark background presentations |
| `ggplot` | R ggplot2-inspired look |
| `fivethirtyeight` | Data journalism |
| `bmh` | Bayesian Methods for Hackers |
| `classic` | Pre-v2.0 Matplotlib |
| `fast` | Performance-optimized |

#note-box[
  Use `plt.style.use('seaborn-v0_8-whitegrid')` as a good starting point for most data visualization work. It provides clean grids and sensible defaults.
]

== Customizing rcParams

`rcParams` is Matplotlib's configuration system, with hundreds of parameters:

```python
import matplotlib as mpl

# Universal settings
mpl.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'figure.dpi': 120,
    'figure.figsize': (8, 5),
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'axes.linewidth': 1.0,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'lines.linewidth': 2,
    'grid.alpha': 0.3,
})
```

=== Important rcParams Categories

| *Category* | *Example Parameters* |
|---|---|
| `font.*` | family, size, weight |
| `figure.*` | dpi, figsize, facecolor |
| `axes.*` | titlesize, labelsize, linewidth |
| `xtick.*`, `ytick.*` | labelsize, color, direction |
| `lines.*` | linewidth, linestyle, marker |
| `legend.*` | fontsize, frameon, loc |
| `grid.*` | alpha, color, linestyle |
| `savefig.*` | dpi, bbox, format |

== Color Palettes

=== Sequential Palettes

For data ordered from low to high (precipitation, temperature, elevation):

```python
cmap = plt.cm.Blues        # Single-hue
cmap = plt.cm.YlOrRd       # Multi-hue
cmap = plt.cm.viridis      # Perceptually uniform
cmap = plt.cm.plasma       # Perceptually uniform
cmap = plt.cm.inferno      # Perceptually uniform
cmap = plt.cm.cividis      # Colorblind-friendly
```

=== Diverging Palettes

For data with a meaningful midpoint (anomalies, differences):

```python
cmap = plt.cm.RdBu
cmap = plt.cm.RdYlBu
cmap = plt.cm.coolwarm
cmap = plt.cm.PiYG
```

=== Qualitative Palettes

For categorical data:

```python
colors = plt.cm.tab10.colors       # 10 distinct colors
colors = plt.cm.Set2.colors        # 8 soft colors
colors = plt.cm.Paired.colors      # 12 paired colors
```

=== Custom Colormap

```python
from matplotlib.colors import LinearSegmentedColormap

colors = ['#313695', '#4575b4', '#74add1', '#abd9e9',
          '#fee090', '#fdae61', '#f46d43', '#d73027']
cmap = LinearSegmentedColormap.from_list('custom_blues', colors)
```

== Font Customization

```python
# Specify font family
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'DejaVu Sans']

# For publications, use serif fonts
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Libertinus Serif']

# LaTeX-style math fonts
plt.rcParams['mathtext.fontset'] = 'stix'  # Also: 'cm', 'dejavusans'
```

== Customizing Grid, Spines, and Ticks

=== Grid Lines

```python
# Major grid only
ax.grid(True, which='major', alpha=0.3, linestyle='-')

# Both major and minor
ax.grid(True, which='both', alpha=0.2)
ax.minorticks_on()
```

=== Spines

```python
# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Move spine position
ax.spines['left'].set_position(('outward', 10))

# Customize spine appearance
ax.spines['bottom'].set_color('#333333')
ax.spines['bottom'].set_linewidth(1.5)
```

=== Ticks

```python
# Set tick locations
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])

# Tick direction (in, out, inout)
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# Tick length and width
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.major.width'] = 1
```

== Complete Example: Publication-Ready Style

```python
import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('default')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.figsize': (7, 4),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.linewidth': 1,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'lines.linewidth': 1.5,
})

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Publication-Ready Plot')
ax.legend(frameon=True, fancybox=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()
```

== Summary

You learned how to customize every aspect of a Matplotlib figure: from high-level style sheets to individual rcParams, colors, fonts, grids, spines, and ticks. Consistent styling is key to professional-looking publications. In the next chapter, we focus on advanced axes customization.








