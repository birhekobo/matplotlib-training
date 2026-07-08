#import "../macros.typ": note-box, warning-box, info-box
= Statistical Visualization

Statistical plots help visualize distributions, summarize data, and identify patterns. This chapter covers box plots, violin plots, error bars, and confidence intervals.

== Box Plots

Box plots show the distribution of data through quartiles, outliers, and whiskers.

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in range(1, 6)]

fig, ax = plt.subplots(figsize=(8, 5))
bp = ax.boxplot(data, labels=['Group 1', 'Group 2', 'Group 3',
                                'Group 4', 'Group 5'],
                patch_artist=True, widths=0.6)

# Customize colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Customize outliers
for flier in bp['fliers']:
    flier.set(marker='o', markersize=6, alpha=0.5)

ax.set_ylabel('Values')
ax.set_title('Box Plot Comparison')
ax.grid(axis='y', alpha=0.3)
plt.show()
```

=== Box Plot Anatomy

A box plot displays:

- *Box*: Interquartile range (IQR, 25th–75th percentile)
- *Median line*: 50th percentile
- *Whiskers*: Typically 1.5 × IQR beyond the box
- *Flier points*: Data beyond the whiskers

```python
# Vertical box plot (default)
ax.boxplot(data)

# Horizontal
ax.boxplot(data, vert=False)

# Notched (shows CI of median)
ax.boxplot(data, notch=True)

# Custom whisker range
ax.boxplot(data, whis=2.0)  # 2 × IQR
```

== Violin Plots

Violin plots combine box plots with kernel density estimation:

```python
fig, ax = plt.subplots(figsize=(8, 5))
vp = ax.violinplot(data, showmeans=True, showmedians=True,
                   widths=0.7)

# Customize colors
for body in vp['bodies']:
    body.set_facecolor('#2c7bb6')
    body.set_alpha(0.6)

vp['cmeans'].set_color('#d62728')
vp['cmeans'].set_linewidth(2)
vp['cmedians'].set_color('#1a1a1a')
vp['cmedians'].set_linewidth(2)

ax.set_xticks(range(1, 6))
ax.set_xticklabels(['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5'])
ax.set_ylabel('Values')
ax.set_title('Violin Plot Comparison')
ax.grid(axis='y', alpha=0.3)
plt.show()
```

#note-box[
  Violin plots are more informative than box plots for multimodal distributions because they show the full density shape. However, they can be harder to compare across many groups.
]

== Error Bars

=== Basic Error Bars

```python
x = np.arange(1, 6)
y = [12, 18, 15, 22, 20]
y_err = [2, 3, 2.5, 4, 3]

fig, ax = plt.subplots(figsize=(8, 5))
ax.errorbar(x, y, yerr=y_err, fmt='o-', capsize=5,
            color='#1f77b4', ecolor='#d62728', elinewidth=1.5,
            markersize=8, capthick=1.5)
ax.set_xlabel('Category')
ax.set_ylabel('Measurement')
ax.set_title('Data with Error Bars')
ax.grid(alpha=0.3)
plt.show()
```

=== Asymmetric Errors

```python
y_err_lower = [1.5, 2, 1.8, 3, 2.5]
y_err_upper = [2.5, 4, 3.2, 5, 3.5]
y_err = [y_err_lower, y_err_upper]

ax.errorbar(x, y, yerr=y_err, fmt='o')
```

=== Shaded Error Regions

```python
fig, ax = plt.subplots(figsize=(8, 5))

x = np.linspace(0, 10, 50)
y_mean = np.sin(x)
y_std = 0.2 + 0.1 * np.abs(x - 5)

ax.plot(x, y_mean, 'b-', linewidth=2, label='Mean')
ax.fill_between(x, y_mean - y_std, y_mean + y_std,
                alpha=0.3, color='blue', label='±1σ')

# Multiple confidence levels
ax.fill_between(x, y_mean - 2*y_std, y_mean + 2*y_std,
                alpha=0.15, color='blue', label='±2σ')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Shaded Error Regions')
ax.legend()
plt.show()
```

== Confidence Intervals

=== Bootstrap Confidence Interval

```python
def bootstrap_ci(data, n_bootstrap=1000, ci=95):
    """Compute bootstrap confidence interval of the mean."""
    means = np.zeros(n_bootstrap)
    n = len(data)
    for i in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        means[i] = np.mean(sample)
    lower = np.percentile(means, (100 - ci) / 2)
    upper = np.percentile(means, 100 - (100 - ci) / 2)
    return lower, upper

data = np.random.normal(5, 2, 200)
lower, upper = bootstrap_ci(data, n_bootstrap=5000)
print(f"95% CI: [{lower:.2f}, {upper:.2f}]")
```

=== Visualizing Confidence Intervals

```python
fig, ax = plt.subplots(figsize=(8, 4))

groups = ['A', 'B', 'C', 'D', 'E']
means = [12, 15, 11, 18, 14]
ci_low = [1.5, 2.0, 1.8, 2.5, 1.9]
ci_high = [2.0, 2.5, 2.2, 3.0, 2.3]

x_pos = np.arange(len(groups))
ci = [means - np.array(ci_low), np.array(ci_high) - means]

ax.errorbar(x_pos, means, yerr=ci, fmt='o', capsize=5,
            capthick=2, markersize=10, color='#1f77b4')
ax.set_xticks(x_pos)
ax.set_xticklabels(groups)
ax.set_ylabel('Mean Value')
ax.set_title('Group Means with 95% Confidence Intervals')
ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax.grid(axis='y', alpha=0.3)
plt.show()
```

== Statistical Annotations

```python
from scipy import stats

# t-test example
group1 = np.random.normal(10, 2, 50)
group2 = np.random.normal(12, 2, 50)

t_stat, p_value = stats.ttest_ind(group1, group2)

fig, ax = plt.subplots(figsize=(8, 5))
ax.boxplot([group1, group2], labels=['Control', 'Treatment'])

# Annotate significance
y_max = max(group1.max(), group2.max())
ax.plot([1, 1, 2, 2], [y_max + 0.5, y_max + 1.5, y_max + 1.5, y_max + 0.5],
        'k-', linewidth=1.5)
ax.text(1.5, y_max + 1.8, f'p = {p_value:.4f}',
        ha='center', fontsize=10)

ax.set_ylabel('Measurement')
ax.set_title('Statistical Comparison')
plt.show()
```

== Summary

You have learned statistical visualization techniques: box plots for quartile summaries, violin plots for full distributions, error bars and shaded regions for uncertainty, and confidence intervals. These tools are essential for communicating statistical findings. In the next chapter, we explore scientific visualization techniques.








