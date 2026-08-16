# syntax=docker/dockerfile:1.7

ARG BASE_IMAGE=condaforge/mambaforge:24.9.0-0
FROM ${BASE_IMAGE}
ARG BASE_IMAGE

LABEL name="PyGILE-Plus"
LABEL version="1.1.1"
LABEL description="Headless geospatial research environment: SAGA, GRASS, WhiteboxTools, OTB, and a Python geospatial and ML stack"
LABEL maintainer="research-team"

ARG DEBIAN_FRONTEND=noninteractive
ARG SAGA_VERSION=9.3.2
ARG OTB_VERSION=9.1.1
ARG GDAL_GRASS_VERSION=2.0.0
ARG SAGA_SHA256=ef8d4ee82eda9b14a738e4e579d1748b39958624fbf6d148e3e10eb6936a3f64
ARG OTB_SHA256=7ae191482c7a1194a90c2b763c457290a335d630856eb7acde58c7c6172f9ad6

ENV PYTHONUNBUFFERED=1
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV DISPLAY=:99
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Fixed thread counts keep floating-point reduction order deterministic.
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV NUMEXPR_NUM_THREADS=1
ENV GDAL_NUM_THREADS=1
ENV PYTHONHASHSEED=0

RUN echo ">>> [01/26] apt packages" && \
    apt-get update && \
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

RUN echo ">>> [02/26] conda environment" && \
    mamba create -n pygile python=3.11.15 -y && \
    mamba run -n pygile conda config --env --add channels conda-forge && \
    mamba run -n pygile conda config --env --set channel_priority strict

RUN echo ">>> [03/26] numpy" && \
    mamba install -n pygile -c conda-forge -y \
    numpy=2.4.6 && \
    mamba clean --all -y

RUN echo ">>> [04/26] grass gdal proj geos" && \
    mamba install -n pygile -c conda-forge -y \
    grass=8.4.2 gdal=3.12.2 proj=9.7.1 geos=3.14.1 \
    libspatialindex=2.1.0 boost-cpp=1.85.0 && \
    mamba clean --all -y

RUN echo ">>> [05/26] check grass layout" && \
    test -d /opt/conda/envs/pygile/grass84/etc/python \
      || { echo "GISBASE is not grass84; update PYTHONPATH and GDAL-GRASS paths" >&2; exit 1; } && \
    test -f /opt/conda/envs/pygile/grass84/include/grass/gis.h \
      || { echo "GRASS development headers absent" >&2; exit 1; } && \
    test -f /opt/conda/envs/pygile/grass84/lib/libgrass_gis.so \
      || { echo "GRASS shared libraries absent" >&2; exit 1; } && \
    test -x /opt/conda/envs/pygile/bin/gdal-config \
      || { echo "conda gdal-config absent" >&2; exit 1; }

RUN echo ">>> [06/26] fiona shapely pyproj" && \
    mamba install -n pygile -c conda-forge -y \
    fiona=1.10.1 shapely=2.1.2 pyproj=3.7.2 && \
    mamba clean --all -y

RUN echo ">>> [07/26] pandas scipy matplotlib seaborn scikit-learn" && \
    mamba install -n pygile -c conda-forge -y \
    pandas=2.3.3 scipy=1.17.1 matplotlib=3.10.9 seaborn=0.13.2 scikit-learn=1.9.0 && \
    mamba clean --all -y

RUN echo ">>> [08/26] geopandas rasterio" && \
    mamba install -n pygile -c conda-forge -y \
    geopandas=1.1.4 rasterio=1.4.4 && \
    mamba clean --all -y

RUN echo ">>> [09/26] xarray netcdf4 h5py zarr" && \
    mamba install -n pygile -c conda-forge -y \
    xarray=2026.7.0 netcdf4=1.7.4 h5py=3.16.0 h5netcdf=1.8.1 zarr=3.1.6 && \
    mamba clean --all -y

RUN echo ">>> [10/26] jupyter jupyterlab ipywidgets" && \
    mamba install -n pygile -c conda-forge -y \
    jupyter=1.1.1 jupyterlab=4.6.2 ipywidgets=8.1.8 && \
    mamba clean --all -y

RUN echo ">>> [11/26] plotly bokeh folium contextily mapclassify" && \
    mamba install -n pygile -c conda-forge -y \
    plotly=6.9.0 bokeh=3.9.2 folium=0.20.0 contextily=1.7.1 mapclassify=2.10.0 && \
    mamba clean --all -y

