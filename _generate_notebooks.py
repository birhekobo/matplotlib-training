"""Generate notebooks 05-08 for Matplotlib Training with CHIRPS data."""
import json, textwrap

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in source.split("\n")]}

def code(source):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": [line + "\n" for line in source.split("\n")]}

NB_META = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
           "language_info": {"name": "python", "version": "3.12.0"}}

def save_nb(name, cells):
    nb = {"nbformat": 4, "nbformat_minor": 5, "metadata": NB_META, "cells": cells}
    path = rf"D:\WOLLO_SATELLITE_REMOTE_SENSING_WEBSITE\matplotlib-training\notebooks\{name}"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"Saved {path}")

# ──────────────────────── NOTEBOOK 05 ────────────────────────
def make_05():
    cells = []

    cells.append(md("""# Module 05: Basic Chart Types with Matplotlib
**CHIRPS Rainfall Data – Ethiopia**

In this module you will learn the fundamental chart types available in Matplotlib.
All examples use real CHIRPS (Climate Hazards Group InfraRed Precipitation with Station)
precipitation data for Ethiopia at 0.05° resolution, January 1981 – December 2022.

"""))

    cells.append(code("""import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

# Load CHIRPS dataset
ds = xr.open_dataset(r'../chirps_1981_2022.nc', engine='netcdf4')
print(f"Dataset shape: {ds.dims}")
print(f"Time range: {ds.time.values[0]} to {ds.time.values[-1]}")
print(f"Mean precipitation: {ds.precip.mean().values:.2f} mm/month")
"""))

    cells.append(code("""# Extract time series at Addis Ababa (9.025N, 38.725E)
lat_idx, lon_idx = 180, 174
ts = ds.precip.isel(latitude=lat_idx, longitude=lon_idx)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
print(f"Location: lat={ds.latitude[lat_idx].values:.3f}, lon={ds.longitude[lon_idx].values:.3f}")
print(f"Record length: {len(ts)} months")
print(f"Annual mean: {ts_df.resample('YE').mean().mean().values[0]:.1f} mm/month")
"""))

    cells.append(md("""---
## 5.1 Line Plot – Rainfall Time Series

The **line plot** is the most basic chart type. It connects data points with straight line segments
and is ideal for showing trends over time.
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(ts_df.index, ts_df['precip'], linewidth=0.6, color='steelblue')
ax.set_title('CHIRPS Monthly Precipitation at Addis Ababa (9.025N, 38.725E)', fontsize=13)
ax.set_xlabel('Year')
ax.set_ylabel('Precipitation (mm/month)')
ax.set_xlim(ts_df.index[0], ts_df.index[-1])
plt.tight_layout()
plt.show()
"""))

    cells.append(code("""# 5-year subset for clarity
fig, ax = plt.subplots(figsize=(12, 4))
sub = ts_df.loc['2000':'2004']
ax.plot(sub.index, sub['precip'], marker='o', markersize=3, linewidth=1, color='coral')
ax.set_title('CHIRPS Precipitation 2000–2004 at Addis Ababa')
ax.set_xlabel('Date'); ax.set_ylabel('Precipitation (mm/month)')
ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 5.2 Scatter Plot – Lag Correlation

Scatter plots show the relationship between two variables. Here we examine
**autocorrelation**: does this month's rainfall predict next month's?
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(6, 6))
precip = ts_df['precip'].values
ax.scatter(precip[:-1], precip[1:], s=8, alpha=0.4, color='darkgreen')
ax.set_title('Lag-1 Autocorrelation – Addis Ababa Rainfall')
ax.set_xlabel('Precipitation month t (mm)')
ax.set_ylabel('Precipitation month t+1 (mm)')

# 1:1 line
lims = [0, max(precip)]
ax.plot(lims, lims, 'r--', linewidth=0.8, label='1:1')
ax.legend()
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_aspect('equal')
plt.tight_layout(); plt.show()

corr = np.corrcoef(precip[:-1], precip[1:])[0, 1]
print(f"Lag-1 Pearson correlation: {corr:.3f}")
"""))

    cells.append(md("""---
## 5.3 Bar Chart – Monthly Climatology

Bar charts use vertical bars to represent quantities. The **climatology** (mean annual cycle)
is a classic application: average rainfall for each calendar month.
"""))

    cells.append(code("""monthly_mean = ts_df.groupby(ts_df.index.month).mean()
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(months, monthly_mean['precip'], color='royalblue', edgecolor='navy', linewidth=0.8)
ax.set_title('Monthly Rainfall Climatology – Addis Ababa (1981–2022)')
ax.set_xlabel('Month'); ax.set_ylabel('Mean Precipitation (mm/month)')
ax.set_ylim(0, monthly_mean['precip'].max() * 1.15)

# Add value labels
for bar, val in zip(bars, monthly_mean['precip']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{val:.0f}',
            ha='center', va='bottom', fontsize=8)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 5.4 Horizontal Bar Chart – Regional Comparison

Horizontal bars are useful when category labels are long or when comparing many items.
"""))

    cells.append(code("""# Extract mean rainfall for several Ethiopian regions
regions = {
    'Addis Ababa':  (180, 174),
    'Gondar':       (252, 150),
    'Mekelle':      (270, 190),
    'Dire Dawa':    (192, 237),
    'Jimma':        (  8, 144),
    'Bahir Dar':    (235, 140),
}
means = {}
for name, (li, lo) in regions.items():
    means[name] = float(ds.precip.isel(latitude=li, longitude=lo).mean().values)

fig, ax = plt.subplots(figsize=(9, 5))
names_list = list(means.keys())
vals_list  = list(means.values())
bars = ax.barh(names_list, vals_list, color='teal', edgecolor='darkcyan')
ax.set_title('Mean Monthly Rainfall – Ethiopian Regions (1981–2022)')
ax.set_xlabel('Precipitation (mm/month)')
for bar, v in zip(bars, vals_list):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{v:.1f}',
            va='center', fontsize=9)
ax.set_xlim(0, max(vals_list) * 1.2)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 5.5 Histogram – Rainfall Distribution

Histograms show the **frequency distribution** of a continuous variable.
They reveal the shape, spread, and central tendency of the data.
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(ts_df['precip'], bins=40, color='mediumseagreen', edgecolor='white', linewidth=0.6)
ax.set_title('Distribution of Monthly Rainfall – Addis Ababa')
ax.set_xlabel('Precipitation (mm/month)'); ax.set_ylabel('Frequency (months)')
ax.axvline(ts_df['precip'].mean(), color='darkred', linestyle='--', linewidth=1.5,
           label=f"Mean = {ts_df['precip'].mean():.1f} mm")
ax.axvline(ts_df['precip'].median(), color='orange', linestyle=':', linewidth=1.5,
           label=f"Median = {ts_df['precip'].median():.0f} mm")
ax.legend()
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 5.6 Pie Chart – Seasonal Rainfall Proportion

Pie charts show proportions of a whole. Despite their popularity, they should be used sparingly.
Here we show the seasonal contribution to total annual rainfall.
"""))

    cells.append(code("""# Define seasons: DJF, MAM, JJA, SON
ts_df['season'] = ts_df.index.month.map({12:'DJF',1:'DJF',2:'DJF',
                                          3:'MAM',4:'MAM',5:'MAM',
                                          6:'JJA',7:'JJA',8:'JJA',
                                          9:'SON',10:'SON',11:'SON'})
seasonal = ts_df.groupby('season')['precip'].sum()
# Reorder
seasonal = seasonal[['DJF','MAM','JJA','SON']]
season_labels = ['DJF (Winter)', 'MAM (Spring)', 'JJA (Summer)', 'SON (Autumn)']

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    seasonal.values, labels=season_labels, autopct='%1.1f%%',
    colors=['cornflowerblue', 'lightgreen', 'gold', 'lightcoral'],
    startangle=90, explode=(0, 0, 0.05, 0),
    textprops={'fontsize': 11}
)
ax.set_title('Seasonal Rainfall Proportion – Addis Ababa', fontsize=13, pad=20)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 5.7 Stem Plot

Stem plots (or *lollipop charts*) draw lines from a baseline to each data point.
They work well for discrete data or when you want to emphasise individual values.
"""))

    cells.append(code("""# Last 24 months of the record
last24 = ts_df.iloc[-24:]
fig, ax = plt.subplots(figsize=(12, 4))
markerline, stemlines, baseline = ax.stem(
    last24.index, last24['precip'],
    linefmt='-b', markerfmt='ob', basefmt='-k', use_line_collection=True
)
ax.set_title('Stem Plot – Last 24 Months at Addis Ababa')
ax.set_ylabel('Precipitation (mm/month)')
ax.set_xlabel('Date')
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 5.8 Step Plot

Step plots show changes as discrete jumps, which is useful for highlighting
when thresholds are crossed or for cumulative data.
"""))

    cells.append(code("""cumulative = ts_df['precip'].cumsum() / 1000  # in metres
fig, ax = plt.subplots(figsize=(14, 4))
ax.step(ts_df.index, cumulative, where='mid', linewidth=1.2, color='darkorange')
ax.set_title('Cumulative Precipitation – Addis Ababa (Step Plot)')
ax.set_xlabel('Year'); ax.set_ylabel('Cumulative Precip (m)')
ax.grid(True, alpha=0.3)
plt.tight_layout(); plt.show()

print(f"Total cumulative rainfall: {cumulative.iloc[-1]:.2f} m over {len(ts_df)} months")
"""))

    cells.append(md("""---
## Exercises – Module 05

1. **Line plot**: Extract the time series for **Gondar** (lat_idx=252, lon_idx=150) and create a
   line plot of monthly rainfall from 2010 to 2020. Add markers for months exceeding 200 mm.

2. **Scatter plot**: Create a scatter plot of **Mekelle** rainfall vs **Addis Ababa** rainfall
   (same time steps). Compute and display the correlation coefficient.

3. **Bar chart**: Compute the monthly climatology for **Dire Dawa** and plot it as a bar chart.
   Which month is the wettest?

4. **Horizontal bar chart**: Extract mean rainfall for 8 Ethiopian cities and create a horizontal
   bar chart sorted from wettest to driest.

5. **Histogram**: Plot side-by-side histograms of rainfall for the **short rainy season** (MAM)
   and **long rainy season** (JJA) in Addis Ababa. Use 20 bins, alpha=0.6.

6. **Pie chart**: Create a pie chart showing the proportion of rainfall contributed by each
   calendar month at a location of your choice.

7. **Stem plot**: Create a stem plot of the 12 monthly climatology values.

8. **Step plot**: Create a step plot showing the cumulative rainfall for the **year 1997**
   (the El Niño year) and compare its shape to a normal year (e.g. 2000).

### Mini-Project: Rainfall Regime Classification

Create a 2×3 figure that characterises the rainfall regime at **Addis Ababa**:
- Top-left: Line plot of the full time series
- Top-middle: Bar chart of monthly climatology
- Top-right: Histogram of monthly rainfall
- Middle-left: Seasonal pie chart
- Middle-middle: Scatter of Oct–Dec vs Mar–May totals (interannual variability)
- Middle-right: Step plot of 1997 cumulative rainfall

Use `plt.subplots(nrows=2, ncols=3, figsize=(16, 10))`.
"""))

    cells.append(code("""# Mini-Project starter
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. Line plot
axes[0,0].plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
axes[0,0].set_title('Full Time Series'); axes[0,0].set_ylabel('mm/month')

# 2. Bar chart – climatology
monthly = ts_df.groupby(ts_df.index.month)['precip'].mean()
axes[0,1].bar(months, monthly, color='royalblue', edgecolor='navy')
axes[0,1].set_title('Monthly Climatology')

# 3. Histogram
axes[0,2].hist(ts_df['precip'], bins=40, color='mediumseagreen', edgecolor='white')
axes[0,2].axvline(ts_df['precip'].mean(), color='red', ls='--')
axes[0,2].set_title('Rainfall Distribution'); axes[0,2].set_xlabel('mm/month')

# 4. Seasonal pie
seasonal = ts_df.groupby('season')['precip'].sum()
seasonal = seasonal[['DJF','MAM','JJA','SON']]
axes[1,0].pie(seasonal, labels=seasonal.index, autopct='%1.0f%%')
axes[1,0].set_title('Seasonal Proportions')

# 5. Scatter: Oct-Dec vs Mar-May
oct_dec = ts_df[ts_df.index.month.isin([10,11,12])].groupby(ts_df[ts_df.index.month.isin([10,11,12])].index.year)['precip'].sum()
mar_may = ts_df[ts_df.index.month.isin([3,4,5])].groupby(ts_df[ts_df.index.month.isin([3,4,5])].index.year)['precip'].sum()
axes[1,1].scatter(oct_dec, mar_may, s=20, alpha=0.6, color='darkgreen')
axes[1,1].set_xlabel('OND total (mm)'); axes[1,1].set_ylabel('MAM total (mm)')
axes[1,1].set_title('OND vs MAM Totals')

# 6. Step plot – 1997 cumulative
year97 = ts_df.loc['1997']
cum97 = year97['precip'].cumsum()
axes[1,2].step(cum97.index, cum97, where='mid', color='darkorange')
axes[1,2].set_title('1997 Cumulative'); axes[1,2].set_ylabel('mm')

plt.tight_layout()
plt.show()
"""))

    save_nb("05_basic_charts.ipynb", cells)

