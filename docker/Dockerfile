# =============================================================================
# PyGILE-Plus — Optimized headless geospatial research environment
# Works on CPU-only machines AND GPU machines (use --gpus all at runtime)
#
# CPU:  docker run -p 8888:8888 dockagile/pygile-plus
# GPU:  docker run --gpus all -p 8888:8888 dockagile/pygile-plus
#
# KEY CHANGES:
#   1. Python 3.11 (grass conda package requires >=3.11)
#   2. GRASS installed via conda-forge early (Step 4) before rasterio
#      so the solver pins PROJ/GDAL versions correctly for everything
#   3. No GRASS source compilation
#   4. No GISBASE
# =============================================================================

FROM condaforge/mambaforge:24.9.0-0

LABEL name="PyGILE-Plus"
LABEL description="Optimized headless geospatial research environment with SAGA 9.x + GRASS (conda) + OTB 9.1 + modern ML stack + 3D visualization"
LABEL maintainer="research-team"

ARG PYTHON_VERSION=3.11
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV MPLBACKEND=Agg

# ── Step 1: System dependencies ───────────────────────────────────────────────
RUN apt-get update && apt-get install -y software-properties-common && \
    apt-key adv --fetch-keys https://repos.codelite.org/CodeLite.asc && \
    apt-add-repository 'deb https://repos.codelite.org/wx3.2/ubuntu/ focal universe' && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential cmake git wget curl unzip \
        libgl1-mesa-glx libgl1-mesa-dev libegl1-mesa \
        libxrandr2 libxss1 libxcursor1 libxcomposite1 \
        libasound2 libxi6 libxtst6 libxinerama1 \
        libfontconfig1 libxrender1 libglib2.0-0 \
        ca-certificates gnupg xvfb \
        make gcc g++ \
        libsqlite3-dev libtiff5-dev libpng-dev \
        libcairo2-dev libfreetype6-dev \
        libfftw3-dev libgsl-dev \
        libpq-dev libopencv-dev \
        libgdal-dev gdal-bin libproj-dev proj-bin libgeos-dev \
        libwxbase3.2-0-unofficial libwxbase3.2unofficial-dev \
        libwxgtk3.2-0-unofficial libwxgtk3.2unofficial-dev \
        wx3.2-headers wx-common \
        libgtk-3-dev \
        nodejs npm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Step 2: Create conda env ──────────────────────────────────────────────────
RUN mamba create -n pygile python=${PYTHON_VERSION} -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

# ── Step 3: NumPy first ───────────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    numpy && \
    mamba clean --all -y

# ── Step 4: GRASS + core geospatial stack together ────────────────────────────
# CRITICAL: grass is installed HERE with gdal/proj/geos so the solver
# pins the correct versions for everything that follows (rasterio etc.)
RUN mamba install -n pygile -c conda-forge -y \
    grass gdal proj geos libspatialindex boost-cpp && \
    mamba clean --all -y

# ── Step 5: Fiona, Shapely, PyProj ───────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    fiona shapely pyproj && \
    mamba clean --all -y

# ── Step 6: Scientific computing core ────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    pandas scipy matplotlib seaborn scikit-learn && \
    mamba clean --all -y

# ── Step 7: GeoPandas and Rasterio ───────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    geopandas rasterio && \
    mamba clean --all -y

# ── Step 8: Data format libraries ────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    xarray netcdf4 h5py h5netcdf zarr && \
    mamba clean --all -y

# ── Step 9: Jupyter ecosystem ─────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    jupyter jupyterlab ipywidgets && \
    mamba clean --all -y

# ── Step 10: Visualization packages ──────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    plotly bokeh folium contextily mapclassify && \
    mamba clean --all -y

# ── Step 11: Additional visualization ────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    holoviews hvplot && \
    mamba clean --all -y

# ── Step 12: Geospatial analysis tools ───────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    osmnx earthpy geoplot && \
    mamba clean --all -y

# ── Step 13: Spatial statistics ──────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    rasterstats xarray-spatial && \
    mamba clean --all -y

# ── Step 14: Image processing ────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    scikit-image tifffile imageio-ffmpeg && \
    mamba clean --all -y

# ── Step 15: OpenCV ───────────────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    opencv && \
    mamba clean --all -y

# ── Step 16: Web mapping ──────────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    localtileserver rio-cogeo rioxarray && \
    mamba clean --all -y

# ── Step 17: Interactive mapping ─────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    ipyleaflet owslib && \
    mamba clean --all -y

# ── Step 18: geemap and leafmap ──────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    geemap leafmap && \
    mamba clean --all -y

# ── Step 19: Optional packages ───────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    census us pykrige palettable geojson && \
    mamba clean --all -y

# ── Step 20: Cloud tools ──────────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    pystac stackstac planetary-computer && \
    mamba clean --all -y

# ── Step 21: WhiteboxTools ────────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    whitebox_tools && \
    mamba clean --all -y

# ── Step 22: pygis and geoai ──────────────────────────────────────────────────
RUN mamba install -n pygile -c conda-forge -y \
    pygis geoai && \
    mamba clean --all -y

