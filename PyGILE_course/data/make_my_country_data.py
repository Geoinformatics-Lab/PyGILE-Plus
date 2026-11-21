"""Make the course's country data for YOUR country, with the same file names and columns.

The lessons read their data from this folder by file name. If you replace a file
with one that has the same name and the same columns, the lesson code runs on your
data. This script makes those replacements from free open sources that cover the
whole world. The full guide is ../YOUR_OWN_DATA.md.

What it makes (each part is independent; run the ones you want):

  boundaries   nepal_districts.geojson, nepal_provinces.geojson, province_names.csv,
               district_headquarters.geojson                       geoBoundaries
  dem          dem_kathmandu_melamchi.tif                          Copernicus DEM GLO-30
  landslides   landslides_nepal.csv                                NASA Global Landslide Catalog
  rainfall     rainfall_monthly_2025.csv                           Open-Meteo (ERA5)
  gauges       rain_gauges_monsoon_2024.csv                        Open-Meteo (ERA5)

The file names stay the same (even "nepal_..."), so no lesson has to change its paths.
Before a course file is replaced for the first time, the original is copied to
_nepal_original/ , so you can always put Nepal back.

How to use it:
  1. Change the settings below.
  2. Run it from this folder, in the pygile environment:
        python make_my_country_data.py                  # every part
        python make_my_country_data.py boundaries dem   # only these parts
     Run "boundaries" first: the other parts use your new districts.

It needs the internet, except "dem" and "landslides", which read files you download
once in a browser (the script tells you which).
"""
import json
import math
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

# ==============================================================================
# SETTINGS: change these for your country
# ==============================================================================

ISO = "LKA"                # your country's 3-letter code, e.g. IND, BGD, PAK, LKA, KEN
CODE_PREFIX = "LK"         # 2 letters for the unit codes, like "NP" in NP01 and NP0769
UNITS = "ADM2"             # the units that take the place of Nepal's 77 districts
GROUPS = "ADM1"            # the units that take the place of Nepal's 7 provinces
                           # (geoBoundaries levels: ADM1 = states or provinces,
                           #  ADM2 = districts, ADM3 = smaller units)

# Part C study area: a box with some relief, like the Kathmandu-Melamchi box
# (85.2, 27.55, 85.8, 28.0). West, south, east, north, in degrees. It must lie inside
# one 1° x 1° Copernicus tile, so no whole number may fall between west and east,
# or between south and north.
DEM_BOX = (80.55, 6.80, 80.95, 7.15)

# NASA Global Landslide Catalog: your country's name exactly as the catalog writes it
GLC_COUNTRY = "Sri Lanka"
GLC_ACCURACY = ["exact", "1km", "5km"]   # add "10km", "25km" to keep more records
GLC_NEED_FATALITIES = True               # False keeps records without a death count

# Monthly rainfall (Part A): up to about six places from dry to wet, low to high.
# name: (latitude, longitude)
RAIN_PLACES = {
    "Colombo": (6.93, 79.85),
    "Kandy": (7.29, 80.63),
    "Nuwara Eliya": (6.97, 80.78),
    "Jaffna": (9.66, 80.01),
    "Hambantota": (6.12, 81.12),
    "Trincomalee": (8.59, 81.21),
}
RAIN_YEAR = 2025

# Rain "gauges" for interpolation (Lesson C8): random points inside your country,
# with the rain total of one season. Nepal uses the monsoon, June to September.
GAUGE_COUNT = 100
GAUGE_SEASON = ("2024-06-01", "2024-09-30")
GAUGE_SEED = 42

# ==============================================================================

HERE = Path(__file__).resolve().parent
RAW = HERE / "_raw"                     # files you download by hand go here
BACKUP = HERE / "_nepal_original"
OPEN_METEO = "https://archive-api.open-meteo.com/v1/archive?"


