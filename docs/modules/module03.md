---
title: Module 3 — Jupyter Notebook Essentials
---

# Module 3: Jupyter Notebook Essentials

This module covers the fundamentals of Jupyter Notebook for interactive data visualization.

---

## Learning Objectives

- Understand the Jupyter Notebook interface and cell types
- Use Markdown and code cells effectively
- Execute Python code and visualize output inline
- Use keyboard shortcuts for efficient workflows
- Export notebooks to different formats

---

## Jupyter Interface

### Cell Types

1. **Code cells** — Execute Python code; output appears below
2. **Markdown cells** — Rich text formatting with LaTeX math support
- **Raw cells** — Unformatted text

### Modes

- **Command mode** (blue border) — keyboard shortcuts for notebook-level actions
- **Edit mode** (green border) — typing into cells

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Shift+Enter | Run cell and select below |
| Ctrl+Enter | Run cell in-place |
| Alt+Enter | Run cell and insert below |
| A / B | Insert cell above / below |
| D D | Delete cell |
| M / Y | Toggle Markdown / Code |
| Up / Down | Navigate cells |

---

## Inline Plotting

```python
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
plt.show()
```

### Matplotlib Backends

| Backend | Use Case |
|---------|----------|
| inline | Static images in notebooks |
| notebook | Interactive widgets |
| widget | Jupyter Widgets integration |
| qtagg / tkagg | Desktop pop-up windows |

---

## Magic Commands

```python
%timeit        # Time execution
%time          # Single-run timing
%who           # List variables
%matplotlib    # Set backend
%load          # Load file into cell
%run           # Run Python script
%%writefile    # Write cell to file
```

---

## Exercises

1. Create a notebook with one Markdown and one code cell
2. Use %timeit to benchmark a NumPy operation
3. Export your notebook as HTML
4. Write a cell with LaTeX:  = mc^2$

---

## Next Steps

Proceed to {doc}`module04` to learn Matplotlib fundamentals.