# ──────────────────────── NOTEBOOK 06 ────────────────────────
def make_06():
    cells = []

    cells.append(md("""# Module 06: Styling Plots with Matplotlib
**CHIRPS Rainfall Data – Ethiopia**

Visual styling transforms a functional plot into a publication-ready graphic.
This module covers colours, markers, line styles, fonts, labels, legends, gridlines,
and Matplotlib style sheets.
"""))

    cells.append(code("""import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset(r'../chirps_1981_2022.nc', engine='netcdf4')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
print("Data loaded successfully")
"""))

    cells.append(md("""---
## 6.1 Colours

Matplotlib supports many colour specifications: named colours, hex strings, RGB tuples, and
colormaps. See https://matplotlib.org/stable/gallery/color/named_colors.html
"""))

    cells.append(code("""# Different colour specifications
color_named = 'firebrick'
color_hex   = '#1f77b4'
color_rgb   = (0.2, 0.6, 0.4)

fig, axes = plt.subplots(3, 1, figsize=(10, 5))

axes[0].plot(ts_df.index[:120], ts_df['precip'][:120], color=color_named, linewidth=0.8)
axes[0].set_title('Named colour: firebrick')

axes[1].plot(ts_df.index[:120], ts_df['precip'][:120], color=color_hex, linewidth=0.8)
axes[1].set_title('Hex colour: #1f77b4')

axes[2].plot(ts_df.index[:120], ts_df['precip'][:120], color=color_rgb, linewidth=0.8)
axes[2].set_title('RGB tuple: (0.2, 0.6, 0.4)')

for ax in axes:
    ax.set_ylabel('Precip (mm/month)')
plt.tight_layout(); plt.show()
"""))

    cells.append(code("""# Colormaps – gradient of colours
fig, ax = plt.subplots(figsize=(10, 4))
years = ts_df.index.year
colours = plt.cm.viridis((years - years.min()) / (years.max() - years.min()))

for i in range(len(ts_df)):
    ax.plot(ts_df.index[i], ts_df['precip'][i], marker='o', linestyle='none',
            color=colours[i], markersize=4, alpha=0.6)

ax.set_title('Rainfall coloured by year (viridis colormap)')
ax.set_ylabel('Precipitation (mm/month)')
sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(years.min(), years.max()))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax)
cbar.set_label('Year')
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.2 Markers

Markers emphasise individual data points. Matplotlib offers many marker styles
(`'o'`, `'^'`, `'s'`, `'D'`, `'*'`, `'x'`, etc.) with controls for size, edge, and face colours.
"""))

    cells.append(code("""fig, axes = plt.subplots(2, 2, figsize=(12, 6))

# Marker types on a climatology
axes[0,0].plot(months, monthly_mean, marker='o', markersize=8, linewidth=1.5, color='#2c7bb6')
axes[0,0].set_title('Circle markers')

axes[0,1].plot(months, monthly_mean, marker='s', markersize=8, linewidth=1.5, color='#d7191c')
axes[0,1].set_title('Square markers')

axes[1,0].plot(months, monthly_mean, marker='^', markersize=8, linewidth=1.5, color='#1a9641')
axes[1,0].set_title('Triangle markers')

# Custom marker style
axes[1,1].plot(months, monthly_mean, marker='D', markersize=10, markerfacecolor='gold',
               markeredgecolor='darkgoldenrod', markeredgewidth=1.5,
               linewidth=1.5, color='darkgoldenrod', linestyle='--')
axes[1,1].set_title('Custom diamond markers')

for ax in axes.flat:
    ax.set_ylabel('Precip (mm/month)')
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.3 Line Styles

Line styles control the appearance of connecting lines: solid, dashed, dotted, dash-dot.
You can also use the `(offset, (on_off_seq))` tuple for custom patterns.
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(10, 5))

styles = [
    ('-',  'solid',    'black'),
    ('--', 'dashed',   'darkred'),
    (':',  'dotted',   'darkgreen'),
    ('-.', 'dash-dot', 'darkblue'),
    ((0, (3, 1, 1, 1)), 'custom',  'purple'),
]

for i, (sty, label, col) in enumerate(styles):
    offset = i * 50  # vertical offset for clarity
    ax.plot(months, monthly_mean + offset, linestyle=sty, color=col,
            linewidth=2, label=f"{label} ({sty})", marker='o', markersize=5)

ax.set_title('Line Styles Comparison')
ax.set_ylabel('Precip + offset (mm/month)')
ax.legend(fontsize=9)
ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.4 Fonts – Family, Size, Weight

You can control text appearance globally via `rcParams` or per element.
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(months, monthly_mean, linewidth=2, color='steelblue', marker='o')

ax.set_title('Font Customisation Demo', fontfamily='serif', fontsize=16, fontweight='bold')
ax.set_xlabel('Month', fontfamily='serif', fontsize=12, fontstyle='italic')
ax.set_ylabel('Precipitation (mm/month)', fontfamily='serif', fontsize=12)

ax.tick_params(axis='both', labelsize=10)
for label in ax.get_xticklabels():
    label.set_fontstyle('italic')
for label in ax.get_yticklabels():
    label.set_fontweight('bold')

plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.5 Labels and Titles

Clear, descriptive labels are essential. `ax.set_xlabel()`, `ax.set_ylabel()`,
and `ax.set_title()` accept `fontdict` for full control.
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(ts_df.index[:240], ts_df['precip'][:240], color='slateblue', linewidth=0.8)

title_font = {'family': 'sans-serif', 'size': 14, 'weight': 'bold', 'color': 'navy'}
label_font = {'family': 'sans-serif', 'size': 11, 'color': 'darkslategray'}

ax.set_title('CHIRPS Monthly Rainfall – Addis Ababa (1981–2000)', fontdict=title_font, pad=15)
ax.set_xlabel('Date', fontdict=label_font)
ax.set_ylabel('Precipitation (mm/month)', fontdict=label_font)

# Annotation
ax.annotate('Peak: Aug 1987', xy=(pd.Timestamp('1987-08-01'), 350),
            xytext=(pd.Timestamp('1986-06-01'), 380),
            arrowprops=dict(arrowstyle='->', color='darkred'),
            fontsize=10, color='darkred')

plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.6 Legends

`ax.legend()` controls legend placement (`loc`), number of columns (`ncol`),
frame visibility, and more.
"""))

    cells.append(code("""# Multiple locations with legend
fig, ax = plt.subplots(figsize=(12, 5))

for loc_name, lat_i, lon_i in [('Addis Ababa', 180, 174), ('Gondar', 252, 150),
                                 ('Mekelle', 270, 190), ('Dire Dawa', 192, 237)]:
    serie = ds.precip.isel(latitude=lat_i, longitude=lon_i)
    clim = serie.groupby('time.month').mean()
    ax.plot(months, clim, marker='o', markersize=4, label=loc_name, linewidth=1.5)

ax.set_title('Monthly Climatology – Multiple Stations', fontsize=13, weight='bold')
ax.set_xlabel('Month'); ax.set_ylabel('Precipitation (mm/month)')
ax.legend(loc='upper left', ncol=2, frameon=True, fancybox=True, shadow=True,
          fontsize=10, title='Station', title_fontsize=11)
ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.7 Gridlines

Gridlines improve readability. Use `ax.grid()` with `which='major'`/`'minor'`/
`'both'` and control style via `linestyle`, `alpha`, etc.
"""))

    cells.append(code("""from matplotlib.ticker import MultipleLocator

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(months, monthly_mean, linewidth=2, color='#2c7bb6', marker='s', markersize=6)

# Major grid
ax.grid(True, which='major', linestyle='-', alpha=0.5, color='gray', linewidth=0.8)
# Minor grid
ax.grid(True, which='minor', linestyle=':', alpha=0.3, color='gray', linewidth=0.5)
ax.xaxis.set_minor_locator(MultipleLocator(1))   # minor ticks between months
ax.yaxis.set_minor_locator(MultipleLocator(20))

ax.set_title('Gridlines – Major and Minor')
ax.set_xlabel('Month'); ax.set_ylabel('Precipitation (mm/month)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 6.8 Themes and Style Sheets

Matplotlib provides built-in style sheets (`'ggplot'`, `'seaborn-v0_8'`, `'bmh'`,
`'fivethirtyeight'`, `'dark_background'`, etc.) for consistent theming.
"""))

    cells.append(code("""styles_to_try = ['default', 'ggplot', 'seaborn-v0_8', 'bmh', 'fivethirtyeight', 'dark_background']
n_styles = len(styles_to_try)

fig, axes = plt.subplots(3, 2, figsize=(14, 10))

for ax, style in zip(axes.flat, styles_to_try):
    with plt.style.context(style):
        ax.plot(months, monthly_mean, marker='o', markersize=6, linewidth=1.5)
        ax.set_title(f"Style: '{style}'")
        ax.set_ylabel('mm/month')
        ax.tick_params(axis='x', rotation=45)

plt.tight_layout(); plt.show()
"""))

    cells.append(code("""# Using a specific style for a publication-ready plot
plt.style.use('seaborn-v0_8')

fig, ax = plt.subplots(figsize=(12, 5))

ten_years = ts_df.loc['2010':'2019']
ax.fill_between(ten_years.index, ten_years['precip'], alpha=0.3, color='steelblue')
ax.plot(ten_years.index, ten_years['precip'], linewidth=1.2, color='steelblue', marker='o', markersize=3)
ax.axhline(ten_years['precip'].mean(), color='darkred', linestyle='--', linewidth=1,
           label=f'Mean = {ten_years["precip"].mean():.1f} mm')

ax.set_title('CHIRPS Rainfall 2010–2019, Addis Ababa — Publication Style')
ax.set_xlabel('Date'); ax.set_ylabel('Precipitation (mm/month)')
ax.legend(loc='upper right', frameon=True)
plt.tight_layout(); plt.show()

# Reset style
plt.style.use('default')
"""))

    cells.append(md("""---
## Exercises – Module 06

1. **Colours**: Create a line plot of **Mekelle** rainfall using a colour gradient from
   light to dark blue that corresponds to the magnitude of rainfall.

2. **Markers**: Plot the monthly climatology for **Gondar** with diamond markers, size 10,
   gold face colour, dark red edge colour, and width 2.

3. **Line styles**: Plot the 1997 and 2000 cumulative rainfall on the same axes using
   different line styles. Add a legend.

4. **Fonts**: Create a figure where the title is Helvetica bold 18pt, axis labels are
   Times New Roman italic 14pt, and tick labels are 12pt.

5. **Labels**: Annotate the three wettest months on a climatology bar chart with arrows.

6. **Legends**: Plot climatologies for 5 Ethiopian cities with custom legend handles
   (use `Patch` from `matplotlib.patches`).

7. **Gridlines**: Create a plot with major grid every 50 mm and minor grid every 10 mm.

8. **Style sheets**: Create a 2×2 figure showing the same climatology under 4 different
   style sheets (`'ggplot'`, `'bmh'`, `'fivethirtyeight'`, `'dark_background'`).

### Mini-Project: Publication-Ready Rainfall Bulletin

Create a single, professionally styled figure showing:
- **Top panel**: Time series for Addis Ababa, 2000–2020, with a filled area under the curve,
  a horizontal line at the mean, and a legend
- **Bottom panel**: Monthly climatology as a bar chart with value labels on top

Use `'seaborn-v0_8'` style, a serif font for the title (bold, 16pt), and custom gridlines.
Add a caption-style annotation explaining the data source.
"""))

    cells.append(code("""# Mini-Project starter
plt.style.use('seaborn-v0_8')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9))

# Top panel – time series
sub = ts_df.loc['2000':'2020']
ax1.fill_between(sub.index, sub['precip'], alpha=0.25, color='steelblue')
ax1.plot(sub.index, sub['precip'], linewidth=0.8, color='steelblue', label='Monthly')
ax1.axhline(sub['precip'].mean(), color='crimson', linestyle='--', linewidth=1.2,
            label=f"Mean = {sub['precip'].mean():.1f} mm")
ax1.set_title('CHIRPS Rainfall at Addis Ababa (9.025°N, 38.725°E)', fontfamily='serif',
              fontsize=16, fontweight='bold')
ax1.set_ylabel('Precipitation (mm/month)')
ax1.legend(fontsize=10, loc='upper right')
ax1.grid(True, alpha=0.3)

# Bottom panel – climatology
bars = ax2.bar(months, monthly_mean, color='steelblue', edgecolor='navy', alpha=0.85)
for bar, val in zip(bars, monthly_mean):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{val:.0f}',
             ha='center', va='bottom', fontsize=8)
ax2.set_title('Monthly Climatology (1981–2022)', fontfamily='serif', fontsize=14)
ax2.set_xlabel('Month'); ax2.set_ylabel('Mean Precipitation (mm/month)')
ax2.grid(True, axis='y', alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

fig.text(0.5, 0.01, 'Data: CHIRPS Version 2.0, Climate Hazards Center, UC Santa Barbara',
         ha='center', fontsize=9, style='italic', color='gray')
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.show()

plt.style.use('default')
"""))

    save_nb("06_styling_plots.ipynb", cells)

