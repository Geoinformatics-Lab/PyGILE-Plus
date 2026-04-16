# =============================================================================
# PyGILE-Plus — Optimized headless geospatial research environment
# Works on CPU-only machines AND GPU machines (use --gpus all at runtime)
#
# CPU:  docker run -p 8888:8888 dockagile/pygile-plus
# GPU:  docker run --gpus all -p 8888:8888 dockagile/pygile-plus
#
# Estimated size: ~22–28 GB (vs 40 GB original)
# Tools: GRASS 8.4 + SAGA 9.3 + OTB 9.1 + PyTorch (CUDA 12.4) + TensorFlow (GPU)
# =============================================================================

FROM condaforge/mambaforge:24.9.0-0

LABEL name="PyGILE-Plus"
LABEL description="Optimized headless geospatial research environment with SAGA 9.x + GRASS 8.4 + OTB 9.1 + modern ML stack + 3D visualization"
LABEL maintainer="research-team"

ARG PYTHON_VERSION=3.10
ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99
# GPU: expose all devices; harmless if no GPU present
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# ── Step 1: System dependencies ───────────────────────────────────────────────
# Identical packages to original — build tools kept (NOT purged) to avoid
# breaking runtime source builds or GRASS/SAGA plugin compilation
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
        flex make bison gcc g++ ccache \
        libproj-dev proj-data proj-bin \
        libgeos-dev libgdal-dev python3-gdal gdal-bin \
        python3-dev python3-numpy \
        libwxbase3.2-0-unofficial libwxbase3.2unofficial-dev \
        libwxgtk3.2-0-unofficial libwxgtk3.2unofficial-dev \
        wx3.2-headers wx-common \
        libgtk-3-dev libgdk-pixbuf2.0-dev libpango1.0-dev libatk1.0-dev \
        libnotify4 libnotify-dev \
        libpq-dev libopencv-dev libhpdf-dev unixodbc-dev \
        libfftw3-dev libgsl-dev \
        libsqlite3-dev libtiff5-dev libpng-dev \
        libcairo2-dev libfreetype6-dev \
        nodejs npm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ── Step 2: Create conda env + configure channels ────────────────────────────
RUN mamba create -n pygile python=${PYTHON_VERSION} -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

# ── Step 3: Install ALL conda packages in one pass ───────────────────────────
# (was 20+ separate mamba install calls — same packages, fewer layers/solves)
RUN mamba install -n pygile -c conda-forge -y \
        numpy pandas scipy matplotlib seaborn scikit-learn \
        gdal proj geos libspatialindex boost-cpp \
        fiona shapely pyproj \
        geopandas rasterio \
        xarray netcdf4 h5py h5netcdf zarr \
        jupyter jupyterlab ipywidgets \
        plotly bokeh folium contextily mapclassify \
        holoviews hvplot \
        osmnx earthpy geoplot \
        rasterstats xarray-spatial \
        scikit-image tifffile imageio-ffmpeg \
        opencv \
        localtileserver rio-cogeo rioxarray \
        ipyleaflet owslib \
        geemap leafmap \
        census us pykrige palettable geojson \
        pystac stackstac planetary-computer \
        whitebox_tools \
        pygis geoai && \
    mamba clean --all -y

# ── Step 4: PyTorch with CUDA (works on CPU too, just no GPU acceleration) ───
RUN mamba run -n pygile pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 && \
    mamba run -n pygile pip install --no-cache-dir pytorch-lightning

# ── Step 5: TensorFlow GPU (works on CPU too if no GPU present) ──────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    "tensorflow[and-cuda]" keras

# ── Step 6: All remaining pip packages ───────────────────────────────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    albumentations timm \
    pythreejs pyvista \
    libpysal esda \
    keplergl \
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

# ── Step 7: pyspatialml (kept separate — known install quirks) ────────────────
RUN mamba run -n pygile pip install --no-cache-dir pyspatialml || \
    mamba run -n pygile pip install --no-cache-dir \
        "git+https://github.com/stevenpawley/Pyspatialml.git" || \
    echo "pyspatialml installation failed - continuing"