def get_json(url):
    """Download and read a JSON answer from a web service."""
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def save(gdf_or_df, name, **kwargs):
    """Save a course file, after keeping the Nepal original once."""
    BACKUP.mkdir(exist_ok=True)
    if (HERE / name).exists() and not (BACKUP / name).exists():
        shutil.copy2(HERE / name, BACKUP / name)
    if name.endswith(".csv"):
        gdf_or_df.to_csv(HERE / name, index=False, encoding="utf-8")
    else:
        gdf_or_df.to_file(HERE / name, driver="GeoJSON", **kwargs)
    print(f"  saved {name}")


def geoboundaries(level):
    """One level of your country's boundaries from geoBoundaries (gbOpen)."""
    meta = get_json(f"https://www.geoboundaries.org/api/current/gbOpen/{ISO}/{level}/")
    units = gpd.read_file(meta["simplifiedGeometryGeoJSON"]).to_crs("EPSG:4326")
    print(f"  {level}: {len(units)} units. Source: {meta['boundarySource']} "
          f"· Licence: {meta['boundaryLicense']}")
    return units


# ------------------------------------------------------------------------------
# boundaries
# ------------------------------------------------------------------------------
def make_boundaries(units, groups):
    """Course-shaped districts, provinces, names and 'headquarters' from two levels."""
    groups = groups.sort_values("shapeName").reset_index(drop=True)
    groups["province_code"] = [f"{CODE_PREFIX}{i:02d}" for i in range(1, len(groups) + 1)]

    # each unit belongs to the group that holds a point inside it
    units = units[["shapeName", "geometry"]].rename(columns={"shapeName": "district"})
    points = units.copy()
    points["geometry"] = units.geometry.representative_point()
    joined = gpd.sjoin(points, groups[["province_code", "geometry"]], predicate="within", how="left")
    joined = joined[~joined.index.duplicated()]
    missing = joined["province_code"].isna()
    if missing.any():                    # a point on a border or a coast: take the nearest group
        utm = groups.estimate_utm_crs()
        nearest = gpd.sjoin_nearest(points[missing].to_crs(utm),
                                    groups[["province_code", "geometry"]].to_crs(utm), how="left")
        joined.loc[missing, "province_code"] = nearest.loc[~nearest.index.duplicated(), "province_code"]
    units["province_code"] = joined["province_code"]

    units = units.sort_values(["province_code", "district"]).reset_index(drop=True)
    units["district_code"] = (units["province_code"]
                              + (units.groupby("province_code").cumcount() + 1).map("{:02d}".format))
    districts = units[["district", "district_code", "province_code", "geometry"]]
    districts = districts.sort_values("district").reset_index(drop=True)

    # provinces made by dissolving the districts, as for Nepal, so the borders match
    provinces = districts.dissolve("province_code").reset_index()[["province_code", "geometry"]]
    names = pd.DataFrame({"province_code": groups["province_code"],
                          "province_number": range(1, len(groups) + 1),
                          "province": groups["shapeName"]})
    hq = gpd.GeoDataFrame({"name": districts["district"]},
                          geometry=districts.geometry.representative_point(), crs="EPSG:4326")
    return districts, provinces, names, hq


def boundaries():
    districts, provinces, names, hq = make_boundaries(geoboundaries(UNITS), geoboundaries(GROUPS))
    save(districts, "nepal_districts.geojson")
    save(provinces, "nepal_provinces.geojson")
    save(names, "province_names.csv")
    save(hq, "district_headquarters.geojson")
    print("\n  Your province codes (use them where the lessons type Nepal's, such as \"NP03\"):")
    print(names.to_string(index=False))
    print("  Note: district_headquarters.geojson holds a point inside each district, not the "
          "real headquarters town. Replace it with real towns if you have them (column 'name').")


def districts_and_provinces():
    """Your districts with their province names, for adding district and province to points."""
    d = gpd.read_file(HERE / "nepal_districts.geojson")
    names = pd.read_csv(HERE / "province_names.csv")
    return d.merge(names[["province_code", "province"]], on="province_code")