# ──────────────────────── NOTEBOOK 07 ────────────────────────
def make_07():
    cells = []

    cells.append(md("""# Module 07: Axes Customization
**CHIRPS Rainfall Data – Ethiopia**

Fine-tune every aspect of your plot axes: limits, ticks, scales, secondary axes,
aspect ratios, and spines.
"""))

    cells.append(code("""import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoLocator, ScalarFormatter, FuncFormatter

ds = xr.open_dataset(r'../chirps_1981_2022.nc', engine='netcdf4')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
print("Data loaded")
"""))

    cells.append(md("""---
## 7.1 Axis Limits (`set_xlim` / `set_ylim`)

Control which portion of the data is visible. Useful for zooming, excluding outliers,
or ensuring consistent scales across subplots.
"""))

    cells.append(code("""fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Full range
axes[0].plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
axes[0].set_title('Full range (default limits)')
axes[0].set_ylabel('Precip (mm/month)')

# Zoom to 1990s
axes[1].plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
axes[1].set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('1999-12-01'))
axes[1].set_title('Zoom: 1990–1999')

# Zoom and clip y-axis
axes[2].plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
axes[2].set_xlim(pd.Timestamp('1990-01-01'), pd.Timestamp('1999-12-01'))
axes[2].set_ylim(0, 200)
axes[2].set_title('Zoom: 1990–1999, y=[0,200]')

for ax in axes:
    ax.set_xlabel('Date')
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 7.2 Tick Locators and Formatters

**Locators** control where ticks are placed (`MultipleLocator`, `AutoLocator`, `MaxNLocator`, etc.).
**Formatters** control the label text (`ScalarFormatter`, `FuncFormatter`, `DateFormatter`).
"""))

    cells.append(code("""from matplotlib.ticker import MultipleLocator, AutoLocator, FormatStrFormatter

fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Default
axes[0,0].plot(months, monthly_mean, 'o-', color='steelblue')
axes[0,0].set_title('Default ticks')

# MultipleLocator
axes[0,1].plot(months, monthly_mean, 'o-', color='steelblue')
axes[0,1].yaxis.set_major_locator(MultipleLocator(50))
axes[0,1].yaxis.set_minor_locator(MultipleLocator(10))
axes[0,1].xaxis.set_major_locator(MultipleLocator(2))
axes[0,1].set_title('MultipleLocator(50/10/2)')
axes[0,1].grid(True, which='both', alpha=0.3)

# FormatStrFormatter
axes[1,0].plot(months, monthly_mean, 'o-', color='steelblue')
axes[1,0].yaxis.set_major_formatter(FormatStrFormatter('%.0f mm'))
axes[1,0].set_title('FormatStrFormatter')

# FuncFormatter
def rain_category(x, pos):
    if x < 50: return f'{x:.0f} (dry)'
    if x < 150: return f'{x:.0f} (mod.)'
    return f'{x:.0f} (wet)'

axes[1,1].plot(months, monthly_mean, 'o-', color='steelblue')
axes[1,1].yaxis.set_major_formatter(FuncFormatter(rain_category))
axes[1,1].set_title('FuncFormatter – custom labels')
axes[1,1].tick_params(axis='x', rotation=45)

for ax in axes.flat:
    ax.set_ylabel('Precip (mm/month)')
plt.tight_layout(); plt.show()
"""))

    cells.append(code("""# DateFormatter for time axis
from matplotlib.dates import DateFormatter, MonthLocator, YearLocator

fig, ax = plt.subplots(figsize=(14, 4))
sub = ts_df.loc['2005':'2007']
ax.plot(sub.index, sub['precip'], 'o-', color='darkred', markersize=4)

ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_minor_formatter(DateFormatter('%b'))

ax.set_title('Date formatting – YearLocator + MonthLocator')
ax.set_ylabel('Precipitation (mm/month)')
ax.grid(True, which='both', alpha=0.3)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 7.3 Logarithmic Scales

Log scales are useful when data spans multiple orders of magnitude.
Use `semilogy`, `semilogx`, or `loglog` (or `ax.set_yscale('log')`).
"""))

    cells.append(code("""fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Linear
axes[0].plot(months, monthly_mean, 'o-', color='steelblue')
axes[0].set_title('Linear scale')
axes[0].set_ylabel('Precip (mm/month)')

# Log y
axes[1].plot(months, monthly_mean, 'o-', color='steelblue')
axes[1].set_yscale('log')
axes[1].set_title('Log y scale')
axes[1].set_ylabel('Precip (mm) [log]')
axes[1].grid(True, which='both', alpha=0.3)

# Symlog (handles zero)
symlog_data = monthly_mean.copy()
axes[2].plot(months, symlog_data, 'o-', color='steelblue')
axes[2].set_yscale('symlog', linthresh=10)
axes[2].set_title('Symlog scale (linthresh=10)')
axes[2].set_ylabel('Precip (mm) [symlog]')
axes[2].grid(True, which='both', alpha=0.3)

for ax in axes:
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 7.4 Secondary Axes

Secondary axes share the same data space but have different tick labels and scales.
Useful for showing unit conversions or complementary variables.
"""))

    cells.append(code("""fig, ax1 = plt.subplots(figsize=(10, 5))

# Primary axis – monthly climatology (mm)
ax1.plot(months, monthly_mean, 'o-', color='steelblue', linewidth=2, markersize=6)
ax1.set_xlabel('Month'); ax1.set_ylabel('Precipitation (mm/month)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

# Secondary axis – same data in metres
ax2 = ax1.twinx()
ax2.plot(months, monthly_mean / 1000, 's--', color='darkorange', linewidth=1.5, markersize=5)
ax2.set_ylabel('Precipitation (m/month)', color='darkorange')
ax2.tick_params(axis='y', labelcolor='darkorange')

# Secondary x-axis – month numbers
ax3 = ax1.secondary_xaxis('top')
ax3.set_xlabel('Month number')
ax3.set_xticks(range(12))
ax3.set_xticklabels(range(1, 13))

ax1.set_title('Dual-axis: mm (left) and m (right)')
plt.tight_layout(); plt.show()
"""))

    cells.append(code("""# Secondary axis with a conversion: mm to inches
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.bar(months, monthly_mean, color='steelblue', alpha=0.7)
ax1.set_xlabel('Month'); ax1.set_ylabel('Precipitation (mm/month)')
ax1.tick_params(axis='x', rotation=45)

def mm_to_inches(mm):
    return mm / 25.4

def inches_to_mm(inches):
    return inches * 25.4

ax2 = ax1.secondary_yaxis('right', functions=(mm_to_inches, inches_to_mm))
ax2.set_ylabel('Precipitation (inches/month)')

ax1.set_title('Dual units: mm and inches')
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 7.5 Aspect Ratio

`ax.set_aspect()` controls the physical aspect ratio of the data coordinates.
`'equal'` ensures one data unit is the same length on both axes.
`'auto'` lets Matplotlib fill the axes box.
A numeric value sets `y / x`.
"""))

    cells.append(code("""fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# auto
axes[0].plot(months, monthly_mean, 'o-', color='steelblue')
axes[0].set_aspect('auto')
axes[0].set_title('aspect="auto"')

# equal (distorts here because ranges differ)
axes[1].plot(months, monthly_mean, 'o-', color='steelblue')
axes[1].set_aspect('equal')
axes[1].set_title('aspect="equal"')

# numeric: y-unit = 2 x-unit
axes[2].plot(months, monthly_mean, 'o-', color='steelblue')
axes[2].set_aspect(0.5)
axes[2].set_title('aspect=0.5')

for ax in axes:
    ax.set_ylabel('Precip (mm/month)')
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(code("""# Aspect ratio on a scatter plot with CHIRPS spatial slice
lat_slice = ds.precip.isel(time=0, longitude=slice(100, 200))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Wrong aspect – distorted map
im1 = axes[0].pcolormesh(ds.longitude[100:200], ds.latitude, lat_slice,
                          cmap='Blues', shading='auto')
axes[0].set_title('Distorted (default aspect)')
plt.colorbar(im1, ax=axes[0], label='mm')

# Correct aspect – lat/lon ≈ 1 at equator
im2 = axes[1].pcolormesh(ds.longitude[100:200], ds.latitude, lat_slice,
                          cmap='Blues', shading='auto')
axes[1].set_aspect(1.0 / np.cos(np.deg2rad(9)))  # ≈1.01 near equator
axes[1].set_title('Corrected aspect (cos(lat))')
plt.colorbar(im2, ax=axes[1], label='mm')

for ax in axes:
    ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## 7.6 Spines and Borders

Spines are the lines connecting the axes ticks. You can move, hide, or style them
individually for creative effects.
"""))

    cells.append(code("""fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Default spines
axes[0,0].plot(months, monthly_mean, 'o-', color='steelblue')
axes[0,0].set_title('Default spines')

# Hide top and right
axes[0,1].plot(months, monthly_mean, 'o-', color='steelblue')
axes[0,1].spines['top'].set_visible(False)
axes[0,1].spines['right'].set_visible(False)
axes[0,1].set_title('Hide top & right')

# Coloured spines
axes[1,0].plot(months, monthly_mean, 'o-', color='darkgreen', linewidth=2)
axes[1,0].spines['left'].set_color('darkgreen')
axes[1,0].spines['left'].set_linewidth(2)
axes[1,0].spines['bottom'].set_color('darkgreen')
axes[1,0].spines['bottom'].set_linewidth(2)
axes[1,0].spines['top'].set_visible(False)
axes[1,0].spines['right'].set_visible(False)
axes[1,0].set_title('Coloured spines')

# Offset spine
axes[1,1].plot(months, monthly_mean, 'o-', color='steelblue')
axes[1,1].spines['left'].set_position(('outward', 10))
axes[1,1].spines['bottom'].set_position(('outward', 10))
axes[1,1].spines['top'].set_visible(False)
axes[1,1].spines['right'].set_visible(False)
axes[1,1].set_title('Offset spines (10 pts)')

for ax in axes.flat:
    ax.set_ylabel('Precip (mm/month)')
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout(); plt.show()
"""))

    cells.append(code("""# Advanced spine customisation – "Matplotlib styled" plot
fig, ax = plt.subplots(figsize=(10, 5))

ax.fill_between(months, monthly_mean, alpha=0.3, color='coral')
ax.plot(months, monthly_mean, 'o-', color='darkred', linewidth=2, markersize=6)

# Custom spine
for spine_name in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine_name].set_linewidth(1.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 15))
ax.spines['bottom'].set_position(('outward', 10))

