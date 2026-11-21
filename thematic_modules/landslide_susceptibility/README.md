# Landslide Susceptibility Mapping

A thematic module of PyGILE-Plus: six notebooks that take you through a complete landslide susceptibility study of a real area, with the GIS engines in the PyGILE-Plus Docker image (WhiteboxTools, SAGA GIS and GRASS GIS) and Python.

**Prerequisites:** Parts A to C of the [PyGILE core curriculum](../../PyGILE_course/README.md): Python, vector data and rasters. Part D (satellite imagery) helps too. These notebooks are a research workflow, not step-by-step lessons, so they have no practice questions or automatic marks.

| Notebook | What it does |
| --- | --- |
| [1 · Configuration and setup](01_Configuration_and_Setup.ipynb) | Paths and parameters for your DEM and outputs, saved as one configuration file |
| [2 · Watershed delineation](02_Watershed_Delineation.ipynb) | Watersheds from the DEM with WhiteboxTools |
| [3 · Terrain and hydrological factors](03_Terrain_and_Hydrological_Factors.ipynb) | Slope, curvature, wetness and other factors for each watershed |
| [4 · Landform classification](04_Landform_Classification.ipynb) | Landforms with geomorphons |
| [5 · Inventory preparation](05_Inventory_Preparation.ipynb) | The landslide inventory and the stack of conditioning factors |
| [6 · Landslide susceptibility mapping](06_LSM_Final.ipynb) | The susceptibility model and the final map |

**Data:** the example inventory is the landslides of the 2015 Gorkha earthquake in Nepal: Gnyawali, K.R., Adhikari, B.R.: Earthquake induced landslides triggered by 2015 Gorkha earthquake Mw 7.8, https://doi.org/10.5066/F7028Q2X, 2017, in the USGS Repository of Earthquake-triggered Ground Failure Inventories, https://doi.org/10.5066/F7H70DB4. Notebook 5 also accepts your own inventory.
