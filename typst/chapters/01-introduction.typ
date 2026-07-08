#import "../macros.typ": note-box, warning-box, info-box
= Introduction to Data Visualization

Data visualization is the graphical representation of information and data. By using visual elements like charts, graphs, and maps, data visualization tools provide an accessible way to see and understand trends, outliers, and patterns in data.

== Why Data Visualization Matters

The human visual system is remarkably efficient at processing visual information. We can detect patterns, anomalies, and relationships in a well-designed graphic much faster than in a table of numbers. This makes visualization an essential tool for:

- *Exploratory data analysis*: Understanding the structure and quality of data
- *Communication*: Conveying findings to diverse audiences
- *Decision making*: Supporting evidence-based choices
- *Storytelling*: Narrating data-driven stories

#note-box[
  *"The greatest value of a picture is when it forces us to notice what we never expected to see."* — John Tukey, pioneering statistician and data visualization advocate.
]

== The Grammar of Graphics

Wilkinson's Grammar of Graphics (2005) provides a theoretical framework for understanding statistical graphics. It decomposes a visualization into:

1. *Data*: The underlying dataset
2. *Aesthetic mappings*: How data variables map to visual properties (position, color, size)
3. *Geometric objects*: The visual elements (points, lines, bars, polygons)
4. *Coordinate system*: How the geometric space is organized (Cartesian, polar, map projections)
5. *Scale transformations*: How data values are mapped to the visual space (linear, log, ordinal)

Understanding this grammar helps you think systematically about constructing visualizations. Matplotlib implements all of these concepts, giving you fine-grained control over each component.

== Key Principles of Effective Visualization

=== Data-Ink Ratio

Edward Tufte introduced the concept of the data-ink ratio:

$"Data-Ink Ratio" = ("Ink used to display data") / ("Total ink used in graphic")$

Maximize this ratio by removing non-data elements:

- Redundant gridlines
- Decorative 3D effects
- Excessive axis labels
- Background images and gradients
- Unnecessary borders

#warning-box[
  Removing elements purely for minimalism can harm readability. The goal is *effective* communication, not extreme minimalism. Keep axis labels, appropriate gridlines, and necessary context.
]

=== Pre-attentive Processing

The human brain processes certain visual properties almost instantly (under 250 milliseconds) without conscious effort. These *pre-attentive attributes* include:

- *Position*: Where something is located
- *Size*: How large or small it appears
- *Color hue*: Red vs. blue vs. green
- *Color intensity*: Bright vs. dim
- *Orientation*: Horizontal vs. vertical vs. angled
- *Shape*: Circle vs. square vs. triangle
- *Motion*: Flashing or moving elements

Use these attributes deliberately:

#table(
  columns: (1fr, 2fr, 2fr),
  [*Attribute*], [*Best For*], [*Example*],
  [Position], [Comparing values], [Bar chart, dot plot],
  [Length], [Quantitative comparison], [Bar chart],
  [Color hue], [Categories], [Scatter plot groups],
  [Color intensity], [Ordered/ranked data], [Heatmap],
  [Size], [Third variable encoding], [Bubble chart],
  [Orientation], [Directional data], [Wind rose],
  [Shape], [Categories (small sets)], [Scatter plot markers],
)

=== Chart Type Selection

Choosing the right chart type is critical:

| *Goal* | *Recommended Chart* |
|---|---|
| Compare categories | Bar chart, dot plot |
| Show trends over time | Line chart, area chart |
| Distribution of one variable | Histogram, box plot, violin plot |
| Relationship between two variables | Scatter plot, hexbin |
| Relationship among many variables | Pair plot, parallel coordinates |
| Composition of a whole | Stacked bar chart, treemap |
| Geographic distribution | Choropleth, contour map |
| Correlation matrix | Heatmap |

== Why Matplotlib?

Matplotlib is the most widely used plotting library in the Python ecosystem. Key advantages include:

1. *Maturity*: First released in 2003 by John D. Hunter, with over two decades of development
2. *Flexibility*: Control every detail of your figure
3. *Publication quality*: Output at any resolution, vector formats (PDF, SVG, EPS)
4. *Ecosystem integration*: Works seamlessly with NumPy, Pandas, xarray, Cartopy
5. *Extensive documentation*: Rich gallery of examples, active community
6. *Customizability*: Full control through the object-oriented API

#info-box[
  Matplotlib is *not* the only Python plotting library. Alternatives include Seaborn (statistical plots), Plotly (interactive), Bokeh (web-based), and Altair (declarative). However, Matplotlib remains the foundation—many of these libraries build on Matplotlib internally.
]

== Course Structure

This book is organized to build skills progressively:

1. *Foundations* (Chapters 1-4): Principles, setup, Jupyter, basics
2. *Core Skills* (Chapters 5-8): Charts, styling, axes, subplots
3. *Advanced Topics* (Chapters 9-13): Statistical, scientific, time series, geographic, integration
4. *Professional Practice* (Chapters 14-15): Advanced techniques, publication readiness
5. *Projects* (Chapters 16-17): Real-world application, capstone

== Summary

Effective data visualization requires both technical skill and design thinking. In this chapter, we introduced the principles that will guide your work throughout this book. The key takeaway is that every visual element should serve a purpose—to inform, to clarify, or to guide the viewer's attention.

In the next chapter, we will set up your Python environment and install the libraries needed for the course.