ax.set_title('Polished spines – clean, offset, no top/right')
ax.set_ylabel('Precipitation (mm/month)')
ax.set_xlabel('Month')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout(); plt.show()
"""))

    cells.append(md("""---
## Exercises – Module 07

1. **Axis limits**: Create a line plot of **Mekelle** rainfall from 2015–2020 only, with
   y-limits set to show only the 0–300 mm range.

2. **Tick locators**: For the monthly climatology, set x-axis ticks at every 2nd month and
   y-axis major ticks every 25 mm with minor ticks every 5 mm.

3. **Tick formatters**: Create a bar chart where y-tick labels show "XX mm" (with units)
   using `FormatStrFormatter`.

4. **Logarithmic scale**: Create a histogram of all CHIRPS rainfall data (all grid cells,
   one time step) using a log y-scale. What shape does the distribution have?

5. **Secondary axis**: Plot the Addis Ababa climatology with mm on the left and inches on the
   right using `ax.twinx()` and the `secondary_yaxis` functions approach.

6. **Aspect ratio**: Create a `pcolormesh` map of CHIRPS rainfall for January 2021 over
   Ethiopia with the correct latitude-adjusted aspect ratio.

7. **Spines**: Reproduce the "polished spines" example for the Addis Ababa time series
   (2000–2010) — hide top/right, offset left/bottom, colour the bottom spine blue.

