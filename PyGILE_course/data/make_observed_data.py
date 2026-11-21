"""Rebuild the course's observed landslide and rainfall tables from their sources.

You do not need to run this to follow the course: the files it makes are already
in this folder. It is here so anyone can check, reproduce or update them.

Download these files by hand into the folder `_raw_observed/` next to this script
(the sites need a browser or have no stable download API):

1. NASA Global Landslide Catalog, export of 7 March 2016 (NASA; free to use, cite it):
   https://data.nasa.gov/docs/legacy/Global_Landslide_Catalog_Export/Global_Landslide_Catalog_Export_rows.csv
   -> Global_Landslide_Catalog_Export_rows.csv
2. USGS landslides of the 2015 Gorkha earthquake (public domain), DOI 10.5066/F7DZ06F9:
   the zip Roback_Nepal_final_files.zip from https://doi.org/10.5066/F7DZ06F9
   -> Roback_Nepal_final_files.zip
3. Department of Hydrology and Meteorology (DHM), Government of Nepal, monthly and
   seasonal "Preliminary precipitation and temperature summary" reports,
   from https://www.dhm.gov.np/climate-services/climate%20reports/monthly-reports
   -> JJAS_2024.pdf (the monsoon of 2024) and January_2025.pdf ... December_2025.pdf
   (2025, not 2024: page 8 of DHM's December 2024 report, the stations Jalesor to Rara,
   is October 2024's page 9 printed again, so those December values are October's)

Needs the `pygile` environment plus pypdf (pip install pypdf).
Run from this folder:  python make_observed_data.py
"""
from pathlib import Path
import re
import zipfile

import geopandas as gpd
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "_raw_observed"

# The boundary layer follows older OCHA spellings. The landslide table uses the
# Government of Nepal's current spelling, which differs for a few districts.
OFFICIAL_SPELLING = {"Chitawan": "Chitwan", "Kabhrepalanchok": "Kavrepalanchok",
                     "Makawanpur": "Makwanpur", "Tanahu": "Tanahun",
                     "Terhathum": "Tehrathum", "Kapilbastu": "Kapilvastu"}


def districts_and_provinces():
    districts = gpd.read_file(HERE / "nepal_districts.geojson")
    names = pd.read_csv(HERE / "province_names.csv")
    return districts.merge(names[["province_code", "province"]], on="province_code")


def landslides_nepal():
    """NASA Global Landslide Catalog: Nepal, located to 5 km or better, known deaths."""
    glc = pd.read_csv(RAW / "Global_Landslide_Catalog_Export_rows.csv")
    keep = ((glc["country_name"] == "Nepal")
            & (glc["event_import_source"] == "glc")
            & glc["location_accuracy"].isin(["exact", "1km", "5km"])
            & glc["fatality_count"].notna())
    glc = glc[keep].copy()
    glc["date"] = pd.to_datetime(glc["event_date"], format="%m/%d/%Y %I:%M:%S %p").dt.strftime("%Y-%m-%d")
    points = gpd.GeoDataFrame(glc, geometry=gpd.points_from_xy(glc["longitude"], glc["latitude"]),
                              crs="EPSG:4326")
    joined = gpd.sjoin(points, districts_and_provinces()[["district", "province", "geometry"]],
                       predicate="within", how="inner")
    out = pd.DataFrame({
        "id": joined["event_id"].astype(int),
        "date": joined["date"],
        "district": joined["district"].replace(OFFICIAL_SPELLING),
        "province": joined["province"],
        "lat": joined["latitude"].round(4),
        "lon": joined["longitude"].round(4),
        "fatalities": joined["fatality_count"].astype(int),
        "size": joined["landslide_size"],
        "trigger": joined["landslide_trigger"],
    }).sort_values(["date", "id"])
    out.to_csv(HERE / "landslides_nepal.csv", index=False)
    print("landslides_nepal.csv:", len(out), "records")


