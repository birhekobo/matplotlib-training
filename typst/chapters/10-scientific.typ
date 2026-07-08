#import "../macros.typ": note-box, warning-box, info-box
= Scientific Visualization

Scientific visualization focuses on representing physical phenomena: contour plots, vector fields, 2D color plots, and 3D surfaces.

== 2D Color Plots (pcolormesh and imshow)

=== pcolormesh

`pcolormesh` creates a pseudocolor plot with a rectangular grid. It is faster than `imshow` for large datasets and handles non-uniform grids.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y) * np.exp(-(X*2 + Y*2) / 6)

fig, ax = plt.subplots(figsize=(8, 6))
pcm = ax.pcolormesh(X, Y, Z, cmap='RdBu_r', shading='auto')
cbar = fig.colorbar(pcm, ax=ax, label='z')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title(r'$z = \sin(x) \cos(y) e^{-(x^2 + y^2)/6}$')
ax.set_aspect('equal')
plt.show()
```

=== imshow

`imshow` displays image data with optional interpolation:

```python
fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(Z, extent=[-3, 3, -3, 3], cmap='viridis',
               origin='lower', aspect='equal',
               interpolation='bilinear')
cbar = fig.colorbar(im, ax=ax)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('imshow with Bilinear Interpolation')
plt.show()
```

#note-box[
  Use `pcolormesh` for scientific data on non-uniform grids. Use `imshow` for uniformly sampled data or when you need image-specific features like interpolation.
]

== Contour Plots

=== Contour (Lines)

```python
fig, ax = plt.subplots(figsize=(8, 6))
contours = ax.contour(X, Y, Z, levels=15, colors='black', linewidths=0.8)
ax.clabel(contours, inline=True, fontsize=8, fmt='%.2f')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Contour Lines')
ax.set_aspect('equal')
plt.show()
```

=== Filled Contour

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Filled contours
cf = ax1.contourf(X, Y, Z, levels=20, cmap='RdBu_r')
fig.colorbar(cf, ax=ax1, label='z')
ax1.set_title('Filled Contour')
ax1.set_aspect('equal')

# Combined filled + lines
cf2 = ax2.contourf(X, Y, Z, levels=20, cmap='RdBu_r')
cs = ax2.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5)
ax2.clabel(cs, inline=True, fontsize=8)
ax2.set_title('Filled + Line Contours')
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()
```

== Streamplots (Vector Fields)

Visualizing flow fields:

```python
x = np.linspace(-2, 2, 30)
y = np.linspace(-2, 2, 30)
X, Y = np.meshgrid(x, y)
U = -Y  # Horizontal velocity
V = X   # Vertical velocity

fig, ax = plt.subplots(figsize=(8, 6))
strm = ax.streamplot(X, Y, U, V, color=np.sqrt(U*2 + V*2),
                     cmap='viridis', linewidth=1.5, density=1.5)
cbar = fig.colorbar(strm.lines, ax=ax, label='Speed')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Streamplot of Rotational Flow')
ax.set_aspect('equal')
plt.show()
```

=== Quiver Plots

```python
# Subsample for readability
step = 3
X_sub = X[::step, ::step]
Y_sub = Y[::step, ::step]
U_sub = U[::step, ::step]
V_sub = V[::step, ::step]

fig, ax = plt.subplots(figsize=(8, 6))
q = ax.quiver(X_sub, Y_sub, U_sub, V_sub,
              color='#1f77b4', alpha=0.7,
              scale=5, width=0.005)
ax.quiverkey(q, 0.9, 0.95, 2, '2 m/s', coordinates='axes')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Quiver Plot (Vector Field)')
ax.set_aspect('equal')
plt.show()
```

== 3D Plots

=== Surface Plot

```python
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
X, Y = np.meshgrid(np.linspace(-3, 3, 50), np.linspace(-3, 3, 50))
Z = np.sin(np.sqrt(X*2 + Y*2))

surf = ax.plot_surface(X, Y, Z, cmap='viridis',
                       linewidth=0, antialiased=True,
                       alpha=0.9)
fig.colorbar(surf, ax=ax, shrink=0.5, label='z')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D Surface Plot')
plt.show()
```

=== Contour Projections

```python
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
surf = ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0, alpha=0.7)
# Contour projections
ax.contour(X, Y, Z, zdir='z', offset=-1.5, cmap='viridis', levels=15)
ax.contour(X, Y, Z, zdir='x', offset=-4, cmap='viridis', levels=10)
ax.contour(X, Y, Z, zdir='y', offset=4, cmap='viridis', levels=10)
ax.set_zlim(-1.5, 1.5)
plt.show()
```

#warning-box[
  3D plots can be visually impressive but often obscure data. Use them only when the third dimension is essential. For most cases, 2D contour plots or color maps are more effective.
]

== Heatmaps

```python
# Correlation matrix heatmap
data = np.random.randn(100, 5)
corr_matrix = np.corrcoef(data.T)

fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1,
               interpolation='nearest')

# Add text annotations
labels = ['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E']
ax.set_xticks(range(5))
ax.set_yticks(range(5))
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_yticklabels(labels)

for i in range(5):
    for j in range(5):
        text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                       ha='center', va='center',
                       color='white' if abs(corr_matrix[i, j]) > 0.5 else 'black')

fig.colorbar(im, ax=ax, shrink=0.8, label='Pearson Correlation')
ax.set_title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.show()
```

== Summary

You have learned a range of scientific visualization techniques: 2D color plots, contour plots, streamlines and quivers, 3D surfaces, and heatmaps. These tools are essential for representing physical and mathematical data. In the next chapter, we focus on time series visualization.