### Mini-Project: Professional Axes for a Spatial-Temporal Analysis

Create a 2×2 figure that demonstrates different axes customisations:
- **Top-left**: Time series for Addis Ababa (1981–2022) with:
  - X-axis: YearLocator + YearFormatter
  - Y-axis: MultipleLocator(50), minor ticks every 10 mm
  - Spines: hide top/right, offset left/bottom by 10 pt
- **Top-right**: Bar chart of monthly climatology with:
  - Secondary y-axis in inches on the right
  - FuncFormatter on y-axis that adds "mm" suffix
- **Bottom-left**: Scatter of Gondar vs Addis Ababa monthly rainfall with:
  - aspect='equal'
  - x-limits and y-limits set to the same range
  - 1:1 reference line
- **Bottom-right**: pcolormap of January 2022 rainfall with:
  - Correct aspect ratio
  - Colourbar with formatted tick labels
"""))

    cells.append(code("""# Mini-Project starter
from matplotlib.dates import YearLocator, YearFormatter

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Top-left: Time series
ax = axes[0,0]
ax.plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
ax.xaxis.set_major_locator(YearLocator(5))
ax.xaxis.set_major_formatter(YearFormatter())
ax.yaxis.set_major_locator(MultipleLocator(50))
ax.yaxis.set_minor_locator(MultipleLocator(10))
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_position(('outward', 10)); ax.spines['bottom'].set_position(('outward', 10))
ax.set_title('Time Series (1981–2022)'); ax.set_ylabel('mm/month')
ax.grid(True, which='both', alpha=0.2)

# Top-right: Climatology with secondary axis
ax = axes[0,1]
ax.bar(months, monthly_mean, color='steelblue', alpha=0.7)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.0f} mm'))
ax2 = ax.secondary_yaxis('right', functions=(lambda x: x/25.4, lambda x: x*25.4))
ax2.set_ylabel('Inches')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_title('Climatology with Dual Units'); ax.tick_params(axis='x', rotation=45)

# Bottom-left: Gondar vs Addis scatter
gondar = ds.precip.isel(latitude=252, longitude=150).values
addis  = ds.precip.isel(latitude=180, longitude=174).values
ax = axes[1,0]
ax.scatter(gondar, addis, s=4, alpha=0.3, color='darkgreen')
ax.set_aspect('equal')
lim = [0, max(gondar.max(), addis.max())]
ax.set_xlim(lim); ax.set_ylim(lim)
ax.plot(lim, lim, 'r--', linewidth=0.8)
ax.set_xlabel('Gondar (mm/month)'); ax.set_ylabel('Addis Ababa (mm/month)')
ax.set_title('Gondar vs Addis Ababa')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)

