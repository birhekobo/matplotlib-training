---
title: Week 1 Solutions
---

# Week 1 Solutions

---

## Solution 1.1: Basic Line Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 3, 100)
y = x**3 - 3 * x**2 + 2 * x + 1

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, color='blue', linewidth=2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(r'$y = x^3 - 3x^2 + 2x + 1$')
ax.grid(alpha=0.3)
plt.show()
```

**Explanation:** We use `np.linspace` to create 100 evenly spaced points over $[-2, 3]$, compute the cubic polynomial, and plot with the object-oriented API. The grid is set to 30% opacity for a subtle background.

---

## Solution 1.2: Multiple Curves

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 4 * np.pi, 200)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.cos(x)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y1, 'r-', label=r'$\sin(x)$', linewidth=2)
ax.plot(x, y2, 'b--', label=r'$\cos(x)$', linewidth=2)
ax.plot(x, y3, 'g:', label=r'$\sin(x)\cos(x)$', linewidth=2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Multiple Trigonometric Functions')
ax.legend()
ax.grid(alpha=0.3)
fig.savefig('curves.png', dpi=150, bbox_inches='tight')
plt.show()
```

---

## Solution 1.3: Scatter Plot Matrix

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.randn(200, 3)

fig, axes = plt.subplots(3, 3, figsize=(10, 10),
                         sharex='col', sharey='row')

for i in range(3):
    for j in range(3):
        ax = axes[i, j]
        if i == j:
            ax.hist(data[:, i], bins=20, color='steelblue', edgecolor='white')
        else:
            ax.scatter(data[:, j], data[:, i], s=10, alpha=0.6, c='steelblue')

plt.suptitle('Scatter Plot Matrix', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Solution 1.4: Bar Chart with Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

np.random.seed(42)
mean_rainfall = np.random.gamma(shape=2, scale=25, size=12)
std_rainfall = np.random.uniform(5, 15, 12)

season_colors = ['#4575b4'] * 3 + ['#fee090'] * 3 + ['#d73027'] * 3 + ['#91bfdb'] * 3

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(months, mean_rainfall, yerr=std_rainfall,
              color=season_colors, edgecolor='black', capsize=5)

ax.bar_label(bars, padding=3, fmt='%.0f')
ax.set_ylabel('Rainfall (mm)')
ax.set_title('Mean Monthly Rainfall')
plt.show()
```

---

## Solution 1.5: Histogram and KDE

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

np.random.seed(42)
normal_samples = np.random.normal(5, 2, 1000)
uniform_samples = np.random.uniform(0, 10, 1000)

fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(normal_samples, bins=30, density=True, alpha=0.6,
        color='steelblue', label='Normal (μ=5, σ=2)')
ax.hist(uniform_samples, bins=30, density=True, alpha=0.4,
        color='orange', label='Uniform [0, 10]')

x = np.linspace(-2, 12, 200)
pdf = stats.norm.pdf(x, 5, 2)
ax.plot(x, pdf, 'r-', linewidth=2, label='Normal PDF')

ax.set_xlabel('Value')
ax.set_ylabel('Density')
ax.set_title('Histogram Comparison with PDF Overlay')
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

---

## Solution 1.6: Customizing Colormaps

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-np.pi, np.pi, 100)
y = np.linspace(-np.pi, np.pi, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, ax = plt.subplots(figsize=(8, 6))
pcm = ax.pcolormesh(X, Y, Z, cmap='RdBu_r', shading='auto')
contours = ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.8)
ax.clabel(contours, inline=True, fontsize=8)
cbar = fig.colorbar(pcm, ax=ax, label='z')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(r'$z = \sin(x) \cdot \cos(y)$')
plt.show()
```

---

## Solution 1.7: Figure Composition

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

fig, axes = plt.subplots(2, 2, figsize=(12, 10),
                         sharey='row', sharex='col')

x = np.linspace(0, 10, 100)
# Top-left: Line plot
axes[0, 0].plot(x, np.sin(x), color='#1f77b4')
axes[0, 0].set_title('Line Plot')
axes[0, 0].set_ylabel('y')

# Top-right: Scatter plot
axes[0, 1].scatter(np.random.randn(50), np.random.randn(50),
                   c=np.random.rand(50), s=80, alpha=0.7)
axes[0, 1].set_title('Scatter Plot')

# Bottom-left: Bar chart
categories = ['A', 'B', 'C', 'D', 'E']
values = np.random.randint(1, 10, 5)
axes[1, 0].bar(categories, values, color='#2ca02c')
axes[1, 0].set_title('Bar Chart')
axes[1, 0].set_xlabel('Category')
axes[1, 0].set_ylabel('Value')

# Bottom-right: Histogram
axes[1, 1].hist(np.random.randn(500), bins=20, color='#d62728', edgecolor='white')
axes[1, 1].set_title('Histogram')
axes[1, 1].set_xlabel('Value')

fig.suptitle('Week 1 Dashboard', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
```
