"""Download two small Sentinel-2 images of the Melamchi valley for Part D.

The Melamchi flood of 15 June 2021 buried the river bed and parts of Melamchi
Bazar under debris. This script saves one cloud-free image from before the flood
(October to December 2020) and one from after it (October to December 2021).
The same season in both years keeps vegetation and snow comparable.

It uses Microsoft Planetary Computer, which needs no account.

Run it once, inside the PyGILE-Plus container or the pygile environment,
from this folder:

    python get_sentinel2_melamchi.py

If a library is missing, the script tells you what to install.

Output (in this folder, about 10 to 15 MB in total):
    s2_melamchi_before.tif    10 bands, UTM 45N, 20 m cells, uint16
    s2_melamchi_after.tif     the same grid, after the flood
    s2_melamchi_scenes.csv    which scenes were used, with dates and cloud cover

Copernicus Sentinel-2 data are free to use and share. The required credit:
"Contains modified Copernicus Sentinel data 2020-2021, processed by ESA."
"""
import sys
from pathlib import Path

missing = []
for module, package in [("pystac_client", "pystac-client"),
                        ("planetary_computer", "planetary-computer"),
                        ("odc.stac", "odc-stac"),
                        ("rioxarray", "rioxarray")]:
    try:
        __import__(module)
    except ImportError:
        missing.append(package)
if missing:
    sys.exit("Missing libraries. Install them first, then run this script again:\n\n"
             f"    pip install {' '.join(missing)}\n")

import numpy as np
import pandas as pd
import planetary_computer
import pystac_client
import rioxarray  # noqa: F401  (adds the .rio methods)
from odc.stac import load

try:
    HERE = Path(__file__).resolve().parent     # run as a script
except NameError:
    HERE = Path.cwd()                          # pasted into a notebook: the notebook's folder

# Melamchi river from Melamchi Bazar up to Helambu, inside the Part C DEM area.
BBOX = (85.48, 27.80, 85.62, 27.98)          # west, south, east, north (degrees)
CRS = "EPSG:32645"                            # UTM 45N, as in the rest of the course
RES = 20                                      # metres
PERIODS = {"before": "2020-10-01/2020-12-31",
           "after": "2021-10-01/2021-12-31"}
# Both periods end before 25 January 2022, when ESA added a +1000 offset to the
# reflectance values. Keeping inside them means no correction is needed.

# Blue, green, red, three red-edge bands, near-infrared (B08 and narrow B8A), two short-wave infrared
BANDS = ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B11", "B12"]
# Scene classification codes that mean "not clear ground" (no data, saturated,
# cloud shadow, cloud medium/high probability, thin cirrus)
BAD_SCL = [0, 1, 3, 8, 9, 10]

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

rows = []
for label, dates in PERIODS.items():
    items = list(catalog.search(collections=["sentinel-2-l2a"], bbox=BBOX, datetime=dates,
                                query={"eo:cloud_cover": {"lt": 30}}).items())
    if not items:
        sys.exit(f"No scenes found for {label} ({dates}). Try raising the cloud limit.")
    print(f"{label}: {len(items)} candidate scenes")

    # A scene's cloud cover is for the whole 110 km tile. What matters is the cloud
    # inside our small box, so load just the classification band, coarsely, per day.
    scl = load(items, bands=["SCL"], bbox=BBOX, crs=CRS, resolution=100,
               groupby="solar_day", chunks={})
    scl = scl["SCL"].compute()
    bad = scl.isin(BAD_SCL).mean(dim=["x", "y"]).to_pandas()
    best_day = bad.idxmin()
    print(f"  clearest day: {best_day:%Y-%m-%d}, {bad.min() * 100:.1f}% of the box not clear")

    day_items = [it for it in items if it.datetime.strftime("%Y-%m-%d") == f"{best_day:%Y-%m-%d}"]
    ds = load(day_items, bands=BANDS, bbox=BBOX, crs=CRS, resolution=RES,
              groupby="solar_day", resampling="bilinear", chunks={})
    img = ds.to_array("band").isel(time=0).compute()
    img = img.where(img > 0, 0).astype("uint16")          # 0 = no data
    img = img.rio.write_crs(CRS).rio.write_nodata(0)
    img.attrs["long_name"] = tuple(BANDS)
    img.attrs["scale_factor"] = 0.0001                    # value x 0.0001 = reflectance
    img.attrs["credit"] = "Contains modified Copernicus Sentinel data 2020-2021, processed by ESA"

    out = HERE / f"s2_melamchi_{label}.tif"
    img.rio.to_raster(out, compress="deflate", predictor=2, tiled=True)
    print(f"  saved {out.name}: {img.shape[1]} rows x {img.shape[2]} columns, "
          f"{out.stat().st_size / 1e6:.1f} MB")

    for it in day_items:
        rows.append({"image": label, "date": f"{best_day:%Y-%m-%d}", "scene_id": it.id,
                     "tile_cloud_cover_pct": it.properties.get("eo:cloud_cover"),
                     "box_not_clear_pct": round(float(bad.min()) * 100, 1)})

pd.DataFrame(rows).to_csv(HERE / "s2_melamchi_scenes.csv", index=False)
print("\nDone. Please send me the three s2_melamchi_* files.")
