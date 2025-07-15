FROM condaforge/mambaforge:24.9.0-0

# PyGILE-Plus: 5-year stable headless geospatial research environment
LABEL name="PyGILE-Plus"
LABEL description="5-year stable headless geospatial research environment with SAGA 9.x + GRASS 8.4 + latest QGIS"
LABEL version="1.2.0"
LABEL maintainer="research-team"

ARG PYTHON_VERSION=3.11
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

# Create conda environment with strict conda-forge priority
RUN mamba create -n pygile python=${PYTHON_VERSION} -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

# Install LATEST STABLE core geospatial stack
RUN mamba install -n pygile -c conda-forge -y \
    gdal proj geos libspatialindex boost-cpp \
    && mamba clean -all -y

# Scientific computing core - latest stable versions
RUN mamba install -n pygile -c conda-forge -y \
    numpy pandas scipy matplotlib seaborn \
    scikit-learn xarray netcdf4 h5py h5netcdf \
    && mamba clean -all -y

# Core geospatial packages - latest versions
RUN mamba install -n pygile -c conda-forge -y \
    geopandas rasterio shapely pyproj fiona \
    && mamba clean -all -y

# Additional geospatial packages - latest stable
RUN mamba install -n pygile -c conda-forge -y \
    contextily folium osmnx earthpy mapclassify geoplot \
    && mamba clean -all -y

# QGIS LTR - latest stable for 5-year support
RUN mamba install -n pygile -c conda-forge -y \
    qgis \
    && mamba clean -all -y

# Deep Learning frameworks - CPU versions for stability (no CUDA conflicts)
RUN mamba install -n pygile -c conda-forge -y \
    pytorch-cpu torchvision torchaudio \
    && mamba clean -all -y

# Install TensorFlow via pip for better compatibility
RUN mamba run -n pygile pip install --no-cache-dir \
    tensorflow keras

# Additional ML/DL tools - latest versions
RUN mamba install -n pygile -c conda-forge -y \
    scikit-image opencv pytorch-lightning \
    && mamba clean -all -y

# Install additional packages via pip
RUN mamba run -n pygile pip install --no-cache-dir \
    albumentations timm

# Jupyter and visualization - latest stable
RUN mamba install -n pygile -c conda-forge -y \
    jupyter jupyterlab ipywidgets \
    plotly bokeh holoviews hvplot \
    && mamba clean -all -y

# Python packages via pip - latest stable versions only
RUN mamba run -n pygile pip install --no-cache-dir \
    sympy numpy-groupies \
    geojson dask-geopandas \
    pykrige cenpy census us \
    sklearn-xarray whitebox \
    PySAGA-cmd

# Download and compile GRASS GIS 8.4 from source - FIXED WITH PYTHON SUPPORT
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
        --with-python=/opt/conda/envs/pygile/bin/python \
        --without-postgres \
        --without-mysql \
        --without-odbc \
        --without-pdal \
        --without-openmp && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    echo "GNU General Public License" > /opt/grass/etc/license && \
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
        -DWITH_TOOLS_VIGRA=OFF \
        -DWITH_TOOLS_PDAL=OFF && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd / && rm -rf /tmp/saga-9.3.2*

# Install WhiteboxTools via conda-forge
RUN mamba install -n pygile -c conda-forge -y \
    whitebox_tools \
    && mamba clean -all -y

# Download and install OTB latest stable
RUN cd /tmp && \
    wget -q https://www.orfeo-toolbox.org/packages/OTB-9.1.1-Linux.tar.gz && \
    tar xf OTB-9.1.1-Linux.tar.gz --one-top-level=/opt/otb && \
    rm -f OTB-9.1.1-Linux.tar.gz

# Environment variables for tools
ENV PATH="/opt/grass/bin:/opt/saga/bin:/opt/otb/bin:$PATH"
ENV LD_LIBRARY_PATH="/opt/grass/lib:/opt/saga/lib:/opt/otb/lib"
ENV OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"
ENV SAGA_CMD="/opt/saga/bin/saga_cmd"
ENV GISBASE="/opt/grass"

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

EXPOSE 8888
CMD ["/start.sh"]