RUN echo ">>> [12/26] holoviews hvplot" && \
    mamba install -n pygile -c conda-forge -y \
    holoviews=1.23.1 hvplot=0.12.2 && \
    mamba clean --all -y

RUN echo ">>> [13/26] osmnx earthpy geoplot" && \
    mamba install -n pygile -c conda-forge -y \
    osmnx=2.1.1 earthpy=0.9.4 geoplot=0.5.1 && \
    mamba clean --all -y

RUN echo ">>> [14/26] rasterstats xarray-spatial" && \
    mamba install -n pygile -c conda-forge -y \
    rasterstats=0.21.0 xarray-spatial=0.5.3 && \
    mamba clean --all -y

RUN echo ">>> [15/26] scikit-image tifffile imageio-ffmpeg" && \
    mamba install -n pygile -c conda-forge -y \
    scikit-image=0.26.0 tifffile=2026.3.3 imageio-ffmpeg=0.6.0 && \
    mamba clean --all -y

RUN echo ">>> [16/26] opencv" && \
    mamba install -n pygile -c conda-forge -y \
    opencv=4.12.0 && \
    mamba clean --all -y

RUN echo ">>> [17/26] localtileserver rio-cogeo rioxarray" && \
    mamba install -n pygile -c conda-forge -y \
    localtileserver=0.11.0 rio-cogeo=7.0.2 rioxarray=0.19.0 && \
    mamba clean --all -y

RUN echo ">>> [18/26] ipyleaflet owslib" && \
    mamba install -n pygile -c conda-forge -y \
    ipyleaflet=0.20.0 owslib=0.35.0 && \
    mamba clean --all -y

RUN echo ">>> [19/26] geemap leafmap" && \
    mamba install -n pygile -c conda-forge -y \
    geemap=0.37.1 leafmap=0.63.0 && \
    mamba clean --all -y

RUN echo ">>> [20/26] census us pykrige palettable geojson" && \
    mamba install -n pygile -c conda-forge -y \
    census=0.8.27 us=3.2.0 pykrige=1.7.3 palettable=3.3.3 geojson=3.3.0 && \
    mamba clean --all -y

RUN echo ">>> [21/26] pystac stackstac planetary-computer" && \
    mamba install -n pygile -c conda-forge -y \
    pystac=1.14.3 stackstac=0.5.1 planetary-computer=1.0.0 && \
    mamba clean --all -y

RUN echo ">>> [22/26] whitebox_tools" && \
    mamba install -n pygile -c conda-forge -y \
    whitebox_tools=2.4.0 && \
    mamba clean --all -y

RUN echo ">>> [23/26] pygis geoai" && \
    mamba install -n pygile -c conda-forge -y \
    pygis=0.9.5 geoai=0.36.0 && \
    mamba clean --all -y

RUN echo ">>> [24/26] richdem pysheds landlab" && \
    mamba install -n pygile -c conda-forge -y \
    richdem=2.3.0 pysheds=0.5 landlab=2.10.1 && \
    mamba clean --all -y

RUN echo ">>> [25/26] cupy" && \
    mamba install -n pygile -c conda-forge -y \
    cupy=14.1.1 && \
    mamba clean --all -y

RUN echo ">>> [26/26] odc-stac laspy python-pdal" && \
    mamba install -n pygile -c conda-forge -y \
    odc-stac=0.5.3 laspy=2.7.0 python-pdal=3.5.3 && \
    mamba clean --all -y

RUN echo ">>> pip: torch" && \
    mamba run -n pygile pip install --no-cache-dir \
    torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124 && \
    mamba run -n pygile pip install --no-cache-dir pytorch-lightning==2.6.5

RUN echo ">>> pip: tensorflow keras" && \
    mamba run -n pygile pip install --no-cache-dir \
    tensorflow==2.21.0 keras==3.15.1

