"""Download the data for the extra PyGILE lessons (A11, D5 and D6).

Run it once, inside the PyGILE-Plus container or the pygile environment, as a
script from this folder or pasted into a notebook (then set HERE below):

    python get_extra_data.py

It has three independent parts. If one fails, the others still run, and you can
run the script again later: files that already exist are skipped.

1. Daily rainfall 2001-2024 at Melamchi and at Kathmandu (Lesson A11)
   -> rain_daily_melamchi_kathmandu.csv                      (about 0.5 MB)
   Source: Open-Meteo historical weather API, ERA5 reanalysis. No account needed.
   Credit: "Weather data by Open-Meteo.com (CC BY 4.0), from the ERA5 reanalysis
   of the Copernicus Climate Change Service."

2. OpenStreetMap roads, rivers and places of the Melamchi valley (Lesson D5)
   -> osm_melamchi_roads.graphml, osm_melamchi.gpkg          (a few MB)
   Source: OpenStreetMap through the Overpass API (osmnx). No account needed.
   Credit: "© OpenStreetMap contributors, available under the ODbL."

3. A Sentinel-2 time series of the Melamchi valley, 2019-2023, at 100 m (Lesson D6)
   -> s2_melamchi_timeseries_100m.nc                         (about 13 MB)
   Source: Microsoft Planetary Computer. No account needed.
   Credit: "Contains modified Copernicus Sentinel data 2019-2023, processed by ESA."

When it finishes, please send the four files it lists at the end.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    HERE = Path(__file__).resolve().parent     # run as a script
except NameError:
    HERE = Path.cwd()                          # pasted into a notebook: the notebook's folder
# In a notebook somewhere else, set the folder yourself, for example:
# HERE = Path("/workspace/PyGILE/PyGILE_course/data")

# The Sentinel-2 box of Part D (west, south, east, north), in degrees
BBOX = (85.48, 27.80, 85.62, 27.98)
results = {}


def need(*modules):
    """Return the pip names of any missing modules."""
    pip_names = {"pystac_client": "pystac-client", "planetary_computer": "planetary-computer",
                 "odc.stac": "odc-stac"}
    missing = []
    for m in modules:
        try:
            __import__(m)
        except ImportError:
            missing.append(pip_names.get(m, m))
    return missing


# ---------------------------------------------------------------------------
# 1. Daily rainfall (Open-Meteo, ERA5)
# ---------------------------------------------------------------------------
def get_rain():
    import pandas as pd
    out = HERE / "rain_daily_melamchi_kathmandu.csv"
    if out.exists():
        return f"{out.name} already exists, skipped"
    places = {"Melamchi": (27.83, 85.57), "Kathmandu": (27.70, 85.32)}
    frames = []
    for name, (lat, lon) in places.items():
        params = {"latitude": lat, "longitude": lon,
                  "start_date": "2001-01-01", "end_date": "2024-12-31",
                  "daily": "precipitation_sum,temperature_2m_mean",
                  "timezone": "Asia/Kathmandu", "models": "era5"}
        base = "https://archive-api.open-meteo.com/v1/archive?"
        try:
            with urllib.request.urlopen(base + urllib.parse.urlencode(params), timeout=120) as r:
                data = json.load(r)
        except urllib.error.HTTPError:          # if "models" is refused, use the default model
            params.pop("models")
            with urllib.request.urlopen(base + urllib.parse.urlencode(params), timeout=120) as r:
                data = json.load(r)
        daily = data["daily"]
        frames.append(pd.DataFrame({
            "date": daily["time"], "place": name,
            "rain_mm": daily["precipitation_sum"],
            "temp_mean_c": daily["temperature_2m_mean"],
        }))
        print(f"  {name}: {len(daily['time'])} days, grid cell at "
              f"{data['latitude']:.2f} N, {data['longitude']:.2f} E, {data['elevation']:.0f} m")
        time.sleep(2)                          # be polite to a free service
    pd.concat(frames).to_csv(out, index=False)
    return f"saved {out.name} ({out.stat().st_size / 1e6:.2f} MB)"


# ---------------------------------------------------------------------------
# 2. OpenStreetMap roads, rivers and places (osmnx)
# ---------------------------------------------------------------------------
def get_osm():
    missing = need("osmnx")
    if missing:
        return f"needs: pip install {' '.join(missing)}"
    import geopandas as gpd
    import osmnx as ox
    graph_path = HERE / "osm_melamchi_roads.graphml"
    gpkg = HERE / "osm_melamchi.gpkg"
    if graph_path.exists() and gpkg.exists():
        return "OSM files already exist, skipped"
    ox.settings.use_cache = True
    ox.settings.requests_timeout = 300
    # Roads a vehicle can use, including tracks: many rural roads in Nepal are tagged "track"
    road_filter = ('["highway"~"trunk|primary|secondary|tertiary|unclassified|residential|'
                   'living_street|service|track|road|trunk_link|primary_link|secondary_link|tertiary_link"]')
    G = ox.graph_from_bbox(BBOX, custom_filter=road_filter, retain_all=True, simplify=True)
    ox.save_graphml(G, graph_path)
    nodes, edges = ox.graph_to_gdfs(G)
    keep = [c for c in ["osmid", "name", "highway", "surface", "length", "geometry"] if c in edges.columns]
    edges = edges.reset_index()[["u", "v", "key"] + keep]
    for col in edges.columns:                  # lists (several tags on one edge) -> text
        if col != "geometry" and edges[col].map(lambda x: isinstance(x, list)).any():
            edges[col] = edges[col].map(lambda x: ";".join(map(str, x)) if isinstance(x, list) else x)
    edges.to_file(gpkg, layer="roads", driver="GPKG")

    rivers = ox.features_from_bbox(BBOX, tags={"waterway": ["river", "stream"]})
    rivers = rivers[rivers.geom_type.isin(["LineString", "MultiLineString"])].reset_index()
    rivers = rivers[[c for c in ["name", "waterway", "geometry"] if c in rivers.columns]]
    rivers.to_file(gpkg, layer="rivers", driver="GPKG")

    places = ox.features_from_bbox(BBOX, tags={"place": ["town", "village", "hamlet", "suburb"]})
    places = places[places.geom_type == "Point"].reset_index()
    places = places[[c for c in ["name", "name:en", "place", "geometry"] if c in places.columns]]
    places.to_file(gpkg, layer="places", driver="GPKG")
    return (f"saved {graph_path.name} ({len(G.nodes)} nodes, {len(G.edges)} edges) and "
            f"{gpkg.name} (roads {len(edges)}, rivers {len(rivers)}, places {len(places)})")


# ---------------------------------------------------------------------------
# 3. Sentinel-2 time series at 100 m (Planetary Computer)
# ---------------------------------------------------------------------------
def get_s2_series():
    missing = need("pystac_client", "planetary_computer", "odc.stac")
    if missing:
        return f"needs: pip install {' '.join(missing)}"
    import numpy as np
    import planetary_computer
    import pystac_client
    import xarray as xr
    from odc.stac import load
    out = HERE / "s2_melamchi_timeseries_100m.nc"
    if out.exists():
        return f"{out.name} already exists, skipped"

    catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",
                                        modifier=planetary_computer.sign_inplace)
    items = list(catalog.search(collections=["sentinel-2-l2a"], bbox=BBOX,
                                datetime="2019-01-01/2023-12-31",
                                query={"eo:cloud_cover": {"lt": 60}}).items())
    print(f"  {len(items)} scenes found")
    bands = ["B04", "B08", "B11", "SCL"]
    ds = load(items, bands=bands, bbox=BBOX, crs="EPSG:32645", resolution=100,
              groupby="solar_day", resampling={"SCL": "nearest", "*": "average"},
              chunks={"x": 512, "y": 512})
    ds = ds.compute()

    # From 25 January 2022 (processing baseline 04.00) ESA adds 1000 to every
    # reflectance value. Remove it, so that all dates use the same scale.
    baseline = {}
    for it in items:
        day = it.datetime.strftime("%Y-%m-%d")
        b = float(it.properties.get("s2:processing_baseline", "0") or 0)
        baseline[day] = max(baseline.get(day, 0), b)
    shift = xr.DataArray([1000 if baseline.get(str(t)[:10], 0) >= 4.0 else 0 for t in ds.time.values],
                         dims="time", coords={"time": ds.time})
    for b in ["B04", "B08", "B11"]:
        valid = ds[b] > 0
        v = (ds[b].astype("int32") - shift).clip(1, 65535)   # keep valid cells above 0 (0 = no data)
        ds[b] = v.where(valid, 0).astype("uint16")

    # Keep dates on which at least 30% of the box is clear land or water
    scl = ds["SCL"]
    clear = scl.isin([4, 5, 6, 11]).mean(dim=["x", "y"])   # vegetation, bare, water, snow
    ds = ds.sel(time=clear.values >= 0.3)
    ds["clear_fraction"] = clear.sel(time=ds.time)
    # Keep the file small: the 2 clearest dates of each month
    cf = ds["clear_fraction"].to_pandas()
    keep = cf.groupby([cf.index.year, cf.index.month]).nlargest(2).index.get_level_values(-1)
    ds = ds.sel(time=np.sort(keep.values))
    ds["SCL"] = ds["SCL"].astype("uint8")
    ds.attrs = {"title": "Sentinel-2 L2A time series of the Melamchi valley, 100 m",
                "credit": "Contains modified Copernicus Sentinel data 2019-2023, processed by ESA",
                "scale_factor_note": "reflectance = value x 0.0001 (the 2022 offset was removed); 0 = no data",
                "selection": "the 2 clearest dates of each month, 2019-2023 (clear = SCL 4, 5, 6 or 11)",
                "scl_note": "SCL: Sentinel-2 scene classification (4 vegetation, 5 bare, 6 water, "
                            "8-10 cloud, 3 cloud shadow, 11 snow)"}
    ds = ds.drop_vars([v for v in ds.coords if v not in ("time", "x", "y", "spatial_ref")])
    import rioxarray  # noqa: F401  (adds .rio)
    ds = ds.rio.write_crs("EPSG:32645")
    for b in ["B04", "B08", "B11", "SCL"]:   # compress; set here so the CRS link is kept
        ds[b].encoding.update({"zlib": True, "complevel": 9, "shuffle": True, "_FillValue": 0,
                               "dtype": "uint8" if b == "SCL" else "uint16"})
    ds.to_netcdf(out)
    return (f"saved {out.name}: {ds.sizes['time']} dates, {ds.sizes['y']} x {ds.sizes['x']} cells, "
            f"{out.stat().st_size / 1e6:.1f} MB")


for label, job in [("1. Rainfall", get_rain), ("2. OpenStreetMap", get_osm),
                   ("3. Sentinel-2 time series", get_s2_series)]:
    print(f"\n{label} ...")
    try:
        results[label] = job()
    except Exception as err:                   # keep going with the other parts
        results[label] = f"FAILED: {type(err).__name__}: {err}"
    print(f"  {results[label]}")

print("\nSummary")
for label, msg in results.items():
    print(f"  {label}: {msg}")
print("\nPlease send: rain_daily_melamchi_kathmandu.csv, osm_melamchi_roads.graphml, "
      "osm_melamchi.gpkg and s2_melamchi_timeseries_100m.nc")
