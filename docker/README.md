# PyGILE-Plus Docker Setup

Setup and usage instructions for the PyGILE-Plus Docker container.

## Installation

### Pull Pre-built Image

```bash
docker pull dockagile/pygile-plus
```

### Build from Source

```bash
git clone https://github.com/Geoinformatics-Lab/PyGILE-Plus.git
cd PyGILE-Plus/docker
docker build -t pygile-plus .
```

Build time: ~30-45 minutes

## Running the Container

### Basic Run (CPU only)

```bash
docker run -it --name pygile-plus \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

Jupyter Lab starts automatically at `http://localhost:8888`

### With GPU Support

```bash
docker run -it --name pygile-plus \
  --gpus all \
  -p 8888:8888 \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

Requires NVIDIA GPU + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) on the host.

### With Resource Allocation

```bash
docker run -it --name pygile-plus \
  --gpus all \
  -p 8888:8888 \
  --memory=16g \
  --cpus=8 \
  --shm-size=2g \
  -v $(pwd)/data:/workspace/data \
  dockagile/pygile-plus
```

### Custom Port

```bash
docker run -it --name pygile-plus \
  -p 8889:8888 \
  dockagile/pygile-plus
```

## HPC / Apptainer (Singularity)

```bash
# Pull and convert from Docker Hub
apptainer pull docker://dockagile/pygile-plus

# Run with GPU passthrough
apptainer run --nv pygile-plus_latest.sif
```

## Environment Setup

### Jupyter Notebooks — First Cell

```python
import os, sys
os.environ['LD_LIBRARY_PATH'] = "/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu:/opt/conda/envs/pygile/lib"
os.environ['SAGA_CMD'] = '/opt/saga/bin/saga_cmd'
os.environ['SAGA_MLB'] = '/opt/saga/lib/saga'
os.environ['GISBASE'] = '/opt/grass'
os.environ['OTB_APPLICATION_PATH'] = '/opt/otb/lib/otb/applications'
sys.path.insert(0, '/opt/grass/etc/python')
print("PyGILE-Plus environment initialized")
```

### Command-Line

```bash
docker exec -it pygile-plus bash
source /workspace/pygile_working_env.sh
```

## Tool Paths

```python
conda_env_path = "/opt/conda/envs/pygile"
saga_cmd       = "/opt/saga/bin/saga_cmd"
saga_lib       = "/opt/saga/lib/saga"
grass_bin      = "/opt/grass/bin"
otb_bin        = "/opt/otb/bin"
whitebox_tools = "/opt/conda/envs/pygile/bin/whitebox_tools"
```

## Container Management

```bash
docker stop pygile-plus
docker start pygile-plus
docker restart pygile-plus
docker logs pygile-plus
docker rm pygile-plus
docker rmi dockagile/pygile-plus
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
- **Algorithm Catalog:** [notebooks/pygile_plus_algorithm_catalog.ipynb](notebooks/pygile_plus_algorithm_catalog.ipynb) — generates full algorithm list for SAGA, GRASS, OTB, and Whitebox as CSV/Excel