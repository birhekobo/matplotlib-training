#import "../macros.typ": note-box, warning-box, info-box
= Appendix

This appendix provides quick reference guides, cheat sheets, and additional resources.

== Matplotlib Cheat Sheet

=== Quick Start

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y)                    # Line plot
ax.scatter(x, y)                 # Scatter plot
ax.bar(x, y)                     # Bar chart
ax.hist(data, bins=20)           # Histogram
ax.contour(X, Y, Z)              # Contour plot
ax.pcolormesh(X, Y, Z)           # 2D color plot
fig.savefig('output.pdf')        # Save figure
plt.show()                       # Display
```

=== Common Customizations

```python
ax.set_xlabel('Label', fontsize=12)
ax.set_ylabel('Label', fontsize=12)
ax.set_title('Title', fontsize=14)
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)
ax.set_xscale('log')
ax.set_yscale('log')
ax.grid(True, alpha=0.3)
ax.legend(loc='best')
ax.text(x, y, 'text')
ax.annotate('text', xy=(x, y), xytext=(x2, y2),
            arrowprops=dict(arrowstyle='->'))
ax.axhline(y=0, color='gray')
ax.axvline(x=0, color='gray')
```

=== Line Styles

| *Style* | *Syntax* |
|---|---|
| Solid | `-` |
| Dashed | `--` |
| Dash-dot | `-.` |
| Dotted | `:` |
| None | `''` or `None` |

=== Markers

| *Marker* | *Syntax* |
|---|---|
| Circle | `o` |
| Square | `s` |
| Triangle up | `^` |
| Diamond | `D` |
| Star | `*` |
| Plus | `+` |
| Cross | `x` |
| Point | `.` |
| Pixel | `,` |

=== Colormaps by Category

| *Type* | *Recommended Colormaps* |
|---|---|
| Sequential | `viridis`, `plasma`, `inferno`, `magma`, `Blues`, `YlOrRd` |
| Diverging | `RdBu`, `RdYlBu`, `coolwarm`, `PiYG`, `PuOr` |
| Qualitative | `tab10`, `Set2`, `Paired`, `Dark2` |
| Cyclic | `twilight`, `hsv` |
| Misc | `terrain`, `gist_earth`, `ocean` |

== Cartopy Quick Reference

=== Common Projections

```python
import cartopy.crs as ccrs

ccrs.PlateCarree()                # Simple lat/lon
ccrs.Robinson()                   # World map (aesthetic)
ccrs.Mercator()                   # Navigation
ccrs.Orthographic(central_longitude=20, central_latitude=10)
ccrs.LambertConformal()           # Mid-latitudes
ccrs.NorthPolarStereo()           # Arctic
ccrs.SouthPolarStereo()           # Antarctic
```

=== Geographic Features

```python
import cartopy.feature as cfeature

ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)
```

=== Gridlines

```python
gl = ax.gridlines(draw_labels=True, linestyle='--', alpha=0.3)
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 8}
gl.ylabel_style = {'size': 8}
```

== Keyboard Shortcuts (Jupyter)

| *Shortcut* | *Action* |
|---|---|
| `Shift + Enter` | Run cell, select next |
| `Ctrl + Enter` | Run cell in place |
| `Esc + a` | Insert cell above |
| `Esc + b` | Insert cell below |
| `Esc + dd` | Delete cell |
| `Esc + m` | Markdown cell |
| `Esc + y` | Code cell |
| `Esc + h` | Show all shortcuts |
| `Esc + o` | Toggle output |
| `Esc + 0` | Restart kernel |

== Troubleshooting Quick Reference

| *Problem* | *Check* | *Solution* |
|---|---|---|
| Plot not showing | Jupyter backend | `%matplotlib inline` |
| Blurry figure | DPI setting | `plt.rcParams['figure.dpi'] = 150` |
| Labels clipped | Save options | `fig.savefig('f.pdf', bbox_inches='tight')` |
| Missing Cartopy features | Installation | `conda install -c conda-forge cartopy` |
| Slow large plot | Subsampling | `data[::2, ::2]` |
| Color mismatch print/screen | Color space | Use CMYK for print, RGB for screen |
| Legend outside plot | Position | `ax.legend(bbox_to_anchor=(1.05, 1))` |
| Date labels overlap | Rotation | `fig.autofmt_xdate()` |
| Memory leak | Close figures | `plt.close(fig)` in loops |
| CHIRPS missing values | Mask NaNs | `data.where(data >= 0)` |

== Resources

=== Documentation

- Matplotlib: `https://matplotlib.org/stable/`
- Cartopy: `https://scitools.org.uk/cartopy/docs/latest/`
- NumPy: `https://numpy.org/doc/stable/`
- Pandas: `https://pandas.pydata.org/docs/`
- xarray: `https://docs.xarray.dev/en/stable/`
- CHIRPS: `https://www.chc.ucsb.edu/data/chirps`

=== Books

- Tufte, E. (2001). *The Visual Display of Quantitative Information*
- Cairo, A. (2012). *The Functional Art*
- Wilke, C. (2019). *Fundamentals of Data Visualization*
- Ware, C. (2012). *Information Visualization: Perception for Design*

=== Tools

- ColorBrewer: `https://colorbrewer2.org/` — Color palette selection
- Coolors: `https://coolors.co/` — Color scheme generator
- Viz Palette: `https://projects.susielu.com/viz-palette` — Color accessibility checker
- Adobe Color: `https://color.adobe.com/` — Color wheel

=== Communities

- StackOverflow `[matplotlib]`: `https://stackoverflow.com/questions/tagged/matplotlib`
- Matplotlib GitHub: `https://github.com/matplotlib/matplotlib`
- Python-Visualization: `https://discourse.matplotlib.org/`

=== BibTeX Citation for This Course

```bibtex
@misc{matplotlib-training2024,
  author = {Matplotlib Training Course},
  title = {Matplotlib Training: From Zero to Publication-Quality Visualizations},
  year = {2024},
  howpublished = {\url{https://github.com/example/matplotlib-training}}
}
```

== Glossary

| *Term* | *Definition* |
|---|---|
| *Artist* | Any visual element in a Matplotlib figure (lines, text, patches) |
| *Axes* | The data plotting area within a Figure |
| *Axes coordinates* | Coordinate system where (0,0) is bottom-left and (1,1) is top-right of axes |
| *Backend* | The rendering engine (Agg for files, QtAgg for interactive, etc.) |
| *cbar* | Colorbar — maps data values to colors |
| *CHIRPS* | Climate Hazards Group InfraRed Precipitation with Station data |
| *CRS* | Coordinate Reference System — defines how coordinates map to Earth |
| *DPI* | Dots Per Inch — resolution measure for printing |
| *Figure* | The top-level container holding axes and artists |
| *GridSpec* | A specification for subplot layout with spanning support |
| *IQR* | Interquartile Range — 25th to 75th percentile |
| *KDE* | Kernel Density Estimate — smooth estimate of probability density |
| *NetCDF* | Network Common Data Format — self-describing scientific data format |
| *OO API* | Object-Oriented API — using fig, ax explicitly vs. pyplot state machine |
| *rcParams* | Matplotlib's runtime configuration parameters |
| *Transform* | The coordinate transformation from data to display space |


