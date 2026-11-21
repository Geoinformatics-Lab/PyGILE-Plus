"""Rebuild the course's Nepal vector data from the original sources.

You do not need to run this to follow the course: the files it makes are already
in this folder. It is here so anyone can check, reproduce or update the data.

Sources
- Nepal boundaries: geoJSON-Nepal by Saugat Acharya (MIT licence),
  https://github.com/mesaugat/geoJSON-Nepal . Its attributes (P-codes, dates)
  show it is derived from the OCHA common operational boundaries, produced by
  the Survey Department of Nepal.
- World countries: Natural Earth 1:110m admin 0 countries (public domain): save
  https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip in _raw/

Run from this folder:  python make_data.py
"""
from pathlib import Path
import urllib.request
import zipfile

import geopandas as gpd
import pandas as pd
import shapely

HERE = Path(__file__).resolve().parent
RAW = HERE / "_raw"
RAW.mkdir(exist_ok=True)
BASE = "https://raw.githubusercontent.com/mesaugat/geoJSON-Nepal/master/"

for name in ["nepal-districts-new.geojson", "nepal-district-headquarters.geojson"]:
    target = RAW / name
    if not target.exists():
        urllib.request.urlretrieve(BASE + name, target)

# --- districts: simplify while keeping shared borders identical ----------------
d = gpd.read_file(RAW / "nepal-districts-new.geojson")
d = d.rename(columns={"DIST_EN": "district", "DIST_PCODE": "district_code",
                      "ADM1_PCODE": "province_code"})
d = d[["district", "district_code", "province_code", "geometry"]]
# coverage_simplify simplifies all polygons together, so neighbours still share
# exactly the same border afterwards (no gaps or overlaps). 0.003 degrees is about 300 m.
d["geometry"] = shapely.coverage_simplify(d.geometry.values, tolerance=0.003)
d = d.sort_values("district").reset_index(drop=True)
d.to_file(HERE / "nepal_districts.geojson", driver="GeoJSON")

# --- provinces: dissolved from the same districts, so they match exactly -------
p = d.dissolve(by="province_code", as_index=False)[["province_code", "geometry"]]
p.to_file(HERE / "nepal_provinces.geojson", driver="GeoJSON")

# --- province names (a plain table, joined to the maps in Lesson B6) -----------
names = ["Koshi", "Madhesh", "Bagmati", "Gandaki", "Lumbini", "Karnali", "Sudurpashchim"]
pd.DataFrame({
    "province_code": [f"NP0{i}" for i in range(1, 8)],
    "province_number": list(range(1, 8)),
    "province": names,
}).to_csv(HERE / "province_names.csv", index=False)

# --- district headquarters (75 points: from before Nawalparasi and Rukum were split) --
hq = gpd.read_file(RAW / "nepal-district-headquarters.geojson").rename(columns={"HQ_NAME": "name"})
hq = hq.sort_values("name").reset_index(drop=True)
hq.to_file(HERE / "district_headquarters.geojson", driver="GeoJSON")

# --- world countries (Natural Earth, public domain) -----------------------------
zip_path = RAW / "ne_110m_admin_0_countries.zip"
w = gpd.read_file(f"zip://{zip_path}!ne_110m_admin_0_countries.shp")
w = w[["NAME", "ISO_A3", "CONTINENT", "POP_EST", "geometry"]].rename(
    columns={"NAME": "name", "ISO_A3": "iso_a3", "CONTINENT": "continent", "POP_EST": "pop_est"})
w.to_file(HERE / "world_countries.geojson", driver="GeoJSON")

# --- Part C: clip the Copernicus DEM tile ---------------------------------------
# Download the tile once in a browser and save it in _raw/ :
# https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N27_00_E085_00_DEM/Copernicus_DSM_COG_10_N27_00_E085_00_DEM.tif
tile = RAW / "Copernicus_DSM_COG_10_N27_00_E085_00_DEM.tif"
if tile.exists():
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.open(tile) as src:
        win = from_bounds(85.20, 27.55, 85.80, 28.00, transform=src.transform)
        win = win.round_offsets().round_lengths()
        dem = np.round(src.read(1, window=win)).astype("int16")
        profile = src.profile.copy()
        profile.pop("interleave", None)
        profile.update(dtype="int16", nodata=-32768, width=dem.shape[1], height=dem.shape[0],
                       transform=src.window_transform(win), compress="deflate", predictor=2,
                       tiled=True, blockxsize=256, blockysize=256)
    with rasterio.open(HERE / "dem_kathmandu_melamchi.tif", "w", **profile) as dst:
        dst.write(dem, 1)
else:
    print("DEM tile not found in _raw/: skipping the Part C DEM")

for f in ["nepal_districts.geojson", "nepal_provinces.geojson", "district_headquarters.geojson",
          "world_countries.geojson", "province_names.csv"]:
    print(f"{f}: {(HERE / f).stat().st_size / 1e3:.0f} kB")
