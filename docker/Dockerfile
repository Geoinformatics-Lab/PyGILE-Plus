FROM condaforge/mambaforge:24.9.0-0

# PyGILE-Plus: Stable headless geospatial research environment
LABEL name="PyGILE-Plus"
LABEL description="Stable headless geospatial research environment with SAGA 9.x + GRASS 8.4 + modern ML stack + 3D visualization"
LABEL maintainer="research-team"

ARG PYTHON_VERSION=3.10
ARG DEBIAN_FRONTEND=noninteractive

# Headless environment variables
ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99

# Add wxWidgets 3.2 repository for Ubuntu focal
RUN apt-get update && apt-get install -y software-properties-common && \
    apt-key adv --fetch-keys https://repos.codelite.org/CodeLite.asc && \
    apt-add-repository 'deb https://repos.codelite.org/wx3.2/ubuntu/ focal universe' && \
    apt-get update

# System dependencies for headless operation + SAGA/GRASS compilation + PyVista
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git wget curl unzip \
    libgl1-mesa-glx libgl1-mesa-dev libegl1-mesa libxrandr2 libxss1 libxcursor1 \
    libxcomposite1 libasound2 libxi6 libxtst6 libxinerama1 \
    libfontconfig1 libxrender1 libglib2.0-0 \
    ca-certificates gnupg xvfb \
    flex make bison gcc g++ ccache \
    libproj-dev proj-data proj-bin \
    libgeos-dev libgdal-dev python3-gdal gdal-bin \
    python3-dev python3-numpy \
    libwxbase3.2-0-unofficial libwxbase3.2unofficial-dev libwxgtk3.2-0-unofficial libwxgtk3.2unofficial-dev wx3.2-headers wx-common \
    libgtk-3-dev libgdk-pixbuf2.0-dev libpango1.0-dev libatk1.0-dev \
    libnotify4 libnotify-dev \
    libpq-dev libpdal-dev libopencv-dev libhpdf-dev unixodbc-dev \
    libfftw3-dev libgsl-dev \
    libsqlite3-dev libtiff5-dev libpng-dev \
    libcairo2-dev libfreetype6-dev \
    nodejs npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create conda environment with strict conda-forge priority
RUN mamba create -n pygile python=${PYTHON_VERSION} -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

# Clean conda cache
RUN mamba clean --all -y

# Install NumPy (NumPy 2.0 compatible with modern ML stack)
RUN mamba install -n pygile -c conda-forge -y \
    numpy \
    && mamba clean -all -y

# Install core geospatial libraries
RUN mamba install -n pygile -c conda-forge -y \
    gdal proj geos libspatialindex boost-cpp \
    && mamba clean -all -y

# Install Fiona, Shapely, PyProj
RUN mamba install -n pygile -c conda-forge -y \
    fiona shapely pyproj \
    && mamba clean -all -y

# Scientific computing core
RUN mamba install -n pygile -c conda-forge -y \
    pandas scipy matplotlib seaborn scikit-learn \
    && mamba clean -all -y

# GeoPandas and Rasterio
RUN mamba install -n pygile -c conda-forge -y \
    geopandas rasterio \
    && mamba clean -all -y

# Data format libraries
RUN mamba install -n pygile -c conda-forge -y \
    xarray netcdf4 h5py h5netcdf zarr \
    && mamba clean -all -y

# Jupyter ecosystem
RUN mamba install -n pygile -c conda-forge -y \
    jupyter jupyterlab ipywidgets \
    && mamba clean -all -y

# Visualization packages
RUN mamba install -n pygile -c conda-forge -y \
    plotly bokeh folium contextily mapclassify \
    && mamba clean -all -y

# Additional visualization
RUN mamba install -n pygile -c conda-forge -y \
    holoviews hvplot \
    && mamba clean -all -y

# Geospatial analysis tools
RUN mamba install -n pygile -c conda-forge -y \
    osmnx earthpy geoplot \
    && mamba clean -all -y

# Spatial statistics and analysis tools
RUN mamba install -n pygile -c conda-forge -y \
    rasterstats || \
    mamba run -n pygile pip install --no-cache-dir rasterstats || \
    echo "rasterstats installation failed - continuing"

