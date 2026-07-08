---
title: Module 2 — Environment Setup
---

# Module 2: Environment Setup

This module covers the complete setup of your Python data visualization environment.

---

## Learning Objectives

- Install Python and create isolated environments
- Install Matplotlib and supporting libraries
- Configure Jupyter Notebook for interactive plotting
- Verify the installation with diagnostic plots
- Access and understand the CHIRPS dataset

---

## 1. Python Distribution

### CPython (python.org)

The standard Python distribution from [python.org](https://python.org).

```powershell
# Verify existing installation
python --version
pip --version
```

### Anaconda / Miniconda

A data-science-focused distribution with its own package manager.

```powershell
conda --version
conda info
```

:::{note}
**Recommendation**: Use Miniconda on Windows (avoids Cartopy DLL issues). Use standard Python + venv on macOS/Linux.
:::

---

## 2. Virtual Environment

### Why Virtual Environments?

- Isolate project dependencies
- Avoid version conflicts
- Reproducible builds

### venv (Built-in)

```powershell
python -m venv matplot-env
# Activate:
# Windows PowerShell:
.\matplot-env\Scripts\Activate.ps1
# Windows CMD:
.\matplot-env\Scripts\activate.bat
# macOS / Linux:
source matplot-env/bin/activate
```

:::{warning}
If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
:::

### Conda Environment

```powershell
conda create --name matplot-env python=3.11
conda activate matplot-env
conda install -c conda-forge matplotlib numpy pandas cartopy xarray netcdf4 jupyter
```

---

## 3. Package Installation

### requirements.txt

Create a `requirements.txt` file with the following content:

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

```powershell
pip install -r requirements.txt
```

---

## 4. Jupyter Kernel

Register your virtual environment as a Jupyter kernel:

```powershell
pip install ipykernel
python -m ipykernel install --user --name=matplot-env --display-name="Matplotlib Training"
```

Start Jupyter:

```powershell
jupyter notebook
```

---

## 5. Diagnostic Plot

Run this script to confirm everything integrates:

```python
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs

fig, axes = plt.subplots(1, 2, figsize=(12, 4),
                         subplot_kw={'projection': ccrs.PlateCarree()})

# Simple line plot
ax0 = axes[0]
x = np.linspace(0, 10, 100)
ax0.plot(x, np.sin(x), color='#2c7bb6')
ax0.set_title('Line Plot Test')
ax0.set_xlabel('x')
ax0.set_ylabel('sin(x)')

# Quick map
ax1 = axes[1]
ax1.coastlines()
ax1.gridlines(draw_labels=True)
ax1.set_title('Cartopy Map Test')
ax1.set_extent([-20, 40, 30, 60])

plt.tight_layout()
plt.show()

print("Environment setup verified successfully!")
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `pip` not found | Reinstall Python with "Add to PATH" |
| Cartopy install fails | Use `conda install -c conda-forge cartopy` |
| Plot not showing in Jupyter | Add `%matplotlib inline` or use `%matplotlib notebook` |
| Kernel not found | Run `python -m ipykernel install` again |

---

## Next Steps

Proceed to {doc}`module03` to learn Jupyter Notebook essentials.
