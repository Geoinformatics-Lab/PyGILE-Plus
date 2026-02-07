# PyGILE-Plus Docker Setup

Setup and usage instructions for the PyGILE-Plus Docker container.

## Installation

### Pull Pre-built Image

```bash
docker pull dockagile/pygile-plus:latest
```

### Build from Source

```bash
git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git
cd PyGILE-Plus/docker
docker build -t pygile-plus .
```

Build time: ~30-45 minutes

## Running the Container

### Basic Run

```bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus:latest
```

Jupyter Lab starts automatically at `http://localhost:8888`

### With Resource Allocation

```bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  --memory=16g \
  --cpus=8 \
  --shm-size=2g \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus:latest
```

### Multiple Mount Points

```bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  -v /path/to/data:/workspace/data \
  -v /path/to/output:/workspace/output \
  -v /path/to/notebooks:/workspace/notebooks \
  dockagile/pygile-plus:latest
```

### Custom Port

```bash
docker run -it --name pygile-plus \
  -p 8889:8888 \
  dockagile/pygile-plus:latest
```

Access at `http://localhost:8889`

## Environment Setup

### For Jupyter Notebooks

Add this as the **first cell** in every notebook:

```python
import os
import sys

os.environ['LD_LIBRARY_PATH'] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib"
os.environ['SAGA_CMD'] = '/opt/saga/bin/saga_cmd'
os.environ['SAGA_MLB'] = '/opt/saga/lib/saga'
os.environ['GISBASE'] = '/opt/grass'
os.environ['OTB_APPLICATION_PATH'] = '/opt/otb/lib/otb/applications'
sys.path.insert(0, '/opt/grass/etc/python')

print("PyGILE-Plus environment initialized")
```

### For Command-Line

```bash
# Connect to running container
docker exec -it pygile-plus bash

# Source environment
source /workspace/pygile_working_env.sh

# Verify tools
saga_cmd --version
grass --version
whitebox_tools --version
```

## Container Management

```bash
# Stop container
docker stop pygile-plus

# Start container
docker start pygile-plus

# Restart container
docker restart pygile-plus

# View logs
docker logs pygile-plus

# Remove container
docker stop pygile-plus
docker rm pygile-plus

# Remove image
docker rmi dockagile/pygile-plus:latest
```

## Accessing Tools

### SAGA GIS (CLI)

```bash
# List libraries
saga_cmd -h

# List tools in library
saga_cmd ta_morphometry

# Run tool
saga_cmd ta_morphometry 0 \
  -ELEVATION=dem.tif \
  -SLOPE=slope.tif \
  -ASPECT=aspect.tif
```

### GRASS GIS (CLI + Python)

**Command-Line:**
```bash
grass /path/to/location/mapset
r.slope.aspect elevation=dem slope=slope
```

**Python:**
```python
import grass.script as gscript
gscript.run_command('r.slope.aspect', elevation='dem', slope='slope')
```

### Whitebox Tools (CLI)

```bash
# List tools
whitebox_tools --listtools

# Tool help
whitebox_tools --toolhelp=Slope

# Run tool
whitebox_tools --run=Slope \
  --input=dem.tif \
  --output=slope.tif
```

### OTB (CLI)

```bash
# List applications
otbcli_-h

# Run application
otbcli_BandMath \
  -il image.tif \
  -out result.tif \
  -exp "im1b1 + im1b2"
```

### Python Libraries

```python
# Standard imports after environment initialization
import geopandas as gpd
import rasterio
import xarray as xr
from pyspatialml import Raster
import torch
import tensorflow as tf
```

## Directory Structure

```
/workspace/
├── data/           # Input data (mount here)
├── output/         # Results (mount here)
├── scripts/        # Scripts
├── notebooks/      # Jupyter notebooks
└── samples/        # Examples

/opt/
├── grass/          # GRASS GIS 8.4.0
├── saga/           # SAGA GIS 9.3.2
└── otb/            # OTB 9.1.1
```

## Verification