# ── Step 8: sklearn-xarray (kept separate — GitHub install) ──────────────────
RUN mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/jgrss/sklearn-xarray.git" || \
    mamba run -n pygile pip install sklearn_xarray || \
    echo "sklearn_xarray installation failed - continuing"

# ── Step 9: Compile GRASS GIS 8.4 from source ────────────────────────────────
# Identical configure flags to original
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

# ── Step 10: Compile SAGA GIS 9.3 from source ────────────────────────────────
# Identical cmake flags to original
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

# ── Step 11: Install OTB 9.1 ─────────────────────────────────────────────────
# Identical to original
RUN cd /tmp && \
    wget -q https://www.orfeo-toolbox.org/packages/OTB-9.1.1-Linux.tar.gz && \
    tar xf OTB-9.1.1-Linux.tar.gz --one-top-level=/opt/otb && \
    rm -f OTB-9.1.1-Linux.tar.gz && \
    sed -i '1 s|^#! */bin/sh|#!/bin/bash|' /opt/otb/bin/otbcli && \
    sed -i 's|\<source\>|.|g' /opt/otb/bin/otbcli && \
    mkdir -p /opt/conda/envs/pygile/etc/conda/activate.d

# ── Step 12: Environment variables ───────────────────────────────────────────
# Identical to original
ENV PATH="/opt/conda/envs/pygile/bin:/opt/grass/bin:/opt/grass/scripts:/opt/saga/bin:/opt/otb/bin:${PATH}"
ENV PYTHONPATH="/opt/otb/lib/python"
ENV LD_LIBRARY_PATH="/opt/conda/envs/pygile/lib:/opt/grass/lib:/opt/saga/lib:/opt/otb/lib:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu"
ENV SAGA_CMD="/opt/saga/bin/saga_cmd"
ENV SAGA_MLB="/opt/saga/lib/saga"
ENV GISBASE="/opt/grass"
ENV OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"

# ── Step 13: Conda activation hooks ──────────────────────────────────────────
# Identical to original
RUN printf '#!/bin/bash\nexport PYTHONPATH="/opt/grass/grass84/etc/python${PYTHONPATH:+:$PYTHONPATH}"\n' \
        > /opt/conda/envs/pygile/etc/conda/activate.d/grass.sh && \
    chmod +x /opt/conda/envs/pygile/etc/conda/activate.d/grass.sh && \
    printf '#!/bin/bash\nif [ -f /opt/otb/otbenv.profile ]; then\n  . /opt/otb/otbenv.profile\nfi\nexport OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"\nexport PYTHONPATH="/opt/otb/lib/python${PYTHONPATH:+:$PYTHONPATH}"\n' \
        > /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh && \
    chmod +x /opt/conda/envs/pygile/etc/conda/activate.d/otb.sh

# ── Step 14: Verify core packages ────────────────────────────────────────────
RUN mamba run -n pygile python -c \
    "import numpy, pandas, geopandas, rasterio, matplotlib; print('Core packages verification: OK')" || \
    echo "Core package verification failed"

# ── Step 15: Workspace structure ─────────────────────────────────────────────
WORKDIR /workspace
RUN mkdir -p /workspace/{data,output,scripts,notebooks,samples}

# ── Step 16: Startup script ───────────────────────────────────────────────────
# Identical to original
RUN printf '#!/bin/bash\n\
source /opt/conda/etc/profile.d/conda.sh\n\
conda activate pygile\n\
cd /workspace\n\
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \\\n\
  --ServerApp.token="" --ServerApp.password="" \\\n\
  --ServerApp.allow_origin="*" --ServerApp.disable_check_xsrf=True\n' \
    > /start.sh && chmod +x /start.sh

# ── Final cleanup (safe: cache only, no packages removed) ────────────────────
RUN mamba clean --all -y && \
    find /opt/conda -name "*.pyc" -delete && \
    find /opt/conda -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

EXPOSE 8888
CMD ["/start.sh"]