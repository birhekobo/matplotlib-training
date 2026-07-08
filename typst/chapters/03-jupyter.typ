#import "../macros.typ": note-box, warning-box, info-box
= Jupyter Notebook Essentials

Jupyter Notebook provides an interactive computing environment that is ideal for data exploration, visualization development, and reproducible research. This chapter covers the essential features you will use throughout this course.

== What is Jupyter?

Jupyter Notebook is a web-based interactive development environment that combines:

- *Code cells*: Executable Python code
- *Markdown cells*: Formatted text, equations, images
- *Output cells*: Rich output including plots, tables, and interactive widgets

This combination makes Jupyter perfect for developing visualizations iteratively—you can tweak parameters, re-run cells, and immediately see the results.

== Installing and Starting Jupyter

If you followed the setup in Chapter 2, Jupyter is already installed.

```bash
jupyter notebook
```

This opens a browser window showing the notebook dashboard. Navigate to your project folder and click *New > Matplotlib Training* to create a new notebook using the kernel you registered.

#note-box[
  Use `jupyter lab` instead of `jupyter notebook` for an enhanced interface with file browser, terminal, and multiple tabs.
]

== Notebook Interface

=== Cell Types

- *Code cells*: Contain Python code. Press `Shift + Enter` to execute.
- *Markdown cells*: Contain formatted text. Double-click to edit, `Shift + Enter` to render.
- *Raw cells*: Unformatted text, useful for including LaTeX source.

=== Keyboard Shortcuts

Essential shortcuts:

| *Shortcut* | *Action* |
|---|---|
| `Shift + Enter` | Run cell and move to next |
| `Ctrl + Enter` | Run cell in place |
| `Alt + Enter` | Run cell and insert new below |
| `Esc + a` | Insert cell above |
| `Esc + b` | Insert cell below |
| `Esc + dd` | Delete cell |
| `Esc + m` | Change to Markdown cell |
| `Esc + y` | Change to Code cell |
| `Esc + h` | Show all keyboard shortcuts |

== Displaying Plots in Jupyter

=== %matplotlib Inline

This magic command renders static PNG plots directly in the notebook:

```python
%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
fig, ax = plt.subplots()
ax.plot(x, np.sin(x))
```

#info-box[
  Set `%matplotlib inline` in a cell at the top of your notebook. It affects the entire notebook session.
]

=== Configuring Output Quality

```python
%matplotlib inline
%config InlineBackend.figure_format = 'retina'  # High DPI
%config InlineBackend.figure_format = 'svg'     # Vector format
%config InlineBackend.figure_format = 'png'     # Default

# Set global figure size and DPI
plt.rcParams['figure.dpi'] = 120
plt.rcParams['figure.figsize'] = (10, 5)
```

=== Interactive Backends

For interactive plots (pan, zoom, rotate):

```python
%matplotlib notebook   # Older, but reliable
%matplotlib widget     # Requires: pip install ipympl
```

#warning-box[
  Interactive backends (`notebook` or `widget`) can conflict with `%matplotlib inline`. Use only one at a time, and restart the kernel when switching.
]

== Best Practices for Notebook-Work

=== Structure Your Notebook

1. *Title and description*: Start with a Markdown cell explaining the notebook
2. *Imports*: All imports in one cell at the top
3. *Configuration*: Matplotlib settings in one cell
4. *Data loading*: A dedicated section for loading data
5. *Analysis*: One logical step per cell
6. *Visualizations*: One figure per cell for clarity

=== Reproducibility

```python
# Set random seed for reproducibility
import numpy as np
np.random.seed(42)

# Record library versions
import matplotlib
print(f"Matplotlib: {matplotlib.__version__}")
```

=== Avoid Common Pitfalls

- Do not modify a cell and re-run it out of order — this creates inconsistencies
- Use `Kernel > Restart & Run All` to verify your notebook runs end-to-end
- Clear output before committing to version control: `Cell > All Output > Clear`

== Exporting Notebooks

Jupyter notebooks can be exported to multiple formats:

| *Format* | *Command* | *Use Case* |
|---|---|---|
| HTML | `File > Download as > HTML` | Web sharing |
| PDF | `File > Download as > PDF` | Printing |
| Python script | `File > Download as > Python` | Production scripts |
| Markdown | `File > Download as > Markdown` | Documentation |

```bash
# Command line conversion
jupyter nbconvert --to html notebook.ipynb
jupyter nbconvert --to python notebook.ipynb
jupyter nbconvert --to pdf notebook.ipynb  # Requires LaTeX
```

== Summary

Jupyter Notebook is your primary environment for developing and experimenting with Matplotlib visualizations. You learned how to create notebooks, run cells, display plots, and follow reproducible workflows. In the next chapter, we dive into Matplotlib's core architecture.








