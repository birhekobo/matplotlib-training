---
title: Module 9 — Statistical Visualisation
---

# Module 9: Statistical Visualisation

Explore statistical plotting techniques: box plots, violin plots, trend analysis with confidence intervals, and correlation heatmaps.

---

## Learning Objectives

- Create box plots to show distribution spread
- Use violin plots for detailed distribution shapes
- Perform linear trend analysis with confidence bands
- Generate correlation heatmaps
- Understand statistical uncertainty in visualisations

---

## Box Plot

```python
fig, ax = plt.subplots(figsize=(12, 6))
ax.boxplot(monthly_data, labels=['Jan', 'Feb', ...])
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Monthly Rainfall Distribution')
```

---

## Violin Plot

```python
fig, ax = plt.subplots(figsize=(8, 6))
ax.violinplot(seasonal_data, positions=[1, 2, 3, 4])
ax.set_xticklabels(['DJF', 'MAM', 'JJA', 'SON'])
```

---

## Trend with Confidence Intervals

```python
from scipy import stats

slope, intercept, r, p, se = stats.linregress(years, rainfall)
trend = slope * years + intercept
ax.fill_between(years, trend - ci, trend + ci, alpha=0.2)
ax.plot(years, trend, color='crimson', label=f'Trend: {slope:.1f} mm/yr')
```

---

## Correlation Heatmap

```python
import seaborn as sns
sns.heatmap(correlation_matrix, cmap='RdBu_r', vmin=-1, vmax=1)
```

---

## Exercises

1. Create box plots of monthly CHIRPS rainfall for 12 months
2. Plot a violin plot by season (DJF, MAM, JJA, SON)
3. Compute and visualise a rainfall trend with 95% CI at a point
4. Create a correlation heatmap for 5 Ethiopian cities

---

## Next Steps

Proceed to {doc}`module10` to learn scientific visualisation.
