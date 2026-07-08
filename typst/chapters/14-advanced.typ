#import "../macros.typ": note-box, warning-box, info-box
= Advanced Matplotlib

This chapter covers advanced techniques: custom artists, animations, interactive widgets, event handling, and path effects.

== Custom Artists

Create reusable custom plot elements by subclassing `Artist`:

```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.text import Text

# Custom annotation box
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot([0, 1, 2], [0, 1, 4], 'o-', color='#1f77b4')

# Custom bbox with arrow
from matplotlib.patches import FancyArrowPatch

class AnnotatedPoint:
    """Draw a point with a label and connecting arrow."""
    def __init__(self, ax, x, y, text,
                 color='#d62728', fontsize=10):
        ax.plot(x, y, 'o', color=color, markersize=8, zorder=5)
        ax.annotate(text, xy=(x, y),
                    xytext=(x + 0.5, y + 0.5),
                    arrowprops=dict(
                        arrowstyle='->',
                        color=color,
                        connectionstyle='arc3,rad=0.2'
                    ),
                    fontsize=fontsize,
                    bbox=dict(
                        boxstyle='round,pad=0.3',
                        facecolor='lightyellow',
                        edgecolor=color
                    ))

AnnotatedPoint(ax, 1, 1, 'Peak value', color='#2ca02c')
AnnotatedPoint(ax, 0, 0, 'Origin', color='#d62728')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Custom Annotations')
ax.grid(alpha=0.3)
plt.show()
```

== Path Effects

Path effects add visual enhancements like shadows, strokes, and glows:

```python
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(8, 4))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), linewidth=3,
        color='#1f77b4',
        path_effects=[pe.SimpleLineShadow(),
                      pe.Normal()])
ax.set_title('Line with Shadow Effect')
plt.show()

# Text with outline
text = ax.text(5, 0.5, 'Important Point', fontsize=14,
               ha='center',
               path_effects=[pe.withStroke(linewidth=3,
                                            foreground='white')])
```

== Animations

=== FuncAnimation

```python
import matplotlib.animation as animation

fig, ax = plt.subplots(figsize=(8, 4))
x = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x, np.sin(x), color='#1f77b4', linewidth=2)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Animated Sine Wave')
ax.grid(alpha=0.3)

def animate(frame):
    line.set_ydata(np.sin(x + frame * 0.1))
    return line,

ani = animation.FuncAnimation(
    fig, animate, frames=100,
    interval=50, blit=True
)

# Save animation
# ani.save('sine_wave.gif', writer='pillow', fps=20)
plt.show()
```

=== ArtistAnimation

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-1.5, 1.5)

artists = []
for phase in np.linspace(0, 2 * np.pi, 50):
    line, = ax.plot(x, np.sin(x + phase), color='#1f77b4')
    artists.append([line])

ani = animation.ArtistAnimation(fig, artists, interval=50, blit=True)
plt.show()
```

#info-box[
  Use `blit=True` for faster animation performance. Blit only redraws the changing elements rather than the entire figure.
]

== Interactive Widgets

Using ipywidgets with Jupyter for interactive plots:

```python
# Requires: pip install ipywidgets ipympl
# In Jupyter: %matplotlib widget

import ipywidgets as widgets
from IPython.display import display

@widgets.interact
def interactive_plot(
    amplitude=(0.1, 3.0, 0.1),
    frequency=(0.5, 5.0, 0.5),
    phase=(0, 2*np.pi, 0.1)
):
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.linspace(0, 4*np.pi, 200)
    y = amplitude * np.sin(frequency * x + phase)
    ax.plot(x, y, color='#1f77b4', linewidth=2)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Sine Wave: A={amplitude}, f={frequency}, φ={phase:.2f}')
    ax.grid(alpha=0.3)
    plt.show()
```

== Event Handling

Connect keyboard and mouse events:

```python
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(0, 10, 100)
line, = ax.plot(x, np.sin(x))
ax.set_title('Click on a point')

def on_click(event):
    if event.inaxes != ax:
        return
    ax.plot(event.xdata, event.ydata, 'ro', markersize=8)
    ax.annotate(f'({event.xdata:.2f}, {event.ydata:.2f})',
                xy=(event.xdata, event.ydata),
                xytext=(5, 5), textcoords='offset points')
    fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
```

== Custom Colormaps

```python
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

# From list of colors
colors = ['#313695', '#4575b4', '#74add1', '#abd9e9',
          '#fee090', '#fdae61', '#f46d43', '#d73027']
cmap = LinearSegmentedColormap.from_list('precip_cmap', colors)

# From a discrete list
discrete_cmap = ListedColormap(['#1f77b4', '#ff7f0e', '#2ca02c',
                                 '#d62728', '#9467bd', '#8c564b'])

# Test it
fig, ax = plt.subplots(figsize=(8, 5))
Z = np.random.randn(50, 50).cumsum(axis=0).cumsum(axis=1)
im = ax.imshow(Z, cmap=cmap)
fig.colorbar(im, ax=ax)
ax.set_title('Custom Colormap')
plt.show()
```

== Performance Tips

=== Vectorization

```python
# Slow: loop-based
for i in range(len(x)):
    y[i] = np.sin(x[i])

# Fast: vectorized
y = np.sin(x)
```

=== Use Path Collections

```python
# For many scatter points, use PathCollection
# (which is what scatter() already uses)
ax.scatter(x, y, s=1, rasterized=True)
```

=== Blitting in Animations

```python
# Enable blit for performance
ani = animation.FuncAnimation(fig, update, blit=True)
```

=== Agg Backend for Scripts

```python
import matplotlib
matplotlib.use('Agg')  # Non-interactive, fastest for scripts
```

== Summary

You have explored advanced Matplotlib techniques: custom reusable artists, path effects for visual polish, animations, interactive widgets, event-driven programming, custom colormaps, and performance optimization. These skills let you create sophisticated, interactive, and performant visualizations. In the next chapter, we focus on producing publication-quality figures.







