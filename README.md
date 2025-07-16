# PyGILE-Plus: Python GeoInformatics Lab Environment-Plus

A comprehensive, headless Docker environment for geospatial research with **2,300+ algorithms** across multiple GIS platforms plus a complete Python geospatial stack.

## What's Included

**Major GIS Platforms:**
- **QGIS LTR 3.40** 
- **SAGA GIS 9.3.2** 
- **GRASS GIS 8.4.0** 
- **Whitebox Tools** (Latest) 
- **Orfeo ToolBox (OTB) 9.1.1** 

**Python Geospatial Stack:**
- **Core Libraries**: GDAL, PROJ, GEOS, Shapely, Fiona, Rasterio, GeoPandas
- **Scientific Computing**: NumPy, SciPy, Pandas, Xarray
- **Machine Learning**: PyTorch, TensorFlow, scikit-learn, scikit-image
- **Visualization**: Matplotlib, Plotly, Folium, Holoviews, Seaborn
- **Image Processing**: OpenCV, scikit-image
- **Web Mapping**: Leafmap, Geemap, ipyleaflet, localtileserver
- **Cloud/Remote Sensing**: EarthEngine API, STAC tools, Planetary Computer
- **Documentation**: Sphinx ecosystem, Jupyter-book
- **Jupyter Lab**: Interactive analysis environment

**Note**: All PyGILE libraries included except Geowombat (NumPy 2.0 compatibility issue). See installation instructions for optional Geowombat setup.

**Key Features:**
- Headless operation (no GUI required)
- **2,326+ GIS algorithms** across major platforms
- **Complete Python geospatial ecosystem** with ML/AI capabilities
- Pre-configured environment with all dependencies
- Jupyter Lab integration for interactive workflows
- Support for both Python scripting and CLI tool access

## Getting Started

### Quick Setup
```bash
# Pull and run the container
docker pull dockagile/pygile-plus
docker run -p 8888:8888 -v $(pwd)/data:/workspace/data pygile-plus

# Access Jupyter Lab at http://localhost:8888
```

**For complete setup instructions**: See [docker/README.md](docker/) for detailed setup guide including environment configuration and tool initialization.

## What's Available

### GIS Processing Algorithms 
| Platform | Access Method | Description |
|----------|---------------|-------------|
| SAGA GIS |  CLI | Comprehensive geoprocessing and analysis |
| GRASS GIS |  CLI + Python | Vector/raster analysis and modeling |
| Whitebox Tools | CLI | Advanced geospatial analysis |
| QGIS | Python/GUI | Desktop GIS processing algorithms |
| OTB | CLI | Remote sensing and image processing |

### Python Libraries & Frameworks
**Geospatial Core:** GDAL, Shapely, Fiona, Rasterio, GeoPandas, PyProj, Cartopy

**Scientific Computing:** NumPy, SciPy, Pandas, Xarray, Dask

**Machine Learning:** PyTorch, TensorFlow, scikit-learn, scikit-image

**Visualization:** Matplotlib, Plotly, Seaborn, Folium, Holoviews, Bokeh

**Image Processing:** OpenCV, scikit-image, Pillow

**Web Mapping:** Leafmap, Geemap, ipyleaflet, Folium

**Cloud/Remote Sensing:** Google Earth Engine API, STAC tools, Planetary Computer

**Development:** Jupyter Lab, IPython, Git

## Use Cases

- Remote sensing analysis and classification
- Spatial data processing and geostatistics  
- Machine learning on geospatial data
- Raster and vector analysis workflows
- Educational geospatial computing
- Large-scale geospatial data processing
- Web mapping and interactive visualization
- Cloud-based geospatial analysis workflows

## Optional Components

### Geowombat Installation
Geowombat is not pre-installed due to NumPy 2.0 compatibility requirements for modern ML frameworks. Install if needed:

```python
# In Jupyter notebook
!pip install geowombat --no-build-isolation
```

**Note**: This may cause conflicts with TensorFlow/PyTorch if you need the latest ML features.

## System Requirements

- Docker with 8GB+ RAM recommended
- 10GB+ storage for the image
- Network access for initial build/pull

## Documentation

For detailed algorithm listings and capabilities, please refer the individual CSV files in the [algorithms_toc/](https://github.com/Geoinformatics-Lab/PyGILE-Plus/tree/main/algorithms_toc) directory.

## License Information

**License Notice**: All software and packages included in this container are made available under their respective licenses. Please refer to the original documentation for specific license terms:

**GIS Platforms:**
- QGIS: https://github.com/qgis/QGIS
- GRASS GIS: https://github.com/OSGeo/grass
- SAGA GIS: https://sourceforge.net/projects/saga-gis/
- Whitebox Tools: https://github.com/jblindsay/whitebox-tools
- OTB (Orfeo ToolBox): https://github.com/orfeotoolbox/OTB

**Python Core Libraries:**
- GDAL: https://github.com/OSGeo/gdal
- Shapely: https://github.com/shapely/shapely
- Fiona: https://github.com/Toblerity/Fiona
- Rasterio: https://github.com/rasterio/rasterio
- GeoPandas: https://github.com/geopandas/geopandas
- PyProj: https://github.com/pyproj4/pyproj

**Scientific Computing:**
- NumPy: https://github.com/numpy/numpy
- SciPy: https://github.com/scipy/scipy
- Pandas: https://github.com/pandas-dev/pandas
- Xarray: https://github.com/pydata/xarray
- scikit-learn: https://github.com/scikit-learn/scikit-learn
- scikit-image: https://github.com/scikit-image/scikit-image

**Machine Learning:**
- PyTorch: https://github.com/pytorch/pytorch
- TensorFlow: https://github.com/tensorflow/tensorflow
- OpenCV: https://github.com/opencv/opencv

**Visualization:**
- Matplotlib: https://github.com/matplotlib/matplotlib
- Plotly: https://github.com/plotly/plotly.py
- Folium: https://github.com/python-visualization/folium
- Seaborn: https://github.com/mwaskom/seaborn
- Bokeh: https://github.com/bokeh/bokeh

**Web Mapping:**
- Leafmap: https://github.com/opengeos/leafmap
- Geemap: https://github.com/opengeos/geemap
- ipyleaflet: https://github.com/jupyter-widgets/ipyleaflet

**Cloud/Remote Sensing:**
- Google Earth Engine API: https://github.com/google/earthengine-api
- PySTAC: https://github.com/stac-utils/pystac
- Stackstac: https://github.com/gjoseph92/stackstac
- Planetary Computer: https://github.com/microsoft/planetary-computer-sdk-for-python

**Documentation:**
- Sphinx: https://github.com/sphinx-doc/sphinx
- Jupyter Book: https://github.com/executablebooks/jupyter-book

**Package Management:**
- Conda/Mamba: https://github.com/conda-forge/miniforge