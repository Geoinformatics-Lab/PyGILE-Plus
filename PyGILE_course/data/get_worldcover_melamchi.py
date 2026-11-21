"""Download the ESA WorldCover 2021 land-cover map of the Melamchi valley for Part D.

WorldCover is a global 10 m land-cover map made by ESA from Sentinel-1 and
Sentinel-2. Lesson D4 uses it as reference labels to train and test a
land-cover classifier on the Sentinel-2 image.

It uses Microsoft Planetary Computer, which needs no account. Run it once,
after get_sentinel2_melamchi.py, in this folder (as a script or pasted into a
notebook):

    python get_worldcover_melamchi.py

Output: worldcover_melamchi_2021.tif, on exactly the same 20 m grid as
s2_melamchi_after.tif (uint8, class codes 10 to 100, 0 = no data).

Licence: CC BY 4.0. Credit: "© ESA WorldCover project 2021 / Contains modified
Copernicus Sentinel data (2021) processed by ESA WorldCover consortium."
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
    sys.exit(f"Missing libraries. Install them first:\n\n    pip install {' '.join(missing)}\n")

import numpy as np
import planetary_computer
import pystac_client
import rioxarray
from odc.stac import load
from rasterio.enums import Resampling

try:
    HERE = Path(__file__).resolve().parent     # run as a script
except NameError:
    HERE = Path.cwd()                          # pasted into a notebook: the notebook's folder
# If you run this in a notebook somewhere else, set the folder yourself, e.g.:
# HERE = Path("/workspace/PyGILE/PyGILE_course/data")

s2_path = HERE / "s2_melamchi_after.tif"
if not s2_path.exists():
    sys.exit(f"{s2_path} not found. Run get_sentinel2_melamchi.py first, or set HERE.")
s2 = rioxarray.open_rasterio(s2_path).isel(band=0)

BBOX = (85.47, 27.79, 85.63, 27.99)   # a little larger than the image, so no edge is missed

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)
items = [it for it in catalog.search(collections=["esa-worldcover"], bbox=BBOX).items()
         if str(it.properties.get("esa_worldcover:product_version", "")).startswith("2")]
if not items:
    sys.exit("No WorldCover 2021 (version 2) tiles found.")
print(f"{len(items)} WorldCover 2021 tile(s): {[it.id for it in items]}")

# Load on WorldCover's own grid: degrees, 1/12000 degree (about 10 m) cells, no resampling
wc = load(items, bands=["map"], bbox=BBOX, crs="EPSG:4326", resolution=1 / 12000,
          resampling="nearest", chunks={})["map"].isel(time=0).compute()
wc = wc.rio.write_crs("EPSG:4326").rio.write_nodata(0)

# Put it on the Sentinel-2 grid. Class codes are labels, not amounts, so take the
# most common 10 m class inside each 20 m cell ("mode"), never an average.
wc20 = wc.rio.reproject_match(s2, resampling=Resampling.mode).astype("uint8")
wc20 = wc20.rio.write_nodata(0)
wc20.attrs = {"long_name": "ESA WorldCover 2021 class",
              "credit": "© ESA WorldCover project 2021 / Contains modified Copernicus "
                        "Sentinel data (2021) processed by ESA WorldCover consortium"}

out = HERE / "worldcover_melamchi_2021.tif"
wc20.rio.to_raster(out, compress="deflate", tiled=True)
codes, counts = np.unique(wc20.values, return_counts=True)
print(f"saved {out.name}: {wc20.shape[0]} rows x {wc20.shape[1]} columns, "
      f"{out.stat().st_size / 1e6:.2f} MB")
print("class codes and cell counts:", dict(zip(codes.tolist(), counts.tolist())))
print("\nDone. Please send me worldcover_melamchi_2021.tif.")
