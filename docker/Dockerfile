# syntax=docker/dockerfile:1.7
FROM condaforge/mambaforge:24.9.0-0

LABEL name="PyGILE-Plus"
LABEL description="Optimized headless geospatial research environment with SAGA 9.x + GRASS (conda) + OTB 9.1 + modern ML stack + 3D visualization"
LABEL maintainer="research-team"

ARG PYTHON_VERSION=3.11
ARG DEBIAN_FRONTEND=noninteractive
ARG GDAL_GRASS_VERSION=2.0.0

ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        software-properties-common ca-certificates curl gnupg && \
    curl -fsSL https://repos.codelite.org/CodeLite.asc \
        | gpg --dearmor -o /usr/share/keyrings/codelite.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/codelite.gpg] https://repos.codelite.org/wx3.2/ubuntu/ focal universe" \
        > /etc/apt/sources.list.d/codelite.list && \
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
        libgdal-dev gdal-bin libproj-dev proj-bin \
        libwxbase3.2-0-unofficial libwxbase3.2unofficial-dev \
        libwxgtk3.2-0-unofficial libwxgtk3.2unofficial-dev \
        wx3.2-headers wx-common \
        libgtk-3-dev \
        nodejs npm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mamba create -n pygile python=${PYTHON_VERSION} -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

RUN mamba install -n pygile -c conda-forge -y \
    numpy && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    grass gdal proj geos libspatialindex boost-cpp && \
    mamba clean --all -y

RUN test -d /opt/conda/envs/pygile/grass84/etc/python \
      || { echo "GISBASE is not grass84; update PYTHONPATH and GDAL-GRASS paths" >&2; exit 1; } && \
    test -f /opt/conda/envs/pygile/grass84/include/grass/gis.h \
      || { echo "GRASS development headers absent" >&2; exit 1; } && \
    test -f /opt/conda/envs/pygile/grass84/lib/libgrass_gis.so \
      || { echo "GRASS shared libraries absent" >&2; exit 1; } && \
    test -x /opt/conda/envs/pygile/bin/gdal-config \
      || { echo "conda gdal-config absent" >&2; exit 1; }

RUN mamba install -n pygile -c conda-forge -y \
    fiona shapely pyproj && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    pandas scipy matplotlib seaborn scikit-learn && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    geopandas rasterio && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    xarray netcdf4 h5py h5netcdf zarr && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    jupyter jupyterlab ipywidgets && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    plotly bokeh folium contextily mapclassify && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    holoviews hvplot && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    osmnx earthpy geoplot && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    rasterstats xarray-spatial && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    scikit-image tifffile imageio-ffmpeg && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    opencv && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    localtileserver rio-cogeo rioxarray && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    ipyleaflet owslib && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    geemap leafmap && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    census us pykrige palettable geojson && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    pystac stackstac planetary-computer && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    whitebox_tools && \
    mamba clean --all -y

RUN mamba install -n pygile -c conda-forge -y \
    pygis geoai && \
    mamba clean --all -y

RUN mamba run -n pygile pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124 && \
    mamba run -n pygile pip install --no-cache-dir pytorch-lightning

RUN mamba run -n pygile pip install --no-cache-dir \
    "tensorflow[and-cuda]" keras

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

RUN mamba run -n pygile pip install --no-cache-dir pyspatialml || \
    mamba run -n pygile pip install --no-cache-dir \
        "git+https://github.com/stevenpawley/Pyspatialml.git" || \
    echo "pyspatialml installation failed - continuing"

RUN mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/jgrss/sklearn-xarray.git" || \
    mamba run -n pygile pip install sklearn_xarray || \
    echo "sklearn_xarray installation failed - continuing"

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

RUN cd /tmp && \
    wget -q https://www.orfeo-toolbox.org/packages/OTB-9.1.1-Linux.tar.gz && \
    tar xf OTB-9.1.1-Linux.tar.gz --one-top-level=/opt/otb && \
    rm -f OTB-9.1.1-Linux.tar.gz && \
    sed -i '1 s|^#! */bin/sh|#!/bin/bash|' /opt/otb/bin/otbcli && \
    sed -i 's|\<source\>|.|g' /opt/otb/bin/otbcli && \
    grep -q 'otbenv.profile' /opt/otb/bin/otbcli \
      || { echo "otbcli no longer self-sources otbenv.profile" >&2; exit 1; }