# Bottom-right: Spatial map
jan22 = ds.precip.isel(time=ds.time.dt.year == 2022, time=ds.time.dt.month == 1).squeeze()
ax = axes[1,1]
im = ax.pcolormesh(ds.longitude, ds.latitude, jan22, cmap='Blues', shading='auto')
ax.set_aspect(1.0 / np.cos(np.deg2rad(9)))
ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
ax.set_title('CHIRPS – January 2022')
cbar = plt.colorbar(im, ax=ax, format=FuncFormatter(lambda v, _: f'{v:.0f} mm'))
cbar.set_label('Precipitation (mm)')

plt.tight_layout()
plt.show()
"""))

    save_nb("07_axes_customization.ipynb", cells)

# ──────────────────────── NOTEBOOK 08 ────────────────────────
def make_08():
    cells = []

    cells.append(md("""# Module 08: Multiple Plots and Layouts
**CHIRPS Rainfall Data – Ethiopia**

Combine multiple views of the same dataset in a single figure using subplots,
GridSpec, inset axes, twin axes, and automatic layout management.
"""))

    cells.append(code("""import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.dates import YearLocator, YearFormatter

ds = xr.open_dataset(r'../chirps_1981_2022.nc', engine='netcdf4')
ts = ds.precip.isel(latitude=180, longitude=174)
ts_df = pd.DataFrame({'precip': ts.values}, index=pd.DatetimeIndex(ts.time.values))
monthly_mean = ts_df.groupby(ts_df.index.month)['precip'].mean()
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
print("Data loaded")
"""))

    cells.append(md("""---
## 8.1 Basic Subplots with `plt.subplots`

The simplest way to create multiple panels is:
`fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))`

`axes` is a 2D array of Axes objects.
"""))

    cells.append(code("""fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Full time series
axes[0,0].plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
axes[0,0].set_title('Full Time Series')
axes[0,0].set_ylabel('mm/month')

# Zoom 2000–2010
axes[0,1].plot(ts_df.index, ts_df['precip'], linewidth=0.8, color='coral')
axes[0,1].set_xlim(pd.Timestamp('2000-01-01'), pd.Timestamp('2010-12-01'))
axes[0,1].set_title('2000–2010 Zoom')
axes[0,1].set_ylabel('mm/month')

# Climatology
axes[1,0].bar(months, monthly_mean, color='mediumseagreen')
axes[1,0].set_title('Monthly Climatology')
axes[1,0].set_ylabel('mm/month')
axes[1,0].tick_params(axis='x', rotation=45)

# Histogram
axes[1,1].hist(ts_df['precip'], bins=40, color='steelblue', edgecolor='white')
axes[1,1].set_title('Rainfall Distribution')
axes[1,1].set_xlabel('mm/month')
axes[1,1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()
"""))

    cells.append(md("""---
## 8.2 GridSpec for Complex Layouts

`GridSpec` gives you fine control over subplot placement, including
spans (rows/columns that cover multiple cells), varying sizes, and
custom positioning.
"""))

    cells.append(code("""fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3,
                       width_ratios=[2, 1, 1], height_ratios=[1, 1, 1.5])

# Row 0 spans: time series across whole top
ax0 = fig.add_subplot(gs[0, :])
ax0.plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
ax0.set_title('CHIRPS Addis Ababa – Full Record (1981–2022)')
ax0.set_ylabel('mm/month')

# Row 1: climatology bar, histogram, seasonal pie
ax1 = fig.add_subplot(gs[1, 0])
ax1.bar(months, monthly_mean, color='royalblue')
ax1.set_title('Climatology')
ax1.tick_params(axis='x', rotation=45)

ax2 = fig.add_subplot(gs[1, 1])
ax2.hist(ts_df['precip'], bins=30, color='mediumseagreen', edgecolor='white')
ax2.set_title('Distribution')
ax2.set_xlabel('mm/month')

ts_df['season'] = ts_df.index.month.map({12:'DJF',1:'DJF',2:'DJF',
                                          3:'MAM',4:'MAM',5:'MAM',
                                          6:'JJA',7:'JJA',8:'JJA',
                                          9:'SON',10:'SON',11:'SON'})
seasonal = ts_df.groupby('season')['precip'].sum()[['DJF','MAM','JJA','SON']]
ax3 = fig.add_subplot(gs[1, 2])
ax3.pie(seasonal, labels=seasonal.index, autopct='%1.0f%%')
ax3.set_title('Seasonal')

# Row 2: map spans 2 cols, 1 col for scatter
lat_slice = ds.precip.isel(time=0)
ax4 = fig.add_subplot(gs[2, :2])
im = ax4.pcolormesh(ds.longitude, ds.latitude, lat_slice, cmap='Blues', shading='auto')
ax4.set_title('CHIRPS – January 1981 Rainfall')
ax4.set_xlabel('Longitude'); ax4.set_ylabel('Latitude')
plt.colorbar(im, ax=ax4, label='mm/month', shrink=0.8)

ax5 = fig.add_subplot(gs[2, 2])
precip = ts_df['precip'].values
ax5.scatter(precip[:-1], precip[1:], s=5, alpha=0.3, color='darkgreen')
ax5.plot([0, precip.max()], [0, precip.max()], 'r--', linewidth=0.8)
ax5.set_title('Lag-1 Scatter')
ax5.set_xlabel('t (mm)'); ax5.set_ylabel('t+1 (mm)')
ax5.set_aspect('equal')

plt.tight_layout()
plt.show()
"""))

    cells.append(md("""---
## 8.3 Shared Axes (`sharex`, `sharey`)

Sharing axes ensures that subplots have identical scales, making
comparison easier. Use `sharex=True` / `sharey=True` or `'row'` / `'col'`.
"""))

    cells.append(code("""# Shared x-axis – compare two locations
gondar = ds.precip.isel(latitude=252, longitude=150)
gondar_df = pd.DataFrame({'precip': gondar.values}, index=pd.DatetimeIndex(gondar.time.values))

fig, axes = plt.subplots(2, 1, figsize=(14, 6), sharex=True, sharey=True)

axes[0].plot(ts_df.index, ts_df['precip'], linewidth=0.5, color='steelblue')
axes[0].set_ylabel('Addis (mm/month)')
axes[0].axhline(ts_df['precip'].mean(), color='steelblue', linestyle='--', linewidth=0.5)

axes[1].plot(gondar_df.index, gondar_df['precip'], linewidth=0.5, color='darkorange')
axes[1].set_ylabel('Gondar (mm/month)')
axes[1].axhline(gondar_df['precip'].mean(), color='darkorange', linestyle='--', linewidth=0.5)
axes[1].set_xlabel('Date')

fig.suptitle('Shared X and Y Axes – Addis Ababa vs Gondar', fontsize=13)
plt.tight_layout()
plt.show()
"""))

    cells.append(code("""# sharex='col', sharey='row'
locations = {
    'Addis Ababa': (180, 174),
    'Gondar':      (252, 150),
    'Mekelle':     (270, 190),
}

fig, axes = plt.subplots(len(locations), 2, figsize=(14, 9),
                         sharex='col', sharey='col')

for i, (name, (li, lo)) in enumerate(locations.items()):
    serie = ds.precip.isel(latitude=li, longitude=lo)
    ts_loc = pd.DataFrame({'precip': serie.values}, index=pd.DatetimeIndex(serie.time.values))
    clim = ts_loc.groupby(ts_loc.index.month)['precip'].mean()

    # Time series (column 0)
    axes[i,0].plot(ts_loc.index, ts_loc['precip'], linewidth=0.4)
    axes[i,0].set_ylabel(f'{name}\\n(mm/month)', fontsize=9)

    # Climatology (column 1)
    axes[i,1].bar(months, clim, color='steelblue', alpha=0.7)
    axes[i,1].tick_params(axis='x', rotation=45)

axes[0,0].set_title('Time Series'); axes[0,1].set_title('Climatology')
axes[-1,0].set_xlabel('Date'); axes[-1,1].set_xlabel('Month')
plt.tight_layout()
plt.show()
"""))

    cells.append(md("""---
