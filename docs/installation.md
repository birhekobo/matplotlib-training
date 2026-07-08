---
title: Installation Guide
---

# Installation Guide

This guide walks you through setting up your environment for the Matplotlib Training Course.

:::{warning}
If you already have Python and a preferred environment manager, skip to {ref}`install-packages`.
:::

---

## 1. Install Python

### Option A: python.org (Recommended for beginners)

1. Go to [python.org/downloads](https://python.org/downloads/)
2. Download Python **3.11 or later**
3. Run the installer — **check "Add Python to PATH"** during installation
4. Verify in a terminal:

   ```powershell
   python --version
   ```

### Option B: Miniconda (Recommended for data science)

1. Download Miniconda from [docs.conda.io](https://docs.conda.io/en/latest/miniconda.html)
2. Run the installer with default settings
3. Verify:

   ```powershell
   conda --version
   ```

---

## 2. Create a Virtual Environment

### Using venv (standard Python)

```powershell
python -m venv matplotlib-training
.\matplotlib-training\Scripts\Activate.ps1
```

On macOS / Linux:

```bash
python3 -m venv matplotlib-training
source matplotlib-training/bin/activate
```

### Using conda

```powershell
conda create --name matplotlib-training python=3.11
conda activate matplotlib-training
```

---

(install-packages)=

## 3. Install Packages

Clone the repository and install dependencies:

```powershell
git clone <repository-url>
cd matplotlib-training
pip install -r requirements.txt
```

### Requirements file (`requirements.txt`)

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

---

## 4. Verify Installation

Run the following Python script to confirm everything works:

```python
import matplotlib
import numpy as np
import pandas as pd
import cartopy
import xarray as xr

print(f"Matplotlib version: {matplotlib.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"Cartopy version: {cartopy.__version__}")
print(f"xarray version: {xr.__version__}")

# Quick plot test
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1], label="Test")
ax.legend()
fig.savefig("test_plot.png", dpi=72)
print("Plot test passed — test_plot.png created.")
```

Expected output (versions may vary):

```text
Matplotlib version: 3.8.4
NumPy version: 1.26.4
Pandas version: 2.2.0
Cartopy version: 0.22.0
xarray version: 2024.1.1
Plot test passed — test_plot.png created.
```

---

## 5. CHIRPS Dataset

The **Climate Hazards Group InfraRed Precipitation with Station data (CHIRPS)** is a quasi-global rainfall dataset spanning 1981–present.

### Characteristics

| Property | Value |
|----------|-------|
| Spatial resolution | 0.05° (~5.5 km) |
| Temporal resolution | Daily, pentadal, monthly |
| Coverage | 50°S – 50°N |
| Source | Satellite + station observations |
| Format | NetCDF / GeoTIFF |

### Downloading CHIRPS Data

```python
import urllib.request

url = (
    "https://data.chc.ucsb.edu/products/CHIRPS-2.0/"
    "global_daily/netcdf/p05/"
    "chirps-v2.0.2024.01.01.nc"
)
urllib.request.urlretrieve(url, "chirps-v2.0.2024.01.01.nc")
```

:::{note}
For this course, sample CHIRPS files are provided in the `datasets/` directory.
:::

---

## Troubleshooting FAQ

### `matplotlib` not found

```powershell
pip install matplotlib
```

### Cartopy installation fails on Windows

Install the pre-compiled wheel from [Christopher Gohlke's site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#cartopy):

```powershell
pip install cartopy-<version>-win_amd64.whl
```

Or use conda (recommended on Windows):

```powershell
conda install -c conda-forge cartopy
```

### Jupyter Notebook does not show plots

Add this at the top of your notebook:

```python
%matplotlib inline
```

### Python not recognized as a command

- Reinstall Python and check **"Add Python to PATH"**
- Restart your terminal after installation

### Permission errors installing packages

```powershell
pip install --user -r requirements.txt
```

Or run your terminal as Administrator (Windows) / use `sudo` (macOS/Linux).
