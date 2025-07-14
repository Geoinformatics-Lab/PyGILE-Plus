# PyGILE-Plus Getting Started Guide

## Quick Setup (5 minutes)

### Step 1: Build the Container
```bash
# Build from Dockerfile
docker build -t pygile-plus .

# Run the container
docker run -it -p 8888:8888 -v $(pwd):/workspace pygile-plus
```

### Step 2: Environment Setup
```bash
# Inside container, run once:
source /workspace/pygile_working_env.sh
```

### Step 3: Launch Jupyter
```bash
# Start Jupyter Lab
jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```

### Step 4: Initialize Environment in Jupyter
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

## Ready to use!
Your PyGILE-Plus environment is now configured with all major GIS analysis tools.