### Quick Check

```python
import sys
packages = ['numpy', 'pandas', 'geopandas', 'rasterio', 
            'torch', 'tensorflow', 'pyvista']
for pkg in packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg}")
```

### Full Test

See example notebook:
[Test_SAGA, GRASS, OTB, Whitebox and Python Packages.ipynb](https://github.com/Geoinformatics-Lab/PyGILE-Plus/blob/main/example_notebooks/)

## Troubleshooting

### Jupyter Not Accessible

```bash
# Check container status
docker ps

# Check port availability
lsof -i :8888  # Linux/Mac
netstat -ano | findstr :8888  # Windows

# Try different port
docker run -p 8889:8888 dockagile/pygile-plus:latest

# View logs
docker logs pygile-plus
```

### CLI Tools Not Found

```bash
# Enter container
docker exec -it pygile-plus bash

# Source environment
source /workspace/pygile_working_env.sh

# Check PATH
echo $PATH

# Manual PATH setup if needed
export PATH="/opt/saga/bin:/opt/grass/bin:$PATH"
```

### Import Errors

```python
# Check Python path
import sys
print(sys.executable)  # Should be /opt/conda/envs/pygile/bin/python

# Check package installation
import subprocess
subprocess.run(['mamba', 'list'], check=True)
```

```bash
# In terminal
conda activate pygile
mamba list | grep package-name
```

### Out of Memory

```bash
# Increase memory
docker run --memory=16g --memory-swap=16g dockagile/pygile-plus:latest

# Increase shared memory
docker run --shm-size=4g dockagile/pygile-plus:latest

# Use chunked processing
import dask.array as da
```

### Slow Performance

```bash
# More CPU cores
docker run --cpus=8 dockagile/pygile-plus:latest

# Use SSD for data
docker run -v /ssd/path:/workspace/data dockagile/pygile-plus:latest
```

### Permission Issues

```bash
# Map user ID
docker run --user $(id -u):$(id -g) dockagile/pygile-plus:latest

# Or fix permissions
chmod -R 777 /path/to/data
```

## Example Workflows

### Terrain Analysis

```bash
docker run -it --name terrain \
  -p 8888:8888 \
  -v /path/to/dem:/workspace/data \
  dockagile/pygile-plus:latest

# In container terminal
docker exec -it terrain bash
source /workspace/pygile_working_env.sh

saga_cmd ta_morphometry 0 \
  -ELEVATION=/workspace/data/dem.tif \
  -SLOPE=/workspace/data/slope.tif
```

### Machine Learning

```python
# In Jupyter (http://localhost:8888)

# Initialize (first cell)
import os, sys
os.environ['LD_LIBRARY_PATH'] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib"
sys.path.insert(0, '/opt/grass/etc/python')

# Process
from pyspatialml import Raster
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier

stack = Raster(['band1.tif', 'band2.tif', 'band3.tif'])
training = gpd.read_file('training.shp')
X, y, coords = stack.extract_vector(training, field='class')

clf = RandomForestClassifier(n_estimators=200)
clf.fit(X, y)
prediction = stack.predict(clf, output='classification.tif')
```

## Performance Tips

**For Large Datasets:**
```bash
docker run --memory=16g --cpus=8 --shm-size=4g dockagile/pygile-plus:latest
```

**Chunked Processing:**
```python
import rioxarray
data = rioxarray.open_rasterio('large.tif', chunks={'x': 512, 'y': 512})
```

**Batch Processing:**
```bash
docker run -d dockagile/pygile-plus:latest
docker exec pygile-plus python /workspace/scripts/process.py
```

## Additional Resources

- Main README: [../README.md](../README.md)
- Algorithm Catalogs: [../algorithms_toc/](../algorithms_toc/)
- Example Notebooks: [../example_notebooks/](../example_notebooks/)
- GitHub: https://github.com/Geoinformatics-Lab/PyGILE-Plus
- Docker Hub: https://hub.docker.com/r/dockagile/pygile-plus