def add_district(df, lat="lat", lon="lon", how="left"):
    points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon], df[lat]), crs="EPSG:4326")
    joined = gpd.sjoin(points, districts_and_provinces()[["district", "province", "geometry"]],
                       predicate="within", how=how)
    return pd.DataFrame(joined[~joined.index.duplicated()].drop(columns=["geometry", "index_right"]))


# ------------------------------------------------------------------------------
# dem
# ------------------------------------------------------------------------------
def copernicus_tile(south, west):
    """Name of the Copernicus DEM GLO-30 tile whose south-west corner is (south, west)."""
    ns = f"N{south:02d}" if south >= 0 else f"S{-south:02d}"
    ew = f"E{west:03d}" if west >= 0 else f"W{-west:03d}"
    return f"Copernicus_DSM_COG_10_{ns}_00_{ew}_00_DEM"


def dem():
    import rasterio
    from rasterio.windows import from_bounds

    west, south, east, north = DEM_BOX
    s, w = math.floor(south), math.floor(west)
    if math.floor(north - 1e-9) != s or math.floor(east - 1e-9) != w:
        raise SystemExit("  DEM_BOX crosses a whole degree: move it inside one 1° x 1° tile.")
    name = copernicus_tile(s, w)
    tile = RAW / f"{name}.tif"
    if not tile.exists():
        RAW.mkdir(exist_ok=True)
        print(f"  Download this tile in a browser and save it in {RAW}:\n"
              f"  https://copernicus-dem-30m.s3.amazonaws.com/{name}/{name}.tif\n"
              "  Then run this part again. (No tile means the box is all sea.)")
        return
    with rasterio.open(tile) as src:
        win = from_bounds(west, south, east, north, transform=src.transform)
        win = win.round_offsets().round_lengths()
        data = np.round(src.read(1, window=win)).astype("int16")
        profile = src.profile.copy()
        profile.pop("interleave", None)
        profile.update(dtype="int16", nodata=-32768, width=data.shape[1], height=data.shape[0],
                       transform=src.window_transform(win), compress="deflate", predictor=2,
                       tiled=True, blockxsize=256, blockysize=256)
    BACKUP.mkdir(exist_ok=True)
    out = HERE / "dem_kathmandu_melamchi.tif"
    if out.exists() and not (BACKUP / out.name).exists():
        shutil.copy2(out, BACKUP / out.name)
    with rasterio.open(out, "w", **profile) as dst:
        dst.write(data, 1)
    print(f"  saved {out.name}: {data.shape[1]} x {data.shape[0]} cells, "
          f"{data.min()} to {data.max()} m")


# ------------------------------------------------------------------------------
# landslides
# ------------------------------------------------------------------------------
def landslides():
    path = HERE / "_raw_observed" / "Global_Landslide_Catalog_Export_rows.csv"
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        print(f"  Download the NASA Global Landslide Catalog in a browser and save it as\n  {path}\n"
              "  https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/"
              "Global_Landslide_Catalog_Export_rows.csv")
        return
    glc = pd.read_csv(path)
    keep = ((glc["country_name"] == GLC_COUNTRY)
            & (glc["event_import_source"] == "glc")
            & glc["location_accuracy"].isin(GLC_ACCURACY))
    if GLC_NEED_FATALITIES:
        keep &= glc["fatality_count"].notna()
    glc = glc[keep].copy()
    if glc.empty:
        raise SystemExit(f"  No records for '{GLC_COUNTRY}'. Check the spelling against the "
                         "catalog's column 'country_name', or loosen the GLC_ settings.")
    glc["date"] = pd.to_datetime(glc["event_date"], format="%m/%d/%Y %I:%M:%S %p").dt.strftime("%Y-%m-%d")
    glc["lat"], glc["lon"] = glc["latitude"].round(4), glc["longitude"].round(4)
    joined = add_district(glc, how="inner")
    out = pd.DataFrame({
        "id": joined["event_id"].astype(int), "date": joined["date"],
        "district": joined["district"], "province": joined["province"],
        "lat": joined["lat"], "lon": joined["lon"],
        "fatalities": joined["fatality_count"].fillna(0).astype(int),
        "size": joined["landslide_size"], "trigger": joined["landslide_trigger"],
    }).sort_values(["date", "id"])
    save(out, "landslides_nepal.csv")
    print(f"  {len(out)} landslides, {out['date'].min()} to {out['date'].max()}"
          + ("  (few records: try adding '10km' to GLC_ACCURACY)" if len(out) < 40 else ""))


