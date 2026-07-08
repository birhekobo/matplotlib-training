#import "../macros.typ": note-box, warning-box, info-box

= Preface

Welcome to *Matplotlib Training: From Zero to Publication-Quality Visualizations*.

This book is designed for scientists, engineers, analysts, and anyone who needs to create professional data visualizations using the Python programming language. Whether you are a complete beginner to data visualization or an experienced programmer looking to refine your plotting skills, this book will guide you through the entire process.

== Why This Book?

Data visualization is a critical skill in the modern data-driven world. A well-crafted visualization can reveal patterns, communicate insights, and tell a compelling story. Matplotlib, the foundational plotting library for Python, provides unparalleled control over every aspect of a figure. Yet many users struggle to move beyond default settings and basic plots.

#note-box[
  This book is built around the *CHIRPS* satellite rainfall dataset, providing a real-world context for all examples and exercises. You will not just learn Matplotlib syntax—you will learn how to create meaningful visualizations with actual scientific data.
]

== Who This Book Is For

- *Students* learning data science or scientific computing
- *Researchers* who need publication-ready figures for papers and presentations
- *Data analysts* who want to improve their reporting dashboards
- *Python developers* transitioning from basic plots to sophisticated visualizations

== Prerequisites

You should have:

- Basic Python knowledge (variables, functions, lists, loops)
- Familiarity with NumPy arrays is helpful but not required
- No prior experience with Matplotlib is assumed

== How to Use This Book

The book is organized into seventeen chapters and an appendix. Each chapter builds on the previous ones, but you can jump to specific topics as needed.

=== Chapter Overview

#table(
  columns: (1fr, 3fr),
  [*Chapter*], [*Content*],
  [1], [Principles of effective data visualization],
  [2], [Setting up your Python environment],
  [3], [Jupyter Notebook essentials],
  [4], [Matplotlib fundamentals: figures, axes, artists],
  [5], [Basic chart types: line, scatter, bar, histogram],
  [6], [Styling and customization],
  [7], [Axes customization and advanced control],
  [8], [Multiple plots and subplot layouts],
  [9], [Statistical visualization],
  [10], [Scientific visualization],
  [11], [Time series visualization],
  [12], [Geographic visualization with Cartopy],
  [13], [NumPy and Pandas integration],
  [14], [Advanced Matplotlib techniques],
  [15], [Publication-quality figures],
  [16], [Real-world projects],
  [17], [Capstone project: rainfall dashboard],
  [Appendix], [Cheat sheets, references, and resources],
)

=== Code Examples

All code examples use the *object-oriented API* (e.g., `fig, ax = plt.subplots()`) rather than the pyplot state-machine interface. This approach gives you explicit control and scales to complex figures.

Code blocks are displayed in monospace font:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 4))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x))
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Sine Wave")
plt.show()
```

=== Exercises and Projects

Each chapter includes hands-on exercises. Solutions to all exercises are provided. The final three chapters are dedicated to real-world projects and a capstone exercise.

== About the Dataset

Throughout this book, we use the Climate Hazards Group InfraRed Precipitation with Station Data (CHIRPS) dataset. CHIRPS provides quasi-global rainfall estimates from 1981 to the present at a 0.05-degree resolution. This real-world dataset makes the learning experience authentic and immediately applicable.

#warning-box[
  Sample data files are provided in the companion repository. For the latest data, visit the CHIRPS website at `https://www.chc.ucsb.edu/data/chirps`.
]

== Conventions Used in This Book

| *Convention* | *Meaning* |
|---|---|
| `monospace` | Code, file paths, terminal commands |
| *italic* | Technical terms, emphasis |
| *bold* | Key concepts, menu items |
| 📝 Note box | Additional commentary or tips |
| ⚠️ Warning box | Common pitfalls to avoid |

== Getting Help

If you encounter issues:

- Check the FAQ in the appendix
- Search StackOverflow with the `[matplotlib]` tag
- Visit the Matplotlib documentation at `https://matplotlib.org/stable/`

== Acknowledgments

This book draws on the work of many contributors to the Matplotlib open-source project, the Cartopy developers, and the scientific Python ecosystem. Special thanks to John D. Hunter, the original creator of Matplotlib, whose vision made this all possible.

== Let's Begin

Turn the page to start your journey from basic plots to publication-quality visualizations.