## 8.4 Inset Plots

Inset plots place a smaller axes inside the main axes, useful for
zooming into a region of interest or showing detail.
Use `ax.inset_axes([x0, y0, width, height])` in figure coordinates.
"""))

    cells.append(code("""fig, ax = plt.subplots(figsize=(14, 5))

# Main plot – full time series
ax.plot(ts_df.index, ts_df['precip'], linewidth=0.6, color='steelblue')
ax.set_title('CHIRPS Addis Ababa – Full Record with Inset Zoom')
ax.set_ylabel('Precipitation (mm/month)')
ax.set_xlabel('Date')

# Inset – zoom on 1997 (strong El Niño year)
ax_inset = ax.inset_axes([0.15, 0.55, 0.25, 0.35])
year97 = ts_df.loc['1997']
ax_inset.plot(year97.index, year97['precip'], 'o-', color='coral', markersize=4)
ax_inset.set_title('1997 (El Niño)', fontsize=10)
ax_inset.set_ylabel('mm/month', fontsize=8)
ax_inset.tick_params(labelsize=7)

# Mark the zoomed region
ax.indicate_inset_zoom(ax_inset, edgecolor='gray')

plt.tight_layout()
plt.show()
"""))

    cells.append(code("""# Inset showing the histogram alongside a time series
fig, ax = plt.subplots(figsize=(14, 5))

ax.plot(ts_df.index, ts_df['precip'], linewidth=0.6, color='steelblue')
ax.set_title('Time Series with Embedded Histogram')
ax.set_ylabel('Precipitation (mm/month)')

# Inset histogram
ax_hist = ax.inset_axes([0.72, 0.55, 0.25, 0.35])
ax_hist.hist(ts_df['precip'], bins=30, color='mediumseagreen', edgecolor='white', orientation='horizontal')
ax_hist.set_title('Distribution', fontsize=9)
ax_hist.set_xlabel('Count', fontsize=8)
ax_hist.tick_params(labelsize=7)
ax_hist.axhline(ts_df['precip'].mean(), color='red', linestyle='--', linewidth=0.8)

plt.tight_layout()
plt.show()
"""))

    cells.append(md("""---
## 8.5 Twin Axes

`ax.twinx()` and `ax.twiny()` create a second axes that shares the
same x or y axis but with an independent scale on the opposite side.
"""))

    cells.append(code("""fig, ax1 = plt.subplots(figsize=(12, 5))

# Primary: monthly rainfall
ax1.bar(months, monthly_mean, color='steelblue', alpha=0.6, label='Mean rainfall')
ax1.set_ylabel('Precipitation (mm/month)', color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')

# Secondary: coefficient of variation
monthly_std = ts_df.groupby(ts_df.index.month)['precip'].std()
monthly_cv = monthly_std / monthly_mean * 100  # CV in %

ax2 = ax1.twinx()
ax2.plot(months, monthly_cv, 'o-', color='darkred', linewidth=2, markersize=6, label='CV (%)')
ax2.set_ylabel('Coefficient of Variation (%)', color='darkred')
ax2.tick_params(axis='y', labelcolor='darkred')

ax1.set_xlabel('Month')
ax1.set_title('Twinx: Mean Rainfall (bars) vs Coefficient of Variation (line)')
ax1.tick_params(axis='x', rotation=45)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.show()
"""))

    cells.append(md("""---
## 8.6 Layout Management

Matplotlib offers several layout engines:
- `plt.tight_layout()` – adjusts subplot params automatically
- `constrained_layout=True` – set when creating the figure; more robust
- `figure.subplots_adjust()` – manual control (left, right, top, bottom, wspace, hspace)
"""))

    cells.append(code("""# Compare tight_layout vs constrained_layout vs no layout

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for i, ax in enumerate(axes.flat):
    ax.plot(ts_df.index[:120], ts_df['precip'][:120])
    ax.set_title(f'Panel {i+1}', fontsize=14)
    ax.set_xlabel('Long label that might get cut off')
    ax.set_ylabel('Precipitation (mm/month)')

plt.tight_layout(pad=2.0)
fig.suptitle('tight_layout(pad=2.0)', y=1.02, fontsize=13)
plt.show()
"""))

    cells.append(code("""# constrained_layout
fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
for i, ax in enumerate(axes.flat):
    ax.plot(ts_df.index[:120], ts_df['precip'][:120])
    ax.set_title(f'Panel {i+1}', fontsize=14)
    ax.set_xlabel('This label will not get cut off')
    ax.set_ylabel('Precipitation (mm/month)')

fig.suptitle('constrained_layout=True', fontsize=13)
plt.show()
"""))

    cells.append(code("""# Manual subplots_adjust
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for i, ax in enumerate(axes.flat):
    ax.plot(ts_df.index[:120], ts_df['precip'][:120])
    ax.set_title(f'Panel {i+1}')
    ax.set_xlabel('X label'); ax.set_ylabel('Y label')

fig.subplots_adjust(left=0.1, right=0.95, top=0.92, bottom=0.1, wspace=0.25, hspace=0.3)
fig.suptitle('Manual subplots_adjust', fontsize=13, y=0.98)
plt.show()
"""))

    cells.append(md("""---
## 8.7 Multi-Panel CHIRPS Analysis Figure

A real-world example combining multiple views of CHIRPS data:
map + time series + histogram + seasonal breakdown.
"""))

    cells.append(code("""# Extract data for several locations
locations = {
    'Addis Ababa': (180, 174),
    'Gondar':      (252, 150),
    'Mekelle':     (270, 190),
}

fig = plt.figure(figsize=(16, 12))
gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[1.2, 1, 1],
                       width_ratios=[1.5, 1, 1], hspace=0.3, wspace=0.3)

# (0,0) – Map of mean rainfall
ax_map = fig.add_subplot(gs[0, 0])
mean_precip = ds.precip.mean(dim='time')
im = ax_map.pcolormesh(ds.longitude, ds.latitude, mean_precip,
                       cmap='YlGnBu', shading='auto')
ax_map.set_title('Mean CHIRPS Rainfall (1981–2022)', fontsize=11)
ax_map.set_xlabel('Longitude'); ax_map.set_ylabel('Latitude')
ax_map.set_aspect(1.0 / np.cos(np.deg2rad(9)))
cbar = plt.colorbar(im, ax=ax_map, shrink=0.7)
cbar.set_label('mm/month')

# Mark locations on map
colours = ['darkred', 'darkorange', 'darkgreen']
for j, (name, (li, lo)) in enumerate(locations.items()):
    lon_val = float(ds.longitude[lo])
    lat_val = float(ds.latitude[li])
    ax_map.plot(lon_val, lat_val, marker='D', color=colours[j], markersize=6)
    ax_map.text(lon_val + 0.5, lat_val, name, fontsize=8, color=colours[j])

# (0,1:3) – Time series for all locations
ax_ts = fig.add_subplot(gs[0, 1:])
for j, (name, (li, lo)) in enumerate(locations.items()):
    serie = ds.precip.isel(latitude=li, longitude=lo)
    ax_ts.plot(serie.time, serie, linewidth=0.4, color=colours[j], label=name, alpha=0.8)
ax_ts.set_title('Monthly Rainfall Comparison', fontsize=11)
ax_ts.set_ylabel('Precipitation (mm/month)')
ax_ts.legend(fontsize=9, ncol=3)
ax_ts.xaxis.set_major_locator(YearLocator(5))
ax_ts.xaxis.set_major_formatter(YearFormatter())

# (1,0) – Histogram Addis
ax_hist = fig.add_subplot(gs[1, 0])
ax_hist.hist(ts_df['precip'], bins=40, color='steelblue', edgecolor='white')
ax_hist.axvline(ts_df['precip'].mean(), color='red', ls='--')
ax_hist.set_title('Addis Rainfall Distribution', fontsize=10)
ax_hist.set_xlabel('mm/month'); ax_hist.set_ylabel('Count')

# (1,1) – Climatology Addis
ax_clim = fig.add_subplot(gs[1, 1])
ax_clim.bar(months, monthly_mean, color='steelblue')
ax_clim.set_title('Addis Climatology', fontsize=10)
ax_clim.tick_params(axis='x', rotation=45, labelsize=8)

