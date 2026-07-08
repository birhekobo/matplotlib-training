# Matplotlib Training Course

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-blue)](https://matplotlib.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)](https://jupyter.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI](https://github.com/birhekobo/matplotlib-training/actions/workflows/ci.yml/badge.svg)](https://github.com/birhekobo/matplotlib-training/actions/workflows/ci.yml)
[![Docs](https://github.com/birhekobo/matplotlib-training/actions/workflows/docs.yml/badge.svg)](https://birhekobo.github.io/matplotlib-training)
[![Deployed](https://img.shields.io/badge/deployed-GitHub%20Pages-blue?logo=githubpages)](https://birhekobo.github.io/matplotlib-training)

A comprehensive **40-day Matplotlib bootcamp** taking learners from beginner to advanced level through hands-on projects using real-world climate and environmental datasets.

## Features

- **40 structured lessons** covering everything from basics to publication-quality figures
- **Real-world datasets** — CHIRPS rainfall data (1981–2022) for Ethiopia
- **Jupyter Notebooks** + **Python scripts** for every lesson
- **MyST documentation** website hosted on GitHub Pages
- **Typst-generated eBook** for offline study
- **Exercises, quizzes, and mini-projects** with solutions
- **Capstone project** building a complete visualization portfolio
- **GitHub Actions** for automated testing and deployment

## Prerequisites

- Python 3.10+
- Basic programming knowledge
- No prior Matplotlib experience required

## Quick Start

```bash
# Clone the repository
git clone https://github.com/birhekobo/matplotlib-training.git
cd matplotlib-training

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

Start with `notebooks/01_introduction_to_visualization.ipynb`.

## Course Outline

| Week | Module | Topics |
|------|--------|--------|
| 1 | Introduction & Setup | Visualization principles, Python setup, Jupyter basics |
| 2 | Matplotlib Fundamentals | Figure, Axes, pyplot, basic charts |
| 3 | Styling & Customization | Colors, markers, themes, labels, legends |
| 4 | Axes & Subplots | Axis limits, ticks, scales, GridSpec, insets |
| 5 | Statistical & Scientific Viz | Box plots, heatmaps, contours, surfaces |
| 6 | Time Series & Geospatial | Date axes, rolling stats, maps, rainfall data |
| 7 | NumPy, Pandas & Advanced | DataFrame plotting, OOP interface, animations |
| 8 | Projects & Capstone | Real-world dashboards, portfolio building |

## Dataset

The course uses [CHIRPS](https://www.chc.ucsb.edu/data/chirps) (Climate Hazards Group InfraRed Precipitation with Station data) — a 40+ year quasi-global rainfall dataset at 0.05° resolution.

- **File:** `chirps_1981_2022.nc`
- **Coverage:** Ethiopia region (30°E–60°E, 0°N–20°N)
- **Period:** January 1981 – December 2022 (504 months)
- **Variable:** Monthly precipitation (mm/month)

## Project Structure

```
matplotlib-training/
├── notebooks/        # Jupyter Notebook lessons
├── scripts/          # Python script equivalents
├── datasets/         # Sample datasets
├── images/           # Generated figures
├── docs/             # MyST documentation
├── typst/            # Typst eBook source
├── book/             # Compiled eBook
├── quizzes/          # Weekly quizzes
├── assignments/      # Take-home assignments
├── solutions/        # Exercise solutions
├── tests/            # Automated tests
└── .github/          # CI/CD workflows
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

## Citation

```bibtex
@misc{matplotlib_training,
  author = {Your Name},
  title = {Matplotlib Training Course},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/username/matplotlib-training}
}
```
