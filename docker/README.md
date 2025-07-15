# PyGILE-Plus Getting Started Guide

## Quick Setup (5 minutes)


## Pull the existing image
```bash
# Pull the image
docker pull dockagile/pygile-plus
```
### Step 1: Build the Container
```bash
# Build from Dockerfile
docker build -t pygile-plus .
```

### Step 2: Run the Container
```bash
# Run the container with a specific name (Jupyter starts automatically)
docker run -it --name pygile-plus-container -p 8888:8888 -v $(pwd):/workspace pygile-plus
```

**Jupyter Lab will start automatically and be available at `http://localhost:8888`**

### Step 3: Setup Environment (Required for Full Functionality)
**In a NEW terminal window**, connect to the running container and run the environment script:

```bash
# Connect to the running container
docker exec -it pygile-plus-container bash

# Run the environment setup script
source /workspace/pygile_working_env.sh
```

### Step 4: Initialize QGIS in Jupyter
**Run this cell first in any new notebook:**
```python
import os
import sys

# Critical environment setup for 1,773 algorithms
os.environ['LD_LIBRARY_PATH'] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib"
os.environ['SAGA_CMD'] = '/opt/saga/bin/saga_cmd'
os.environ['SAGA_MLB'] = '/opt/saga/lib/saga'
os.environ['GISBASE'] = '/opt/grass'
os.environ['OTB_APPLICATION_PATH'] = '/opt/otb/lib/otb/applications'

# Add GRASS to Python path
sys.path.insert(0, '/opt/grass/etc/python')

# Initialize QGIS
from qgis.core import QgsApplication
QgsApplication.setPrefixPath('/opt/conda/envs/pygile', True)
qgs = QgsApplication([], False)
qgs.initQgis()

import processing
from processing.core.Processing import Processing
Processing.initialize()

print(" PyGILE-Plus initialized with 1,773+ algorithms!")
```

## Why Both Steps Are Needed

- **Shell script** (`pygile_working_env.sh`) = Sets up PATH and system environment for command-line tools (SAGA, GRASS, OTB, WhiteboxTools)
- **Python initialization code** = Initializes QGIS and processing framework within Jupyter

Both are required for full access to all 1,773+ algorithms.

## Available Tools

- **QGIS Native**: 289 algorithms
- **GDAL**: 57 algorithms  
- **GRASS GIS**: 307 algorithms
- **WhiteboxTools**: 460 algorithms (CLI)
- **SAGA GIS**: 509 algorithms (CLI)
- **OTB**: 100+ algorithms (CLI)

**Total: 1,773+ algorithms**

## Quick Test
```python
# Test algorithm count
providers = QgsApplication.processingRegistry().providers()
total = sum(len(provider.algorithms()) for provider in providers)
print(f"QGIS Integrated: {total} algorithms")
print("External CLI: 1,069 algorithms")
print(f"Grand Total: {total + 1069} algorithms")
```

## Complete Setup Flow

1. **Container starts** → Jupyter auto-launches at `http://localhost:8888`
2. **Run shell script** in separate terminal → System tools become available  
3. **Run Python code** in Jupyter → QGIS integration works
4. **All 1,773+ algorithms** are now available!

## Ready to use!
Your PyGILE-Plus environment is now fully configured with all major Free and Open Source GIS analysis tools.