RUN echo ">>> pip: analysis, docs, tooling" && \
    mamba run -n pygile pip install --no-cache-dir \
    albumentations==2.0.8 timm==1.0.28 \
    pythreejs==2.4.2 pyvista==0.48.4 \
    libpysal==4.14.1 esda==2.9.0 \
    keplergl==0.3.7 \
    earthengine-api==1.7.38 \
    sphinx==9.0.4 sphinx-sitemap==2.9.0 sphinxcontrib-bibtex==2.7.0 \
    sphinx_inline_tabs==2025.12.21.14 pydata-sphinx-theme==0.20.0 \
    sankee==0.3.0 overturemaps==1.0.1 whiteboxgui==2.3.0 \
    jupyter-book==2.1.6 ghp-import==2.1.0 \
    numpy-groupies==0.11.3 sympy==1.13.1 \
    dask-geopandas==0.5.0 \
    cenpy==1.0.1 \
    whitebox==2.3.6 PySAGA-cmd==1.2.6 \
    streamlit-folium==0.27.4 black==26.5.1 flake8==7.3.0

RUN echo ">>> pip: sklearn-xarray topotoolbox" && \
    mamba run -n pygile pip install --no-cache-dir \
    "git+https://github.com/jgrss/sklearn-xarray.git@6384364de6a3176e1701e24da9d660ab48cb3e48" && \
    mamba run -n pygile pip install --no-cache-dir topotoolbox==0.0.12

# fitz shadows PyMuPDF and pathlib shadows the standard library; both arrive
# transitively and break imports.
RUN echo ">>> pip: drop shadowing packages" && \
    mamba run -n pygile pip uninstall -y fitz pathlib || true

RUN echo ">>> build SAGA ${SAGA_VERSION}" && \
    mkdir -p /opt/manifest && \
    cd /tmp && \
    wget -q "https://sourceforge.net/projects/saga-gis/files/SAGA%20-%209/SAGA%20-%20${SAGA_VERSION}/saga-${SAGA_VERSION}.tar.gz" && \
    if [ -n "${SAGA_SHA256}" ]; then \
      echo "${SAGA_SHA256}  saga-${SAGA_VERSION}.tar.gz" | sha256sum -c -; \
      echo "verified" > /opt/manifest/saga_checksum.txt; \
    else \
      echo "WARNING: SAGA tarball checksum not verified" >&2; \
      { echo "UNVERIFIED"; sha256sum "saga-${SAGA_VERSION}.tar.gz"; } > /opt/manifest/saga_checksum.txt; \
    fi && \
    tar -xzf "saga-${SAGA_VERSION}.tar.gz" && \
    cd "saga-${SAGA_VERSION}/saga-gis" && \
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
    make -j"$(nproc)" && \
    make install && \
    ldconfig && \
    cd / && rm -rf "/tmp/saga-${SAGA_VERSION}"*

RUN echo ">>> install OTB ${OTB_VERSION}" && \
    cd /tmp && \
    wget -q "https://www.orfeo-toolbox.org/packages/OTB-${OTB_VERSION}-Linux.tar.gz" && \
    if [ -n "${OTB_SHA256}" ]; then \
      echo "${OTB_SHA256}  OTB-${OTB_VERSION}-Linux.tar.gz" | sha256sum -c -; \
      echo "verified" > /opt/manifest/otb_checksum.txt; \
    else \
      echo "WARNING: OTB tarball checksum not verified" >&2; \
      { echo "UNVERIFIED"; sha256sum "OTB-${OTB_VERSION}-Linux.tar.gz"; } > /opt/manifest/otb_checksum.txt; \
    fi && \
    tar xf "OTB-${OTB_VERSION}-Linux.tar.gz" --one-top-level=/opt/otb && \
    rm -f "OTB-${OTB_VERSION}-Linux.tar.gz" && \
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

RUN echo ">>> build GDAL-GRASS driver" && \
    echo "/opt/conda/envs/pygile/grass84/lib" > /etc/ld.so.conf.d/grass.conf && \
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
    make -j"$(nproc)" && \
    make install && \
    ldconfig && \
    cd / && rm -rf /tmp/gdal-grass && \
    test -f /opt/conda/envs/pygile/lib/gdalplugins/gdal_GRASS.so \
      || { echo "gdal_GRASS.so not installed" >&2; exit 1; } && \
    test -f /opt/conda/envs/pygile/lib/gdalplugins/ogr_GRASS.so \
      || { echo "ogr_GRASS.so not installed" >&2; exit 1; }

