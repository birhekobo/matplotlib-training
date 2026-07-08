# Week 2 Quiz — Chart Types, Styling, and Axes

**Instructions:** Answer each question to the best of your ability.

---

**1.** Which function creates a bar chart in Matplotlib?
   - a) `plt.bar(x, height)`
   - b) `plt.barh(x, height)`
   - c) `plt.hist(x)`
   - d) `plt.barplot(x, y)`

**2.** What parameter changes the transparency of a plot element?
   - a) `transparent`
   - b) `alpha`
   - c) `opacity`
   - d) `visibility`

**3.** How do you change the colour of a line to red?
   - a) `plt.plot(x, y, "red")`
   - b) `plt.plot(x, y, color="red")`
   - c) `plt.plot(x, y, c="r")`
   - d) All of the above

**4.** Which parameter in `plt.scatter()` controls the marker size?
   - a) `size`
   - b) `s`
   - c) `markersize`
   - d) `ms`

**5.** What does `ax.set_xlim(0, 100)` do?
   - a) Set the x-axis tick locations
   - b) Set the x-axis data limits to [0, 100]
   - c) Set the x-axis label to "0–100"
   - d) Set the figure width

**6.** Which function is used to create a histogram?
   - a) `plt.bar()`
   - b) `plt.hist()`
   - c) `plt.histogram()`
   - d) `plt.distplot()`

**7.** How do you add horizontal grid lines only?
   - a) `plt.grid(True)`
   - b) `plt.grid(axis="y")`
   - c) `plt.grid(horizontal=True)`
   - d) `ax.yaxis.grid(True)`

**8.** Which of the following is a valid Matplotlib style?
   - a) `"seaborn-v0_8-darkgrid"`
   - b) `"ggplot"`
   - c) `"fivethirtyeight"`
   - d) All of the above

**9.** What does `plt.tight_layout()` do?
   - a) Adjusts subplot parameters to prevent overlapping elements
   - b) Tightens the axis limits to the data
   - c) Removes all white space from the figure
   - d) Compresses the file size when saving

**10.** How do you create a pie chart?
   - a) `plt.pie(values)`
   - b) `plt.piechart(values)`
   - c) `plt.circle(values)`
   - d) `plt.pie_plot(values)`

---

## Answer Key

| # | Answer | Notes |
|---|--------|-------|
| 1 | **a** | `plt.bar(x, height)` creates a vertical bar chart; `plt.barh` is horizontal |
| 2 | **b** | The `alpha` parameter controls transparency (0 = invisible, 1 = opaque) |
| 3 | **d** | All three syntaxes are valid: named colour, `color=` kwarg, or single-letter `c=` |
| 4 | **b** | The `s` parameter controls marker size in `plt.scatter()` |
| 5 | **b** | `set_xlim` sets the visible data limits of the x-axis |
| 6 | **b** | `plt.hist()` creates a histogram |
| 7 | **b** | `plt.grid(axis="y")` shows only horizontal grid lines |
| 8 | **d** | All three are built-in Matplotlib style sheets |
| 9 | **a** | `tight_layout()` adjusts spacing to avoid overlapping labels |
| 10 | **a** | `plt.pie(values)` creates a pie chart |