ENV PATH="/opt/conda/envs/pygile/bin:/opt/saga/bin:/opt/otb/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/conda/envs/pygile/lib:/opt/saga/lib:/opt/otb/lib:/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu"
ENV SAGA_CMD="/opt/saga/bin/saga_cmd"
ENV SAGA_MLB="/opt/saga/lib/saga"
ENV OTB_APPLICATION_PATH="/opt/otb/lib/otb/applications"
ENV PYTHONPATH="/opt/conda/envs/pygile/grass84/etc/python:/opt/otb/lib/otb/python"
ENV GDAL_DATA="/opt/conda/envs/pygile/share/gdal"
ENV PROJ_DATA="/opt/conda/envs/pygile/share/proj"
ENV PROJ_LIB="/opt/conda/envs/pygile/share/proj"
ENV GDAL_DRIVER_PATH="/opt/conda/envs/pygile/lib/gdalplugins"

RUN echo "/opt/conda/envs/pygile/grass84/lib" > /etc/ld.so.conf.d/grass.conf && \
    ldconfig && \
    cd /tmp && \
    git clone --depth 1 --branch ${GDAL_GRASS_VERSION} https://github.com/OSGeo/gdal-grass.git && \
    cd gdal-grass && mkdir build && cd build && \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_PREFIX_PATH=/opt/conda/envs/pygile \
        -DAUTOLOAD_DIR=/opt/conda/envs/pygile/lib/gdalplugins \
        -DGDAL_CONFIG_PREFER_PATH=/opt/conda/envs/pygile/bin \
        -DGRASS_BIN_PREFER_PATH=/opt/conda/envs/pygile/bin && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    cd / && rm -rf /tmp/gdal-grass && \
    test -f /opt/conda/envs/pygile/lib/gdalplugins/gdal_GRASS.so \
      || { echo "gdal_GRASS.so not installed" >&2; exit 1; } && \
    test -f /opt/conda/envs/pygile/lib/gdalplugins/ogr_GRASS.so \
      || { echo "ogr_GRASS.so not installed" >&2; exit 1; }

COPY <<'PYVERIFY' /usr/local/lib/pygile_verify.py
from osgeo import gdal, ogr

assert gdal.__version__.startswith("3.12"), "GDAL version is " + gdal.__version__
assert "/opt/otb/" not in gdal.__file__, "osgeo resolved from OTB: " + gdal.__file__
assert gdal.GetDriverByName("GRASS") is not None, "GDAL GRASS driver absent"
assert ogr.GetDriverByName("GRASS") is not None, "OGR GRASS driver absent"

import numpy, pandas, matplotlib, fiona, rasterio, geopandas
import grass.script

print("GDAL " + gdal.__version__ + " from " + gdal.__file__)
print("GRASS raster and vector drivers registered")
PYVERIFY

COPY <<'SHVERIFY' /usr/local/bin/pygile-verify
#!/bin/bash
set -eo pipefail
source /opt/conda/etc/profile.d/conda.sh
conda activate pygile

python /usr/local/lib/pygile_verify.py

gdalinfo_path="$(command -v gdalinfo)"
if [ "$gdalinfo_path" != "/opt/conda/envs/pygile/bin/gdalinfo" ]; then
  echo "FAIL: gdalinfo resolves to $gdalinfo_path" >&2
  exit 1
fi

if [ "${GDAL_DRIVER_PATH:-}" = "disable" ]; then
  echo "FAIL: GDAL_DRIVER_PATH is disable" >&2
  exit 1
fi

if [ "${PROJ_LIB:-}" != "${PROJ_DATA:-}" ]; then
  echo "FAIL: PROJ_LIB and PROJ_DATA disagree" >&2
  exit 1
fi

otb_output="$(otbcli_BandMath -help 2>&1 || true)"
case "$otb_output" in
  *"error while loading shared libraries"*|*"command not found"*)
    echo "FAIL: otbcli_BandMath: $otb_output" >&2
    exit 1
    ;;
esac
if [ -z "$otb_output" ]; then
  echo "FAIL: otbcli_BandMath produced no output" >&2
  exit 1
fi

python -c "import otbApplication" >/dev/null 2>&1 \
  || echo "WARN: import otbApplication unavailable (OTB 9.1 bindings built for Python 3.8)"

echo "ALL REQUIRED CHECKS PASSED"
SHVERIFY

RUN chmod +x /usr/local/bin/pygile-verify

WORKDIR /workspace
RUN mkdir -p /workspace/{data,output,scripts,notebooks,samples}

RUN printf '#!/bin/bash\n\
source /opt/conda/etc/profile.d/conda.sh\n\
conda activate pygile\n\
cd /workspace\n\
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root \\\n\
  --ServerApp.token="" --ServerApp.password="" \\\n\
  --ServerApp.allow_origin="*" --ServerApp.disable_check_xsrf=True\n' \
    > /start.sh && chmod +x /start.sh

RUN mamba clean --all -y && \
    find /opt/conda -name "*.pyc" -delete && \
    find /opt/conda -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

RUN /usr/local/bin/pygile-verify

EXPOSE 8888
CMD ["/start.sh"]