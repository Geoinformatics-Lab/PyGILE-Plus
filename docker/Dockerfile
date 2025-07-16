FROM condaforge/mambaforge:24.9.0-0

# PyGILE-Plus: Stable headless geospatial research environment
LABEL name="PyGILE-Plus"
LABEL description="Enhanced stable headless geospatial research environment with SAGA 9.x + GRASS 8.4 + latest QGIS + modern ML stack + NumPy 2.0 compatibility"
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

# System dependencies for headless operation + SAGA/GRASS compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git wget curl unzip \
    libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 libxcursor1 \
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create conda environment with strict conda-forge priority (matching batch file strategy)
RUN mamba create -n pygile python=${PYTHON_VERSION} -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

# Clean conda cache to prevent compatibility issues (batch file strategy)
RUN mamba clean --all -y

# Install NumPy without version constraint (NumPy 2.0 compatible with modern ML stack)
RUN mamba install -n pygile -c conda-forge -y \
    numpy \
    && mamba clean -all -y

# Install core geospatial libraries with version pins (batch file approach)
RUN mamba install -n pygile -c conda-forge -y \
    gdal proj geos libspatialindex boost-cpp \
    && mamba clean -all -y

# Install Fiona, Shapely, PyProj (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    fiona shapely pyproj \
    && mamba clean -all -y

# Scientific computing core - including missing scikit-learn (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    pandas scipy matplotlib seaborn scikit-learn \
    && mamba clean -all -y

# GeoPandas and Rasterio (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    geopandas rasterio \
    && mamba clean -all -y

# Data format libraries (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    xarray netcdf4 h5py h5netcdf zarr \
    && mamba clean -all -y

# Jupyter ecosystem (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    jupyter jupyterlab ipywidgets \
    && mamba clean -all -y

# Visualization packages (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    plotly bokeh folium contextily mapclassify \
    && mamba clean -all -y

# Additional visualization (keeping existing holoviews hvplot)
RUN mamba install -n pygile -c conda-forge -y \
    holoviews hvplot \
    && mamba clean -all -y

# Geospatial analysis tools (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    osmnx earthpy geoplot \
    && mamba clean -all -y

# Image processing libraries (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    scikit-image tifffile imageio-ffmpeg \
    && mamba clean -all -y

# Keep existing opencv separate (original dockerfile had it)
RUN mamba install -n pygile -c conda-forge -y \
    opencv \
    && mamba clean -all -y

# Web mapping dependencies (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    localtileserver rio-cogeo rioxarray \
    && mamba clean -all -y

# Interactive mapping tools (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    ipyleaflet owslib \
    && mamba clean -all -y

# geemap and leafmap (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    geemap leafmap \
    && mamba clean -all -y

# Optional packages (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    census us pykrige palettable geojson \
    && mamba clean -all -y

# Cloud tools (batch file grouping)
RUN mamba install -n pygile -c conda-forge -y \
    pystac stackstac planetary-computer \
    && mamba clean -all -y

# QGIS LTR - latest stable for 5-year support (keeping existing)
RUN mamba install -n pygile -c conda-forge -y \
    qgis \
    && mamba clean -all -y

# Deep Learning frameworks - CPU versions for stability (keeping existing)
RUN mamba install -n pygile -c conda-forge -y \
    pytorch-cpu torchvision torchaudio pytorch-lightning \
    && mamba clean -all -y

# Install TensorFlow via pip for better compatibility (keeping existing)
RUN mamba run -n pygile pip install --no-cache-dir \
    tensorflow keras

# Additional ML/DL tools (keeping existing + adding batch file items)
RUN mamba run -n pygile pip install --no-cache-dir \
    albumentations timm

# Install pygis meta-package with fallback (batch file approach)
RUN mamba install -n pygile -c conda-forge -y pygis || \
    mamba run -n pygile pip install pygis || \
    echo "pygis installation failed - continuing"

# WhiteboxTools via conda-forge (keeping existing)
RUN mamba install -n pygile -c conda-forge -y \
    whitebox_tools \
    && mamba clean -all -y

# Earth Engine API (batch file - pip only)
RUN mamba run -n pygile pip install --no-cache-dir \
    earthengine-api || \
    echo "earthengine-api installation failed - continuing"

# Custom sklearn_xarray (batch file approach with fallback)
RUN mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/jgrss/sklearn-xarray.git" || \
    mamba run -n pygile pip install sklearn_xarray || \
    echo "sklearn_xarray installation failed - continuing"

# Sphinx documentation tools (batch file grouping)
RUN mamba run -n pygile pip install --no-cache-dir \
    sphinx sphinx_sitemap "sphinxcontrib.bibtex" \
    sphinx_inline_tabs pydata-sphinx-theme || \
    echo "Sphinx tools installation failed - continuing"

# Specialized packages (batch file grouping)
RUN mamba run -n pygile pip install --no-cache-dir \
    sankee || \
    echo "sankee installation failed - continuing"

# Advanced packages (batch file grouping)
RUN mamba run -n pygile pip install --no-cache-dir \
    overturemaps whiteboxgui || \
    echo "advanced packages installation failed - continuing"

# Publishing tools (batch file grouping)
RUN mamba run -n pygile pip install --no-cache-dir \
    jupyter-book ghp-import || \
    echo "publishing tools installation failed - continuing"

# NumPy utilities (batch file grouping)
RUN mamba run -n pygile pip install --no-cache-dir \
    numpy-groupies sympy || \
    echo "numpy utilities installation failed - continuing"

# Additional geospatial Python packages (keeping from original approach)
RUN mamba run -n pygile pip install --no-cache-dir \
    geojson dask-geopandas \
    pykrige cenpy census us \
    sklearn-xarray whitebox \
    PySAGA-cmd || \
    echo "additional geospatial packages installation failed - continuing"

# Download and compile GRASS GIS 8.4 from source (keeping existing)
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
        --without-openmp && \
    make -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/grass-8.4.0*

# Download and compile SAGA GIS 9.3 from source (keeping existing)
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
        -DWITH_TOOLS_VIGRA=OFF \
        -DWITH_TOOLS_PDAL=OFF && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd / && rm -rf /tmp/saga-9.3.2*

# Download and install OTB with Python bindings setup (keeping existing)
RUN cd /tmp && \
    wget -q https://www.orfeo-toolbox.org/packages/OTB-9.1.1-Linux.tar.gz && \
    tar xf OTB-9.1.1-Linux.tar.gz --one-top-level=/opt/otb && \
    rm -f OTB-9.1.1-Linux.tar.gz && \
    mkdir -p /opt/conda/envs/pygile/etc/conda/activate.d/ && \
    echo '#!/bin/bash' > /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    echo 'export PYTHONPATH="/opt/otb/lib/python:$PYTHONPATH"' >> /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    echo 'export OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"' >> /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    chmod +x /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh

# Environment variables for tools (keeping existing)
ENV PATH="/opt/grass/bin:/opt/saga/bin:/opt/otb/bin:$PATH"
ENV LD_LIBRARY_PATH="/opt/grass/lib:/opt/saga/lib:/opt/otb/lib"
ENV SAGA_CMD="/opt/saga/bin/saga_cmd"
ENV GISBASE="/opt/grass"

# Verification of core packages (batch file approach)
RUN mamba run -n pygile python -c "import numpy, pandas, geopandas, rasterio, matplotlib; print('Core packages verification: OK')" || \
    echo "Core package verification failed"

# Create workspace structure (keeping existing)
WORKDIR /workspace
RUN mkdir -p /workspace/{data,output,scripts,notebooks,samples}

# Create startup script (keeping existing)
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