# ------------------------------------------------------------------------------
# rainfall and gauges (Open-Meteo, ERA5 reanalysis)
# ------------------------------------------------------------------------------
def open_meteo_daily(lat, lon, start, end):
    """Daily rain at one place from Open-Meteo. Returns (DataFrame, elevation in m)."""
    params = {"latitude": lat, "longitude": lon, "start_date": start, "end_date": end,
              "daily": "precipitation_sum", "timezone": "auto", "models": "era5"}
    try:
        data = get_json(OPEN_METEO + urllib.parse.urlencode(params))
    except urllib.error.HTTPError:           # if "models" is refused, use the default model
        params.pop("models")
        data = get_json(OPEN_METEO + urllib.parse.urlencode(params))
    daily = pd.DataFrame({"date": pd.to_datetime(data["daily"]["time"]),
                          "rain_mm": data["daily"]["precipitation_sum"]})
    return daily, data["elevation"]


MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def rainfall():
    rows = []
    for name, (lat, lon) in RAIN_PLACES.items():
        daily, elev = open_meteo_daily(lat, lon, f"{RAIN_YEAR}-01-01", f"{RAIN_YEAR}-12-31")
        monthly = daily.groupby(daily["date"].dt.month)["rain_mm"].sum().reindex(range(1, 13))
        row = {"station": name, "lat": lat, "lon": lon, "elevation_m": int(round(elev))}
        row.update({f"{m}_mm": int(round(v)) for m, v in zip(MONTHS, monthly)})
        rows.append(row)
        time.sleep(1)                        # be polite to a free service
    table = add_district(pd.DataFrame(rows))
    cols = ["station", "district", "province", "elevation_m"] + [f"{m}_mm" for m in MONTHS]
    save(table[cols], "rainfall_monthly_2025.csv")


def gauges():
    country = districts_and_provinces().dissolve()
    rng = np.random.default_rng(GAUGE_SEED)
    w, s, e, n = country.total_bounds
    points = []
    while len(points) < GAUGE_COUNT:         # random points that fall inside the country
        lon, lat = rng.uniform(w, e), rng.uniform(s, n)
        if country.contains(gpd.points_from_xy([lon], [lat])[0]).iloc[0]:
            points.append((round(lat, 4), round(lon, 4)))
    rows = []
    for i, (lat, lon) in enumerate(points, start=1):
        daily, elev = open_meteo_daily(lat, lon, *GAUGE_SEASON)
        rows.append({"station": f"Point {i:03d}", "lat": lat, "lon": lon,
                     "elevation_m": int(round(elev)), "monsoon_mm": round(daily["rain_mm"].sum(), 1)})
        if i % 20 == 0:
            print(f"  {i} of {len(points)} points")
        time.sleep(0.5)
    table = add_district(pd.DataFrame(rows))
    cols = ["station", "district", "province", "lat", "lon", "elevation_m", "monsoon_mm"]
    save(table[cols].sort_values("station"), "rain_gauges_monsoon_2024.csv")
    print("  The column keeps the name 'monsoon_mm'; it holds your season's total.")


PARTS = {"boundaries": boundaries, "dem": dem, "landslides": landslides,
         "rainfall": rainfall, "gauges": gauges}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(PARTS)
    for part in wanted:
        print(f"\n{part}")
        try:
            PARTS[part]()
        except SystemExit as stop:
            print(stop)
        except Exception as error:           # one failing part should not stop the others
            print(f"  {part} failed: {type(error).__name__}: {error}")
    print("\nCredits to keep with your data are in ../YOUR_OWN_DATA.md.")