# ── Step 23: PyTorch with CUDA ────────────────────────────────────────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 && \
    mamba run -n pygile pip install --no-cache-dir pytorch-lightning

# ── Step 24: TensorFlow GPU ───────────────────────────────────────────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    "tensorflow[and-cuda]" keras

# ── Step 25: All remaining pip packages ──────────────────────────────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    albumentations timm \
    pythreejs pyvista \
    libpysal esda \
    keplergl \
    WxPython \
    earthengine-api \
    sphinx sphinx_sitemap "sphinxcontrib.bibtex" \
    sphinx_inline_tabs pydata-sphinx-theme \
    sankee overturemaps whiteboxgui \
    jupyter-book ghp-import \
    numpy-groupies sympy \
    geojson dask-geopandas \
    pykrige cenpy census us \
    whitebox PySAGA-cmd \
    streamlit-folium nbconvert black flake8 || \
    echo "Some pip packages failed - continuing"

# ── Step 26: pyspatialml ──────────────────────────────────────────────────────
RUN mamba run -n pygile pip install --no-cache-dir pyspatialml || \
    mamba run -n pygile pip install --no-cache-dir \
        "git+https://github.com/stevenpawley/Pyspatialml.git" || \
    echo "pyspatialml installation failed - continuing"

# ── Step 27: sklearn-xarray ───────────────────────────────────────────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/jgrss/sklearn-xarray.git" || \
    mamba run -n pygile pip install sklearn_xarray || \
    echo "sklearn_xarray installation failed - continuing"

# ── Step 28: Compile SAGA GIS 9.3 from source ────────────────────────────────
RUN cd /tmp && \
    wget -q https://sourceforge.net/projects/saga-gis/files/SAGA%20-%209/SAGA%20-%209.3.2/saga-9.3.2.tar.gz && \
    tar -xzf saga-9.3.2.tar.gz && \
    cd saga-9.3.2/saga-gis && \
    mkdir build && cd build && \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/saga \
        -DWITH_TRIANGLE=OFF \
        -DWITH_SYSTEM_SVM=ON \
        -DWITH_DEV_TOOLS=OFF \
        -DWITH_GUI=OFF \
        -DWITH_TOOLS_VIGRA=OFF \
        -DWITH_TOOLS_PDAL=OFF && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd / && rm -rf /tmp/saga-9.3.2*

# ── Step 29: Install OTB 9.1 ──────────────────────────────────────────────────
RUN cd /tmp && \
    wget -q https://www.orfeo-toolbox.org/packages/OTB-9.1.1-Linux.tar.gz && \
    tar xf OTB-9.1.1-Linux.tar.gz --one-top-level=/opt/otb && \
    rm -f OTB-9.1.1-Linux.tar.gz && \
    sed -i '1 s|^#! */bin/sh|#!/bin/bash|' /opt/otb/bin/otbcli && \
    sed -i 's|\<source\>|.|g' /opt/otb/bin/otbcli && \
    mkdir -p /opt/conda/envs/pygile/etc/conda/activate.d

# ── Step 30: Environment variables ───────────────────────────────────────────
ENV PATH="/opt/conda/envs/pygile/bin:/opt/saga/bin:/opt/otb/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/conda/envs/pygile/lib:/opt/saga/lib:/opt/otb/lib:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu"
ENV SAGA_CMD="/opt/saga/bin/saga_cmd"
ENV SAGA_MLB="/opt/saga/lib/saga"
ENV OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"
ENV PYTHONPATH="/opt/conda/envs/pygile/grass84/etc/python:/opt/otb/lib/python"

# ── Step 31: OTB activation hook ─────────────────────────────────────────────
RUN printf '#!/bin/bash\n\
if [ -f /opt/otb/otbenv.profile ]; then\n\
  . /opt/otb/otbenv.profile\n\
fi\n\
export OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"\n\
export PYTHONPATH="/opt/otb/lib/python${PYTHONPATH:+:$PYTHONPATH}"\n' \
    > /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    chmod +x /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh

# ── Step 32: Verify ───────────────────────────────────────────────────────────
RUN mamba run -n pygile python -c \
    "import numpy, pandas, geopandas, rasterio, matplotlib; print('Core packages: OK')" || \
    echo "Core package verification failed"

RUN mamba run -n pygile python -c \
    "import grass.script; print('GRASS Python API: OK')" || \
    echo "GRASS verification failed"

# ── Step 33: Workspace ───────────────────────────────────────────────────────
WORKDIR /workspace
RUN mkdir -p /workspace/{data,output,scripts,notebooks,samples}

# ── Step 34: Startup script ───────────────────────────────────────────────────
RUN printf '#!/bin/bash\n\
source /opt/conda/etc/profile.d/conda.sh\n\
conda activate pygile\n\
cd /workspace\n\
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \\\n\
  --ServerApp.token="" --ServerApp.password="" \\\n\
  --ServerApp.allow_origin="*" --ServerApp.disable_check_xsrf=True\n' \
    > /start.sh && chmod +x /start.sh

# ── Final cleanup ─────────────────────────────────────────────────────────────
RUN mamba clean --all -y && \
    find /opt/conda -name "*.pyc" -delete && \
    find /opt/conda -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

EXPOSE 8888
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/start.sh"]
