#import "../macros.typ": note-box, warning-box, info-box
= Axes Customization

Axes are where the data lives. This chapter covers advanced control over axes: scales, limits, secondary axes, annotations, and transformations.

== Setting Limits and Scales

=== Axis Limits

```python
# Explicit limits
ax.set_xlim(0, 100)
ax.set_ylim(-1.5, 1.5)

# Auto margins (add padding)
ax.margins(x=0.05, y=0.1)

# Invert axes
ax.invert_xaxis()
ax.invert_yaxis()
```

=== Logarithmic Scales

```python
ax.set_xscale('log')
ax.set_yscale('log')

# Symmetric log (handles negative values)
ax.set_yscale('symlog', linthresh=0.1)

# Logit scale for probabilities
ax.set_xscale('logit')
```

#note-box[
  Use log scales when your data spans multiple orders of magnitude, such as income distributions, earthquake magnitudes, or bacterial growth.
]

=== Custom Scales

```python
# Reciprocal
ax.set_yscale('function', functions=(lambda x: 1/x, lambda x: 1/x))

# Square root
ax.set_yscale('function', functions=(np.sqrt, np.square))
```

== Secondary Axes

Secondary axes share the same data space but have different scales or units.

```python
fig, ax = plt.subplots(figsize=(8, 4))

# Primary axis
x_celsius = np.linspace(0, 100, 10)
y = x_celsius ** 1.5
ax.plot(x_celsius, y, color='#d62728')
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Output')

# Secondary axis (Fahrenheit)
def c_to_f(c):
    return c * 9/5 + 32

def f_to_c(f):
    return (f - 32) * 5/9

secax = ax.secondary_xaxis('top', functions=(c_to_f, f_to_c))
secax.set_xlabel('Temperature (°F)')
```

== Twin Axes

Twin axes share the x-axis but have independent y-axes—useful for comparing datasets with different units.

```python
fig, ax1 = plt.subplots(figsize=(8, 4))

x = np.linspace(0, 10, 50)
ax1.plot(x, np.exp(x), color='#1f77b4', label='Exponential')
ax1.set_xlabel('x')
ax1.set_ylabel('exp(x)', color='#1f77b4')
ax1.tick_params(axis='y', labelcolor='#1f77b4')

ax2 = ax1.twinx()
ax2.plot(x, np.sin(x), color='#d62728', label='Sine')
ax2.set_ylabel('sin(x)', color='#d62728')
ax2.tick_params(axis='y', labelcolor='#d62728')

plt.title('Twin Axes: Different Scales')
plt.show()
```

#warning-box[
  Use twin axes sparingly. They can mislead readers into drawing false correlations. Always label each axis clearly and use different colors.
]

== Annotations

Annotations draw attention to specific data points or features.

=== Text Annotations

```python
fig, ax = plt.subplots(figsize=(8, 4))
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)
ax.plot(x, y)

# Basic annotation
ax.annotate('Maximum', xy=(np.pi/2, 1), xytext=(np.pi/2 + 1, 1.2),
            arrowprops=dict(arrowstyle='->', color='black'),
            fontsize=10)

# Annotation with box
ax.annotate('Zero crossing', xy=(np.pi, 0), xytext=(np.pi + 0.5, -0.5),
            arrowprops=dict(arrowstyle='->', color='gray'),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow'),
            fontsize=10)
```

=== Arrow Styles

```python
arrowstyles = ['-', '->', '-[', '-|>', '<->', '<|-|>']
```

=== Text Boxes

```python
ax.text(0.95, 0.05, 'N = 1000',
        transform=ax.transAxes,  # Use axes coordinates
        fontsize=10,
        verticalalignment='bottom',
        horizontalalignment='right',
        bbox=dict(boxstyle='square', facecolor='white', alpha=0.8))
```

== Coordinate Systems

Matplotlib provides several coordinate systems:

| *System* | *Transform* | *Coordinates* |
|---|---|---|
| Data | `ax.transData` | Data values |
| Axes | `ax.transAxes` | 0–1 within axes |
| Figure | `fig.transFigure` | 0–1 within figure |
| Display | `fig.transFigure` | Pixel coordinates |

```python
# Place text relative to axes (independent of data)
ax.text(0.5, 0.95, 'Figure Title', transform=ax.transAxes,
        ha='center', va='top', fontweight='bold')

# Place text in figure coordinates
fig.text(0.5, 0.02, 'Common X Label', ha='center')
```

== Working with Dates

```python
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Create date range
dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(365)]
values = np.random.randn(365).cumsum()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(dates, values)

# Format the x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

fig.autofmt_xdate()  # Rotate and align labels
ax.set_ylabel('Cumulative Value')
ax.set_title('Time Series with Date Formatting')
plt.show()
```

== Summary

You now have fine-grained control over axes: limits, scales, secondary and twin axes, annotations, coordinate systems, and date formatting. This level of control is what makes Matplotlib the preferred library for publication-quality figures. In the next chapter, we explore multiple plots and subplot layouts.