RUN echo ">>> write build manifest" && \
    { \
      echo "PyGILE-Plus build manifest"; \
      echo "built_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"; \
      echo "base_image: ${BASE_IMAGE}"; \
      echo "saga_checksum: $(tr '\n' ' ' < /opt/manifest/saga_checksum.txt)"; \
      echo "otb_checksum: $(tr '\n' ' ' < /opt/manifest/otb_checksum.txt)"; \
      echo ""; \
      echo "[engines]"; \
      echo "saga: $(saga_cmd --version 2>&1 | grep -i 'SAGA Version' || true)"; \
      echo "grass: $(grass --version 2>&1 | head -1)"; \
      echo "whitebox_tools: $(whitebox_tools --version 2>&1 | head -1)"; \
      echo "gdal: $(gdalinfo --version)"; \
      echo "otb: $(otbcli_Smoothing -version 2>&1 | tail -1)"; \
      echo ""; \
      echo "[compiler]"; \
      gcc --version | head -1; \
      cmake --version | head -1; \
      echo ""; \
      echo "[saga gdal linkage]"; \
      ldd /opt/saga/lib/saga/libio_gdal.so 2>/dev/null | grep -i -E 'gdal|proj' \
        || echo "libio_gdal.so not found"; \
    } > /opt/manifest/build_manifest.txt && \
    mamba run -n pygile conda list -n pygile --explicit > /opt/manifest/conda_explicit.txt && \
    mamba run -n pygile pip freeze > /opt/manifest/pip_freeze.txt && \
    cat /opt/manifest/build_manifest.txt

COPY <<'PYVERIFY' /usr/local/lib/pygile_verify.py
import importlib.metadata as md

from osgeo import gdal, ogr

assert gdal.__version__.startswith("3.12"), "GDAL version is " + gdal.__version__
assert "/opt/otb/" not in gdal.__file__, "osgeo resolved from OTB: " + gdal.__file__
assert gdal.GetDriverByName("GRASS") is not None, "GDAL GRASS driver absent"
assert ogr.GetDriverByName("GRASS") is not None, "OGR GRASS driver absent"

import numpy, pandas, matplotlib, fiona, rasterio, geopandas, xrspatial
import grass.script
import richdem, pysheds, landlab, laspy, pdal, odc.stac

try:
    import topotoolbox
except ImportError:
    print("NOTE: topotoolbox unavailable")

try:
    import cupy
    print("cupy " + cupy.__version__)
except ImportError:
    print("NOTE: cupy unavailable")

for pkg, want in [("numpy", "2."), ("geopandas", "1."), ("rasterio", "1.4")]:
    got = md.version(pkg)
    assert got.startswith(want), f"{pkg} is {got}, expected {want}x"

for bad in ("fitz", "pathlib"):
    try:
        md.version(bad)
        raise AssertionError(f"{bad} is installed and shadows a real module")
    except md.PackageNotFoundError:
        pass

print("GDAL " + gdal.__version__ + " from " + gdal.__file__)
print("geopandas " + md.version("geopandas") + ", numpy " + numpy.__version__)
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

# saga_cmd exits 134 on teardown even when output is correct, so match on
# stdout rather than exit status.
saga_ver="$(saga_cmd --version 2>&1 || true)"
case "$saga_ver" in
  *"SAGA Version: 9.3.2"*) ;;
  *) echo "FAIL: SAGA 9.3.2 not reported" >&2; exit 1 ;;
esac

grass_ver="$(grass --version 2>&1 || true)"
case "$grass_ver" in
  *"GRASS GIS 8.4"*) ;;
  *) echo "FAIL: GRASS 8.4 not reported" >&2; exit 1 ;;
esac

wbt_ver="$(whitebox_tools --version 2>&1 || true)"
case "$wbt_ver" in
  *"v2.4.0"*) ;;
  *) echo "FAIL: WhiteboxTools 2.4.0 not reported" >&2; exit 1 ;;
esac

for t in ta_morphometry ta_hydrology ta_preprocessor ta_channels; do
  lib_out="$(saga_cmd "$t" 2>&1 || true)"
  case "$lib_out" in
    *"[0]"*) ;;
    *) echo "FAIL: SAGA library $t unavailable" >&2; exit 1 ;;
  esac
done

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
  || echo "NOTE: otbApplication unavailable (OTB 9.1 bindings target Python 3.8)"

echo "ALL REQUIRED CHECKS PASSED"
SHVERIFY

RUN chmod +x /usr/local/bin/pygile-verify

WORKDIR /workspace
RUN mkdir -p /workspace/data /workspace/output /workspace/scripts \
             /workspace/notebooks /workspace/samples

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