# (1,2) – Seasonal pie Addis
ax_pie = fig.add_subplot(gs[1, 2])
seasonal = ts_df.groupby('season')['precip'].sum()[['DJF','MAM','JJA','SON']]
ax_pie.pie(seasonal, labels=seasonal.index, autopct='%1.0f%%',
           colors=['cornflowerblue','lightgreen','gold','lightcoral'])
ax_pie.set_title('Addis Seasonal Split', fontsize=10)

# (2,0) – Gondar vs Addis scatter
gondar_ts = ds.precip.isel(latitude=252, longitude=150).values
ax_scatter = fig.add_subplot(gs[2, 0])
ax_scatter.scatter(gondar_ts, ts_df['precip'].values, s=4, alpha=0.2, color='darkgreen')
ax_scatter.set_aspect('equal')
lim = [0, max(gondar_ts.max(), ts_df['precip'].max())]
ax_scatter.set_xlim(lim); ax_scatter.set_ylim(lim)
ax_scatter.plot(lim, lim, 'r--', linewidth=0.5)
ax_scatter.set_xlabel('Gondar (mm/month)')
ax_scatter.set_ylabel('Addis (mm/month)')
ax_scatter.set_title('Gondar vs Addis', fontsize=10)

# (2,1) – Mekelle time series 2015-2020
mekelle = ds.precip.isel(latitude=270, longitude=190)
mekelle_df = pd.DataFrame({'precip': mekelle.values}, index=pd.DatetimeIndex(mekelle.time.values))
sub_mek = mekelle_df.loc['2015':'2020']
ax_mek = fig.add_subplot(gs[2, 1])
ax_mek.plot(sub_mek.index, sub_mek['precip'], 'o-', color='darkorange', markersize=2, linewidth=0.6)
ax_mek.set_title('Mekelle 2015–2020', fontsize=10)
ax_mek.set_xlabel('Date'); ax_mek.set_ylabel('mm/month')

# (2,2) – CV bar chart
monthly_std_all = ts_df.groupby(ts_df.index.month)['precip'].std()
cv = monthly_std_all / monthly_mean * 100
ax_cv = fig.add_subplot(gs[2, 2])
ax_cv.bar(months, cv, color='lightcoral')
ax_cv.set_title('Addis CV (%)', fontsize=10)
ax_cv.set_ylabel('CV (%)'); ax_cv.tick_params(axis='x', rotation=45, labelsize=8)

fig.suptitle('CHIRPS Ethiopia – Multi-Panel Analysis', fontsize=15, fontweight='bold', y=1.01)
plt.show()
"""))

    cells.append(md("""---
## Exercises – Module 08

1. **Subplots basic**: Create a 3×1 figure showing the time series for **Addis Ababa**,
   **Gondar**, and **Mekelle** stacked vertically with shared x-axis.

2. **GridSpec**: Create a figure with a map of mean CHIRPS rainfall on the left (spanning
   full height) and three time series panels stacked on the right.

3. **Shared axes**: Plot monthly climatologies for 4 Ethiopian cities in a 2×2 grid with
   shared y-axis (`sharey='row'` or `sharey=True`).

4. **Inset plots**: Create a time series for Addis Ababa (1981–2022) with an inset that
   zooms into the 1984–1985 drought period.

5. **Twin axes**: Create a plot showing **mean rainfall** (bars) and **number of wet months
   > 100 mm** (line) per decade. Use `twinx`.

6. **Layout management**: Create a 3×3 subplot figure and compare `tight_layout(pad=1)`,
   `constrained_layout=True`, and `subplots_adjust(hspace=0.4, wspace=0.4)`.

### Mini-Project: Comprehensive CHIRPS Dashboard

Create a dashboard-style figure with **4 panels** using `GridSpec`:
- **Panel 1** (top, full width): Map of mean annual CHIRPS rainfall with location markers
  for 5 Ethiopian cities. Include a colourbar.
- **Panel 2** (bottom-left): Time series for two cities (Addis + one of your choice) on
  the same axes with a legend.
- **Panel 3** (bottom-centre): Side-by-side monthly climatologies (grouped bar chart) for
  the same two cities.
- **Panel 4** (bottom-right): Histogram of monthly rainfall for both cities with
  transparent overlapping bars.

Use `constrained_layout=True`, professional styling ('seaborn-v0_8'), and
include proper labels, titles, and colour coding consistent across panels.
"""))

    cells.append(code("""# Mini-Project starter
import matplotlib.patches as mpatches

plt.style.use('seaborn-v0_8')

fig = plt.figure(figsize=(16, 12), constrained_layout=True)
gs = gridspec.GridSpec(2, 3, figure=fig, height_ratios=[1.2, 1])

# Panel 1 – Map (spans top row)
ax_map = fig.add_subplot(gs[0, :])
mean_precip = ds.precip.mean(dim='time')
im = ax_map.pcolormesh(ds.longitude, ds.latitude, mean_precip,
                       cmap='YlGnBu', shading='auto')
ax_map.set_aspect(1.0 / np.cos(np.deg2rad(9)))
ax_map.set_title('Mean CHIRPS Rainfall (1981–2022)', fontsize=13, fontweight='bold')
ax_map.set_xlabel('Longitude'); ax_map.set_ylabel('Latitude')
cbar = plt.colorbar(im, ax=ax_map, shrink=0.6)
cbar.set_label('Precipitation (mm/month)')

# Location data
city_data = [
    ('Addis Ababa', 180, 174, 'darkred'),
    ('Gondar', 252, 150, 'darkorange'),
    ('Mekelle', 270, 190, 'darkgreen'),
    ('Dire Dawa', 192, 237, 'purple'),
    ('Jimma', 8, 144, 'teal'),
]

for name, li, lo, col in city_data:
    lon_val, lat_val = float(ds.longitude[lo]), float(ds.latitude[li])
    ax_map.plot(lon_val, lat_val, 'D', color=col, markersize=7, zorder=5)
    ax_map.text(lon_val + 0.4, lat_val, name, fontsize=9, color=col, fontweight='bold', zorder=5)

# Panel 2 – Time series (bottom-left)
ax_ts = fig.add_subplot(gs[1, 0])
for name, li, lo, col in city_data[:2]:
    serie = ds.precip.isel(latitude=li, longitude=lo)
    ax_ts.plot(serie.time, serie, linewidth=0.4, color=col, label=name, alpha=0.8)
ax_ts.set_title('Monthly Rainfall Comparison', fontsize=11)
ax_ts.set_xlabel('Date'); ax_ts.set_ylabel('Precipitation (mm/month)')
ax_ts.legend(fontsize=9)
ax_ts.xaxis.set_major_locator(YearLocator(5))

# Panel 3 – Grouped bar (bottom-centre)
ax_bar = fig.add_subplot(gs[1, 1])
width = 0.35
x = np.arange(12)
for i, (name, li, lo, col) in enumerate(city_data[:2]):
    serie = ds.precip.isel(latitude=li, longitude=lo)
    clim = serie.groupby('time.month').mean()
    ax_bar.bar(x + i*width, clim, width, color=col, label=name, alpha=0.8)
ax_bar.set_xticks(x + width/2)
ax_bar.set_xticklabels(months, rotation=45, fontsize=8)
ax_bar.set_title('Monthly Climatology', fontsize=11)
ax_bar.set_ylabel('Precipitation (mm/month)')
ax_bar.legend(fontsize=9)

# Panel 4 – Histogram (bottom-right)
ax_hist = fig.add_subplot(gs[1, 2])
for name, li, lo, col in city_data[:2]:
    serie = ds.precip.isel(latitude=li, longitude=lo)
    ax_hist.hist(serie.values, bins=40, alpha=0.5, color=col, label=name)
ax_hist.set_title('Rainfall Distribution', fontsize=11)
ax_hist.set_xlabel('Precipitation (mm/month)')
ax_hist.set_ylabel('Frequency')
ax_hist.legend(fontsize=9)

plt.show()
plt.style.use('default')
"""))

    save_nb("08_multiple_plots.ipynb", cells)

if __name__ == "__main__":
    make_05()
    make_06()
    make_07()
    make_08()
    print("\nAll notebooks generated successfully!")
