# Week 3 Quiz — Statistical, Scientific, Time Series, and Geographic Visualization

**Instructions:** Answer each question to the best of your ability.

---

**1.** Which library builds on Matplotlib and provides high-level statistical plots like violin plots and heatmaps?
   - a) Plotly
   - b) Seaborn
   - c) Bokeh
   - d) Altair

**2.** What is the correct way to create a violin plot with Seaborn?
   - a) `sns.violinplot(data=df, x="month", y="rainfall")`
   - b) `plt.violinplot(data=df, x="month", y="rainfall")`
   - c) `sns.violin(data=df, month, rainfall)`
   - d) `sns.violin_plot(df.month, df.rainfall)`

**3.** Which Matplotlib function is best for showing the distribution of a dataset?
   - a) `plt.plot()`
   - b) `plt.boxplot()`
   - c) `plt.contour()`
   - d) `plt.imshow()`

**4.** What does `plt.colorbar()` add to a figure?
   - a) A legend for line colours
   - b) A colour bar for scalar mappable objects (e.g. pcolormesh)
   - c) A colour picker dialog
   - d) A bar chart with coloured bars

**5.** How do you format x-axis ticks as dates in Matplotlib?
   - a) `plt.xticks(date_format="%Y-%m")`
   - b) `ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))`
   - c) `plt.dates()`  (d) `ax.format_date("%Y-%m")`

**6.** Which Cartopy projection is most suitable for equatorial rainfall maps?
   - a) `ccrs.Orthographic()`
   - b) `ccrs.PlateCarree()`
   - c) `ccrs.NorthPolarStereo()`
   - d) `ccrs.Mercator()`

**7.** How do you add country borders to a Cartopy map?
   - a) `ax.countries()`
   - b) `ax.add_feature(cfeature.BORDERS)`
   - c) `plt.borders()`
   - d) `cartopy.borders(ax)`

**8.** What is the purpose of `ax.gridlines(draw_labels=True)` in Cartopy?
   - a) Draw a grid on the map
   - b) Add latitude/longitude grid lines with labels
   - c) Enable the map grid snapping
   - d) Draw a legend grid

**9.** Which function from `scipy.stats` is commonly used for linear regression?
   - a) `scipy.stats.linregress()`
   - b) `scipy.stats.linear_regression()`
   - c) `scipy.optimize.curve_fit()`
   - d) `scipy.stats.pearsonr()`

**10.** What does `np.corrcoef()` return?
   - a) The covariance matrix
   - b) The Pearson correlation coefficient matrix
   - c) The p-value of a correlation test
   - d) The R² value

---

## Answer Key

| # | Answer | Notes |
|---|--------|-------|
| 1 | **b** | Seaborn provides high-level statistical visualisation built on Matplotlib |
| 2 | **a** | `sns.violinplot()` is the correct Seaborn API |
| 3 | **b** | `plt.boxplot()` displays distribution quartiles and outliers |
| 4 | **b** | `plt.colorbar()` creates a colour bar for `mappable` objects |
| 5 | **b** | `mdates.DateFormatter` formats date ticks; must import `matplotlib.dates` |
| 6 | **b** | `PlateCarree` is a simple cylindrical projection suitable for equatorial regions |
| 7 | **b** | `cfeature.BORDERS` adds country boundaries |
| 8 | **b** | `gridlines(draw_labels=True)` adds labelled lat/lon grid lines |
| 9 | **a** | `scipy.stats.linregress()` performs linear regression |
| 10 | **b** | `np.corrcoef()` returns the Pearson correlation matrix |
