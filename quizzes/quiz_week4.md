# Week 4 Quiz — Advanced Matplotlib, NumPy/Pandas Integration, and Projects

**Instructions:** Answer each question to the best of your ability.

---

**1.** Which object in Matplotlib represents the entire window or page?
   - a) `Axes`
   - b) `Figure`
   - c) `Canvas`
   - d) `Subplot`

**2.** How do you create an animation in Matplotlib?
   - a) `plt.animation()`
   - b) `matplotlib.animation.FuncAnimation()`
   - c) `plt.animate()`
   - d) `ax.animate()`

**3.** Which method is used to update an artist's data in an animation?
   - a) `ax.plot(new_data)`
   - b) `artist.set_data(new_data)`
   - c) `artist.update(new_data)`
   - d) `ax.redraw(new_data)`

**4.** What does `ax.fill_between(x, y1, y2)` do?
   - a) Draws a vertical bar chart
   - b) Fills the area between two curves
   - c) Creates a contour plot
   - d) Fills the entire axes with colour

**5.** Which of the following is true about `plt.subplots()` vs `plt.subplot()`?
   - a) They are identical
   - b) `plt.subplots()` creates a figure and an array of axes in one call
   - c) `plt.subplot()` creates a figure and an array of axes in one call
   - d) `plt.subplots()` only works with 2×2 grids

**6.** How do you add a second y-axis to a plot?
   - a) `ax.twinx()`
   - b) `ax.second_y()`
   - c) `plt.dual_axis()`
   - d) `ax.dual_axis()`

**7.** What is the purpose of `rcParams` in Matplotlib?
   - a) Save figures in different formats
   - b) Configure global default parameters for all plots
   - c) Render plots in real-time
   - d) Create interactive widgets

**8.** Which library provides `GridSpec` for complex subplot layouts?
   - a) `matplotlib.gridspec`
   - b) `matplotlib.layout`
   - c) `matplotlib.subplots`
   - d) `matplotlib.axes_grid`

**9.** What does `pd.DataFrame.plot(kind="line")` use under the hood?
   - a) Matplotlib
   - b) Plotly
   - c) Bokeh
   - d) Altair

**10.** In a course project using real climate data, what is the first step after loading NetCDF data with xarray?
   - a) Plot all the data immediately
   - b) Inspect the dataset structure, dimensions, coordinates, and variables
   - c) Aggregate to annual means
   - d) Save to a new NetCDF file

---

## Answer Key

| # | Answer | Notes |
|---|--------|-------|
| 1 | **b** | `Figure` is the top-level container representing the window/page |
| 2 | **b** | `FuncAnimation` from `matplotlib.animation` is the standard class |
| 3 | **b** | `artist.set_data()` updates the data displayed by an artist in an animation |
| 4 | **b** | `fill_between` shades the region between the two y-values |
| 5 | **b** | `plt.subplots()` returns `(fig, axes_array)`; `plt.subplot()` returns a single axes |
| 6 | **a** | `ax.twinx()` creates a twin Axes sharing the x-axis |
| 7 | **b** | `rcParams` stores global Matplotlib configuration defaults |
| 8 | **a** | `matplotlib.gridspec.GridSpec` enables complex subplot arrangements |
| 9 | **a** | Pandas uses Matplotlib as its default plotting backend |
| 10 | **b** | Always inspect the dataset first to understand structure (`.dims`, `.coords`, `.data_vars`) |
