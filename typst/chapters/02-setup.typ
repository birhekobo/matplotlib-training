#import "../macros.typ": note-box, warning-box, info-box
= Environment Setup

Before we can create visualizations, we need to set up a proper Python development environment. This chapter walks through every step, from installing Python to verifying your full data visualization stack.

== Installing Python

You need Python version 3.11 or later. There are two primary options:

=== Python.org Distribution

The standard CPython distribution is available at `python.org/downloads/`. During installation on Windows, make sure to check *"Add Python to PATH"*.

Verify the installation:

```bash
python --version
pip --version
```

=== Miniconda (Recommended for Data Science)

Miniconda provides Python plus the `conda` package manager, which handles binary dependencies (like Cartopy on Windows) much better than pip:

Download from `docs.conda.io/en/latest/miniconda.html` and run the installer.

```bash
conda --version
```

#note-box[
  *Recommendation*: Use Miniconda on Windows to avoid DLL issues with Cartopy. Use standard Python with `venv` on macOS and Linux for a lighter setup.
]

== Creating a Virtual Environment

Virtual environments isolate project dependencies, preventing conflicts between different projects.

=== Using venv (Built-in)

```bash
# Create environment
python -m venv matplotlib-training

# Activate — Windows PowerShell
matplotlib-training\Scripts\Activate.ps1

# Activate — Windows CMD
matplotlib-training\Scripts\activate.bat

# Activate — macOS / Linux
source matplotlib-training/bin/activate
```

#warning-box[
  If PowerShell blocks script execution, run: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
]

=== Using Conda

```bash
conda create --name matplotlib-training python=3.11
conda activate matplotlib-training
```

== Installing Packages

Create a `requirements.txt` file:

```text
matplotlib>=3.8.0
numpy>=1.24.0
pandas>=2.0.0
xarray>=2023.6.0
netCDF4>=1.6.0
cartopy>=0.22.0
jupyter>=1.0.0
ipykernel>=6.25.0
scipy>=1.11.0
rasterio>=1.3.0
rioxarray>=0.15.0
geopandas>=0.14.0
```

Install with:

```bash
pip install -r requirements.txt
```

Or with conda:

```bash
conda install -c conda-forge matplotlib numpy pandas cartopy xarray netcdf4 jupyter scipy
```

== Configuring Jupyter

Register your environment as a Jupyter kernel so you can select it in notebooks:

```bash
python -m ipykernel install --user --name=matplotlib-training --display-name="Matplotlib Training"
```

Launch Jupyter:

```bash
jupyter notebook
```

== Verifying the Installation

Run this diagnostic script to confirm everything works:

```python
import matplotlib
import numpy as np
import pandas as pd
import cartopy
import xarray as xr

print(f"Matplotlib: {matplotlib.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Cartopy: {cartopy.__version__}")
print(f"xarray: {xr.__version__}")

# Quick plot test
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])
fig.savefig("test.png", dpi=72)
print("✓ Plot test passed")
```

#info-box[
  Save this script as `check_setup.py` and run it with `python check_setup.py`. Any import errors indicate missing packages.
]

== Troubleshooting Common Issues

| *Problem* | *Solution* |
|---|---|
| `python` not recognized | Reinstall Python with "Add to PATH" checked |
| Cartopy install fails on Windows | Use `conda install -c conda-forge cartopy` |
| `pip` command not found | `python -m pip install --upgrade pip` |
| Permission errors | `pip install --user -r requirements.txt` or use Administrator shell |
| Conda command not found | Add Conda to PATH or use Anaconda Prompt |
| Plot not showing in Jupyter | Add `%matplotlib inline` at top of notebook |

== Summary

You now have a fully functional data visualization environment. All the libraries needed for this course are installed and verified. In the next chapter, we will learn how to use Jupyter Notebook effectively for interactive data exploration and visualization.








