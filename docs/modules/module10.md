---
title: Module 10 — Scientific Visualisation
---

# Module 10: Scientific Visualisation

Explore advanced scientific visualisation techniques including contour plots, surface plots, vector fields, and 3D visualisation.

---

## Learning Objectives

- Create contour and filled contour plots
- Build 3D surface and wireframe plots
- Visualise vector fields with quiver plots
- Use colour maps effectively for scientific data
- Annotate scientific figures with colour bars

---

## Contour Plots

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, ax = plt.subplots()
contour = ax.contour(X, Y, Z, levels=10, colors='black')
ax.clabel(contour, inline=True, fontsize=8)
filled = ax.contourf(X, Y, Z, levels=20, cmap='RdBu_r')
fig.colorbar(filled, ax=ax)
```

---

## 3D Surface Plots

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0)
fig.colorbar(surf, ax=ax)
```

---

## Vector Fields

```python
U = np.sin(X) * np.cos(Y)
V = np.cos(X) * np.sin(Y)
ax.quiver(X[::5, ::5], Y[::5, ::5], U[::5, ::5], V[::5, ::5])
```

---

## Exercises

1. Create a contour map of CHIRPS rainfall over Ethiopia
2. Make a 3D surface plot of the rainfall topography
3. Add contour labels and custom levels
4. Create a multi-panel figure with different visualisation types

---

## Next Steps

Proceed to {doc}`module11` to learn time series visualisation.
