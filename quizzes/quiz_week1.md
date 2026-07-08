# Week 1 Quiz — Introduction & Setup & Matplotlib Basics

**Instructions:** Answer each question to the best of your ability.

---

**1.** What command installs Matplotlib via pip?
   - a) `pip install matplotlib`
   - b) `pip install matplot`
   - c) `pip install mpl`
   - d) `conda install matplotlib`

**2.** Which import statement is the standard convention for Matplotlib?
   - a) `import matplotlib as mpl`
   - b) `import matplotlib.pyplot as plt`
   - c) `from matplotlib import *`
   - d) `import matplotlib.plot as plt`

**3.** What does `plt.plot(x, y)` return?
   - a) A Figure object
   - b) A list of Line2D objects
   - c) An Axes object
   - d) A NumPy array

**4.** Which function displays a figure in a non-interactive script?
   - a) `plt.display()`
   - b) `plt.show()`
   - c) `plt.render()`
   - d) `plt.draw()`

**5.** What is the purpose of `plt.figure(figsize=(8, 6))`?
   - a) Set the figure title
   - b) Create a figure with a specific width and height in inches
   - c) Change the default DPI
   - d) Add a new subplot

**6.** Which method adds a title to the current axes?
   - a) `ax.title("Title")`
   - b) `ax.set_title("Title")`
   - c) `plt.set_title("Title")`
   - d) `ax.title.set("Title")`

**7.** How do you create a 2×2 grid of subplots?
   - a) `plt.subplot(2, 2)`
   - b) `plt.subplots(2, 2)`
   - c) `plt.subplot(2, 2, 1)`
   - d) `plt.subplots(nrows=2, ncols=2)`

**8.** What does the `label` parameter in `plt.plot(x, y, label="Data")` do?
   - a) Sets the x-axis label
   - b) Sets the legend label for the line
   - c) Sets the window title
   - d) Changes the line colour

**9.** Which function adds a legend to a plot?
   - a) `plt.legend()`
   - b) `plt.legend(show=True)`
   - c) `ax.add_legend()`
   - d) `plt.legend(labels=["Data"])`

**10.** What file format is NOT supported by `plt.savefig()`?
   - a) PNG
   - b) PDF
   - c) SVG
   - d) PSD

---

## Answer Key

| # | Answer | Notes |
|---|--------|-------|
| 1 | **a** | `pip install matplotlib` (or `conda install matplotlib` — both valid, but `pip` is the first-party option) |
| 2 | **b** | `import matplotlib.pyplot as plt` is the standard alias |
| 3 | **b** | `plt.plot` returns a list of `Line2D` objects |
| 4 | **b** | `plt.show()` renders and displays the figure |
| 5 | **b** | `figsize` sets width and height in inches |
| 6 | **b** | `ax.set_title("Title")` is the Axes method |
| 7 | **d** | `plt.subplots(2, 2)` (or equivalently `plt.subplots(nrows=2, ncols=2)`) |
| 8 | **b** | `label` sets the legend entry for the artist |
| 9 | **a** | `plt.legend()` adds the legend |
| 10 | **d** | PSD is not a supported Matplotlib output format |
