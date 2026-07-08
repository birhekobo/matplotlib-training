---
title: Module 14 — Advanced Matplotlib
---

# Module 14: Advanced Matplotlib

Explore advanced features: object-oriented architecture, custom artists, animations, interactive plots, and performance optimisation.

---

## Learning Objectives

- Understand the Artist layer architecture
- Create custom artists and transforms
- Build animations with FuncAnimation
- Create interactive plots with widgets
- Optimise performance for large datasets

---

## Artists

```python
from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D

fig, ax = plt.subplots()
circle = Circle((0.5, 0.5), 0.2, color='steelblue', alpha=0.5)
ax.add_patch(circle)
```

---

## Animations

```python
from matplotlib.animation import FuncAnimation

def animate(frame):
    ax.clear()
    ax.plot(x[:frame], y[:frame])
    return ax

anim = FuncAnimation(fig, animate, frames=100, interval=50)
```

---

## Widgets

```python
from matplotlib.widgets import Slider, Button

ax_slider = fig.add_axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Threshold', 0, 100, valinit=50)
slider.on_changed(update)
```

---

## Exercises

1. Create a custom artist that draws a rainfall gauge
2. Build an animation of 12 months of CHIRPS rainfall
3. Add a slider to control the time step of a map
4. Optimise a scatter plot of 1 million points

---

## Next Steps

Proceed to {doc}`module15` for publication-quality figures.