def landslides_melamchi():
    """USGS Gorkha earthquake landslides of at least 5,000 m², at least 1 km inside the course DEM."""
    with zipfile.ZipFile(RAW / "Roback_Nepal_final_files.zip") as z:
        z.extractall(RAW)
    full = gpd.read_file(RAW / "Roback_Nepal_final_files" / "Full20170209.shp")
    full["geometry"] = full.geometry.make_valid()
    point = full.geometry.representative_point().to_crs("EPSG:4326")   # always inside the polygon
    inside = point.x.between(85.21, 85.79) & point.y.between(27.56, 27.99) & (full["Area"] >= 5000)
    sel = full[inside].copy()
    sel["lon"], sel["lat"] = point[inside].x.round(5), point[inside].y.round(5)
    sel = sel.sort_values(["lat", "lon"], ascending=[False, True]).reset_index(drop=True)
    out = pd.DataFrame({"id": [f"G{i + 1:03d}" for i in range(len(sel))],
                        "lat": sel["lat"], "lon": sel["lon"],
                        "area_m2": sel["Area"].round().astype(int)})
    out.to_csv(HERE / "landslides_melamchi.csv", index=False)
    print("landslides_melamchi.csv:", len(out), "landslides")


# One station in the DHM annex: name, latitude, longitude, elevation, total, % of normal
STATION = re.compile(r"([A-Z][A-Za-z.()' /-]*?)\s+(\d{2}\.\d+)\s+(\d{2}\.\d+)\s+(\d+)\s+(\d+(?:\.\d+)?|-)\s+(\d+(?:\.\d+)?|-)")


def dhm_stations(pdf_path):
    """Read the station table (Annex 1) of a DHM summary report into a DataFrame."""
    import pypdf
    rows = []
    for page in pypdf.PdfReader(pdf_path).pages:
        for line in page.extract_text().splitlines():   # two stations side by side per line
            for m in STATION.finditer(line):
                name, lat, lon, elev, total, pct = m.groups()
                rows.append({"station": " ".join(name.split()), "lat": float(lat), "lon": float(lon),
                             "elevation_m": int(elev),
                             "total_mm": None if total == "-" else float(total),
                             "pct_normal": None if pct == "-" else float(pct)})
    return pd.DataFrame(rows).drop_duplicates("station")


def rain_gauges_monsoon():
    """DHM monsoon (June to September) 2024 totals at every station that reported one."""
    st = dhm_stations(RAW / "JJAS_2024.pdf").dropna(subset=["total_mm"])
    points = gpd.GeoDataFrame(st, geometry=gpd.points_from_xy(st["lon"], st["lat"]), crs="EPSG:4326")
    joined = gpd.sjoin(points, districts_and_provinces()[["district", "province", "geometry"]],
                       predicate="within", how="left")
    joined["district"] = joined["district"].replace(OFFICIAL_SPELLING)
    out = joined[["station", "district", "province", "lat", "lon", "elevation_m", "total_mm"]]
    out = out.rename(columns={"total_mm": "monsoon_mm"}).sort_values("station")
    out.to_csv(HERE / "rain_gauges_monsoon_2024.csv", index=False)
    print("rain_gauges_monsoon_2024.csv:", len(out), "stations")


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
# Six stations across Nepal with a total for every month of 2025: plains, hills, mountains
STATIONS = {"Pokhara Airport": ("Kaski", "Gandaki"), "Kathmandu Airport": ("Kathmandu", "Bagmati"),
            "Jomsom": ("Mustang", "Gandaki"), "Biratnagar Airport": ("Morang", "Koshi"),
            "Jumla": ("Jumla", "Karnali"), "Chautara": ("Sindhupalchok", "Bagmati")}


def rainfall_monthly():
    """Monthly rainfall of 2025 at six DHM stations, rounded to whole millimetres."""
    tables = {month: dhm_stations(RAW / f"{month}_2025.pdf").set_index("station") for month in MONTHS}
    rows = []
    for station, (district, province) in STATIONS.items():
        row = {"station": station, "district": district, "province": province,
               "elevation_m": int(tables["January"].loc[station, "elevation_m"])}
        for month in MONTHS:
            row[month[:3].lower() + "_mm"] = int(round(tables[month].loc[station, "total_mm"]))
        rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(HERE / "rainfall_monthly_2025.csv", index=False)
    print("rainfall_monthly_2025.csv:", len(out), "stations")


if __name__ == "__main__":
    rainfall_monthly()
    landslides_nepal()
    landslides_melamchi()
    rain_gauges_monsoon()
