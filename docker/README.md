# PyGILE-Plus Docker Setup

Quick setup instructions for the PyGILE-Plus Docker environment.

## Quick Start 

### Option 1: Pull Pre-built Image (Recommended) [After successful pull, then see "Running the container"]
```bash
docker pull iamvuon/pygile-plus
```

OR

### Option 2: Build from Source
```bash
# From the docker/ directory
docker build -t pygile-plus .
```

## Running the Container

### Basic Setup
```bash
# Run with Jupyter Lab auto-start
docker run -it --name pygile-plus-container -p 8888:8888 -v $(pwd):/workspace iamvuon/pygile-plus
```

**Jupyter Lab starts automatically at `http://localhost:8888`**

### Full Environment Setup (Required for All Tools)

**Step 1: Environment Setup for CLI Tools**
In a **new terminal window**:
```bash
# Connect to running container
docker exec -it pygile-plus-container bash

# Run environment setup script
source /workspace/pygile_working_env.sh
```

**Step 2: Initialize in Jupyter**
Run this **first cell** in any new notebook:
```python
import os
import sys

# Environment setup for direct tool access
os.environ['LD_LIBRARY_PATH'] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib"
os.environ['SAGA_CMD'] = '/opt/saga/bin/saga_cmd'
os.environ['SAGA_MLB'] = '/opt/saga/lib/saga'
os.environ['GISBASE'] = '/opt/grass'
os.environ['OTB_APPLICATION_PATH'] = '/opt/otb/lib/otb/applications'

# Add GRASS to Python path
sys.path.insert(0, '/opt/grass/etc/python')

print("PyGILE-Plus initialized with direct GIS tool access + complete Python stack!")
```

## Available Tools & Libraries

### GIS Processing Algorithms 
- **SAGA GIS**: (CLI)
- **GRASS GIS**: (CLI + Python + direct integration)
- **Whitebox Tools**: (CLI)
- **OTB**: (CLI)

### Python Geospatial Stack
**Core:** GDAL, Shapely, Fiona, Rasterio, GeoPandas, PyProj  
**Scientific:** NumPy, SciPy, Pandas, Xarray  
**ML/AI:** PyTorch, TensorFlow, scikit-learn, scikit-image, OpenCV, PySpatialML  
**Visualization:** Matplotlib, Plotly, Folium, Leafmap, Geemap, pythreejs  
**Web/Cloud:** Earth Engine API, STAC tools, Planetary Computer, localtileserver  
**Spatial Analysis:** rasterstats, xarray-spatial

**All PyGILE libraries included**

## Access Methods

### GRASS GIS (Dual Access)
```python
# Python integration
import grass.script as gscript
gscript.run_command('r.slope.aspect', elevation='dem', slope='slope')

# Or CLI (in terminal)
# r.slope.aspect elevation=dem slope=slope
```

### SAGA GIS (CLI)
```bash
# Terminal/CLI access
saga_cmd ta_morphometry 0 -ELEVATION=dem.tif -SLOPE=slope.tif
```

### Whitebox Tools (CLI)
```bash
# Terminal/CLI access
whitebox_tools --run=Slope --input=dem.tif --output=slope.tif
```

### OTB (CLI)
```bash
# Terminal/CLI access
otbcli_BandMath -il image.tif -out result.tif -exp "im1b1+im1b2"
```

### PySpatialML (New)
```python
# Spatial machine learning on raster stacks
from pyspatialml import Raster
stack = Raster(['band1.tif', 'band2.tif', 'band3.tif'])
```

### pythreejs (New)
```python
# Interactive 3D visualization in Jupyter
import pythreejs as p3j
```

## Verification Test

For complete testing and examples of all tools, see the example notebook:
[Test_SAGA, GRASS, OTB, Whitebox and Python Packages.ipynb](https://github.com/Geoinformatics-Lab/PyGILE-Plus/blob/main/example_notebooks/Test_QGIS%2C%20SAGA%2C%20GRASS%2C%20OTB%2C%20Whitebox%20and%20Python%20Packages.ipynb)

This notebook demonstrates:
- SAGA GIS command-line usage  
- GRASS GIS dual access (CLI + Python)
- OTB remote sensing tools
- Whitebox Tools geospatial analysis
- Python geospatial library imports
- Complete algorithm extraction and verification

## Container Management

### Persistent Data
```bash
# Mount local directory for persistent data
docker run -p 8888:8888 -v /path/to/your/data:/workspace/data pygile-plus
```

### Resource Allocation
```bash
# Allocate more resources
docker run -p 8888:8888 --memory=8g --cpus=4 pygile-plus
```

### Stop/Restart
```bash
# Stop container
docker stop pygile-plus-container

# Restart container
docker start pygile-plus-container

# Remove container
docker rm pygile-plus-container
```

## Troubleshooting

### Common Issues

**Jupyter not accessible:**
- Check if port 8888 is available
- Try: `docker run -p 8889:8888 pygile-plus`

**CLI tools not found:**
- Ensure you ran: `source /workspace/pygile_working_env.sh`
- Check PATH: `echo $PATH`

**Import errors:**
- Container uses conda environment: `/opt/conda/envs/pygile`
- All packages pre-installed, no additional setup needed

### Performance Tips

- Allocate 8GB+ RAM for large datasets
- Use SSD storage for better I/O performance
- Mount data directories rather than copying into container

## Next Steps

1. **Access Jupyter**: http://localhost:8888
2. **Run environment setup** in terminal
3. **Initialize environment** in first notebook cell

For detailed examples and algorithm documentation, see the main repository README and [algorithms_toc/](https://github.com/Geoinformatics-Lab/PyGILE-Plus/tree/main/algorithms_toc) directory.
