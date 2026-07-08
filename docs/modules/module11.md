---
title: Module 11 — Time Series Visualisation
---

# Module 11: Time Series Visualisation

Analyse and visualise temporal data using specialised time series techniques with Matplotlib and Pandas.

---

## Learning Objectives

- Create time series plots with proper date formatting
- Use DateFormatter and DateLocator for tick control
- Compute and visualise rolling statistics
- Handle multiple time series on shared axes
- Visualise seasonality and trends

---

## Basic Time Series

```python
import pandas as pd
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(df.index, df['precip'], linewidth=0.8)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
```

---

## Rolling Statistics

```python
df['rolling_mean'] = df['precip'].rolling(window=12, center=True).mean()
df['rolling_std'] = df['precip'].rolling(window=12).std()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(df.index, df['precip'], alpha=0.3, label='Monthly')
ax.plot(df.index, df['rolling_mean'], color='crimson', label='12-month MA')
ax.fill_between(df.index, df['rolling_mean'] - df['rolling_std'],
                df['rolling_mean'] + df['rolling_std'], alpha=0.2)
ax.legend()
```

---

## Seasonal Decomposition

```python
# Visualise the seasonal cycle
monthly_clim = df.groupby(df.index.month)['precip'].mean()
ax.plot(months, monthly_clim, marker='o')
```

---

## Exercises

1. Plot the full CHIRPS time series for Addis Ababa
2. Add a 12-month rolling mean and standard deviation
3. Create a seasonal subplot with individual years overlaid
4. Highlight El Niño years with a different colour

---

## Next Steps

Proceed to {doc}`module12` to learn geographic visualisation.