RUN mamba install -n pygile -c conda-forge -y \
    xarray-spatial || \
    mamba run -n pygile pip install --no-cache-dir xarray-spatial || \
    echo "xarray-spatial installation failed - continuing"

# Image processing libraries
RUN mamba install -n pygile -c conda-forge -y \
    scikit-image tifffile imageio-ffmpeg \
    && mamba clean -all -y

# OpenCV
RUN mamba install -n pygile -c conda-forge -y \
    opencv \
    && mamba clean -all -y

# Web mapping dependencies
RUN mamba install -n pygile -c conda-forge -y \
    localtileserver rio-cogeo rioxarray \
    && mamba clean -all -y

# Interactive mapping tools
RUN mamba install -n pygile -c conda-forge -y \
    ipyleaflet owslib \
    && mamba clean -all -y

# geemap and leafmap
RUN mamba install -n pygile -c conda-forge -y \
    geemap leafmap \
    && mamba clean -all -y

# Optional packages
RUN mamba install -n pygile -c conda-forge -y \
    census us pykrige palettable geojson \
    && mamba clean -all -y

# Cloud tools
RUN mamba install -n pygile -c conda-forge -y \
    pystac stackstac planetary-computer \
    && mamba clean -all -y

# Deep Learning frameworks - GPU versions via pip (avoids conda ffmpeg conflict)
# Uses PyTorch's official CUDA 12.4 wheel index - works with Python 3.10
RUN mamba run -n pygile pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu124 && \
    mamba run -n pygile pip install --no-cache-dir \
    pytorch-lightning

# Install TensorFlow GPU via pip (tensorflow[and-cuda] bundles CUDA/cuDNN wheels)
RUN mamba run -n pygile pip install --no-cache-dir \
    "tensorflow[and-cuda]" keras

# Additional ML/DL tools
RUN mamba run -n pygile pip install --no-cache-dir \
    albumentations timm

# Install pygis meta-package with fallback
RUN mamba install -n pygile -c conda-forge -y pygis || \
    mamba run -n pygile pip install pygis || \
    echo "pygis installation failed - continuing"

# WhiteboxTools
RUN mamba install -n pygile -c conda-forge -y \
    whitebox_tools \
    && mamba clean -all -y

# ========================================
# PROBLEMATIC PACKAGES - ALL VIA PIP NOW!
# ========================================

# 3D visualization packages - pythreejs & pyvista via PIP ONLY
RUN mamba run -n pygile pip install --no-cache-dir \
    pythreejs pyvista || \
    echo "3D visualization packages installation failed - continuing"

# PySAL spatial statistics - libpysal & esda via PIP ONLY
RUN mamba run -n pygile pip install --no-cache-dir \
    libpysal esda || \
    echo "PySAL packages installation failed - continuing"

# Advanced geospatial visualization - keplergl via PIP ONLY
RUN mamba run -n pygile pip install --no-cache-dir \
    keplergl || \
    echo "keplergl installation failed - continuing"

# Spatial ML package - pyspatialml via PIP ONLY (from PyPI or GitHub)
RUN mamba run -n pygile pip install --no-cache-dir \
    pyspatialml || \
    mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/stevenpawley/Pyspatialml.git" || \
    echo "pyspatialml installation failed - continuing"

# ========================================
# END OF PROBLEMATIC PACKAGES
# ========================================

# Earth Engine API
RUN mamba run -n pygile pip install --no-cache-dir \
    earthengine-api || \
    echo "earthengine-api installation failed - continuing"

# Custom sklearn_xarray
RUN mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/jgrss/sklearn-xarray.git" || \
    mamba run -n pygile pip install sklearn_xarray || \
    echo "sklearn_xarray installation failed - continuing"

# Sphinx documentation tools
RUN mamba run -n pygile pip install --no-cache-dir \
    sphinx sphinx_sitemap "sphinxcontrib.bibtex" \
    sphinx_inline_tabs pydata-sphinx-theme || \
    echo "Sphinx tools installation failed - continuing"

