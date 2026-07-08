#import "../macros.typ": note-box, warning-box, info-box
= Publication-Quality Figures

This chapter consolidates best practices for creating figures that meet the standards of academic journals, conference proceedings, and professional reports.

== Journal Requirements

=== Common Journal Specifications

| *Journal / Venue* | *Column Width* | *Figure Width* | *Format* | *DPI* |
|---|---|---|---|---|
| Nature / Science | Single: 89 mm (3.5 in) | 89 mm | EPS/PDF | 300+ |
| | Double: 183 mm (7.2 in) | 183 mm | | |
| AGU (JGR, GRL) | 3.5 in or 7.2 in | As specified | PDF/EPS | 300 |
| IEEE | 3.5 in (88.9 mm) | 3.5 in | EPS/PDF | 600 |
| AMS (BAMS, JCLI) | 3.375 in (85.7 mm) | 3.375 in | EPS/TIFF | 300 |
| Springer | 122 mm (4.8 in) | 122 mm | EPS/TIFF | 300 |

=== Figure Preparation Checklist

- [ ] Correct dimensions for target journal
- [ ] Vector format (PDF/EPS) preferred
- [ ] 300+ DPI if raster format must be used
- [ ] Font sizes meet journal minimum (typically 6-8 pt minimum)
- [ ] All text is editable (no outlined fonts)
- [ ] Color figures are RGB or CMYK as required
- [ ] Resolution: fine lines and text are sharp
- [ ] All panels are labeled (A, B, C, etc.)

== Font Configuration for Publications

```python
import matplotlib.pyplot as plt
import matplotlib as mpl

# Journal-quality font settings
mpl.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Libertinus Serif'],
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.format': 'pdf',
    'savefig.bbox': 'tight',
    'font.mathfontset': 'stix',
})

# Or use LaTeX for exact journal font matching
mpl.rcParams['text.usetex'] = True  # Requires LaTeX installation
```

== Single vs. Double Column

=== Single Column Figure

```python
fig, ax = plt.subplots(figsize=(3.5, 2.625))  # 4:3 ratio
ax.plot(x, y)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Signal')
fig.savefig('figure_single.pdf')
```

=== Double Column Figure

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
ax1.plot(x, y)
ax2.scatter(x, z)
fig.savefig('figure_double.pdf')
```

#note-box[
  Many journals allow figures to be single or double column width. Design your figure for the width, keeping text at legible sizes.
]

== Resolution and Format

```python
# Vector format (always preferred)
fig.savefig('figure.pdf')
fig.savefig('figure.eps')

# High-resolution raster
fig.savefig('figure.tiff', dpi=600, compressed=True)
fig.savefig('figure.png', dpi=300)

# For web/online supplemental
fig.savefig('figure.png', dpi=150)
```

=== Understanding DPI

| *DPI* | *Use Case* | *Pixel Size (3.5 in)* |
|---|---|---|
| 72 | Web, screen viewing | 252 × 189 |
| 150 | Presentations | 525 × 394 |
| 300 | Print publication | 1050 × 788 |
| 600 | High-end printing | 2100 × 1575 |
| 1200 | Archival quality | 4200 × 3150 |

== Multi-Panel Figure Labeling

```python
fig, axes = plt.subplots(2, 2, figsize=(7.2, 6))
panel_labels = ['(a)', '(b)', '(c)', '(d)']

for ax, label in zip(axes.flat, panel_labels):
    ax.plot(x, y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    # Add panel label
    ax.text(-0.1, 1.1, label, transform=ax.transAxes,
            fontsize=10, fontweight='bold', va='top', ha='right')

plt.tight_layout()
```

== Color Considerations

=== Converting for Print

```python
# Grayscale conversion test
fig, ax = plt.subplots()
line1 = ax.plot(x, y1, color='#1f77b4', linewidth=2, label='Series 1')
line2 = ax.plot(x, y2, color='#ff7f0e', linewidth=2, label='Series 2')
# Check that lines are distinguishable in grayscale
```

=== Checking Color Accessibility

```python
# Use colorblind-friendly palettes
COLORS_CB = {
    'blue': '#0077BB',
    'cyan': '#33BBEE',
    'teal': '#009988',
    'orange': '#EE7733',
    'red': '#CC3311',
    'magenta': '#EE3377',
    'grey': '#BBBBBB',
}

# Ensure all lines use different markers as well
ax.plot(x, y1, color=COLORS_CB['blue'], marker='o', label='Signal A')
ax.plot(x, y2, color=COLORS_CB['orange'], marker='s', label='Signal B')
```

== Figure Checklist

Run this before submission:

```python
def check_figure_quality(fig, filename):
    """Print quality metrics for a figure."""
    import os
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    size_kb = os.path.getsize(filename) / 1024
    print(f"File: {filename}")
    print(f"Size: {size_kb:.0f} KB")
    print(f"Format: {filename.split('.')[-1]}")
    print(f"DPI: 300")
    print(f"Figure size: {fig.get_size_inches()} in")
    print("✓ Figure saved successfully")
```

#warning-box[
  Always preview your figure at 100% zoom in a PDF viewer before submission. What looks good at 200% zoom may be illegible at actual print size. Check that all text, lines, and markers are clearly visible.
]

== Summary

Publication-quality figures require attention to journal specifications, font choices, resolution, color accessibility, and multi-panel layouts. By following the guidelines in this chapter, you can create figures that meet the standards of top academic journals. In the next chapter, we apply these skills to real-world projects.