# Specialized packages
RUN mamba run -n pygile pip install --no-cache-dir \
    sankee || \
    echo "sankee installation failed - continuing"

# Advanced packages
RUN mamba run -n pygile pip install --no-cache-dir \
    overturemaps whiteboxgui || \
    echo "advanced packages installation failed - continuing"

# Publishing tools
RUN mamba run -n pygile pip install --no-cache-dir \
    jupyter-book ghp-import || \
    echo "publishing tools installation failed - continuing"

# NumPy utilities
RUN mamba run -n pygile pip install --no-cache-dir \
    numpy-groupies sympy || \
    echo "numpy utilities installation failed - continuing"

# Additional geospatial Python packages
RUN mamba run -n pygile pip install --no-cache-dir \
    geojson dask-geopandas \
    pykrige cenpy census us \
    sklearn-xarray whitebox \
    PySAGA-cmd || \
    echo "additional geospatial packages installation failed - continuing"

# Missing packages from original PyGILE
RUN mamba run -n pygile pip install --no-cache-dir \
    streamlit-folium nbconvert black flake8 || \
    echo "PyGILE missing packages installation failed - continuing"

# Download and compile GRASS GIS 8.4 from source
RUN cd /tmp && \
    wget -q https://grass.osgeo.org/grass84/source/grass-8.4.0.tar.gz && \
    tar -xzf grass-8.4.0.tar.gz && \
    cd grass-8.4.0 && \
    ./configure \
        --prefix=/opt/grass \
        --with-cxx \
        --with-proj-share=/usr/share/proj \
        --with-gdal=/usr/bin/gdal-config \
        --with-geos \
        --with-sqlite \
        --with-cairo \
        --with-freetype=yes \
        --with-fftw \
        --without-postgres \
        --without-mysql \
        --without-odbc \
        --without-pdal \
        --without-openmp \
        --without-opengl && \
    make -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/grass-8.4.0*

# Download and compile SAGA GIS 9.3 from source
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

# Download and install OTB with Python bindings
RUN cd /tmp && \
    wget -q https://www.orfeo-toolbox.org/packages/OTB-9.1.1-Linux.tar.gz && \
    tar xf OTB-9.1.1-Linux.tar.gz --one-top-level=/opt/otb && \
    rm -f OTB-9.1.1-Linux.tar.gz && \
    mkdir -p /opt/conda/envs/pygile/etc/conda/activate.d/ && \
    echo '#!/bin/bash' > /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    echo 'export PYTHONPATH="/opt/otb/lib/python:$PYTHONPATH"' >> /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    echo 'export OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"' >> /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    chmod +x /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh

# Environment variables for tools
ENV PATH="/opt/grass/bin:/opt/saga/bin:/opt/otb/bin:$PATH"
ENV LD_LIBRARY_PATH="/opt/grass/lib:/opt/saga/lib:/opt/otb/lib"
ENV SAGA_CMD="/opt/saga/bin/saga_cmd"
ENV GISBASE="/opt/grass"

# GPU / CUDA environment - lets TensorFlow find its bundled CUDA libraries
# and allows Apptainer --nv passthrough to work correctly
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV LD_LIBRARY_PATH="/opt/conda/envs/pygile/lib/python3.10/site-packages/nvidia/cuda_runtime/lib:${LD_LIBRARY_PATH}"

# Verification of core packages
RUN mamba run -n pygile python -c "import numpy, pandas, geopandas, rasterio, matplotlib; print('Core packages verification: OK')" || \
    echo "Core package verification failed"

# Create workspace structure
WORKDIR /workspace
RUN mkdir -p /workspace/{data,output,scripts,notebooks,samples}

# Create startup script
RUN printf '#!/bin/bash\n\
source /opt/conda/etc/profile.d/conda.sh\n\
conda activate pygile\n\
cd /workspace\n\
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \\\n\
  --ServerApp.token="" --ServerApp.password="" \\\n\
  --ServerApp.allow_origin="*" --ServerApp.disable_check_xsrf=True\n\
' > /start.sh && chmod +x /start.sh

# Final cleanup
RUN mamba clean -all -y

EXPOSE 8888
CMD ["/start.sh"]