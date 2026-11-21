# Run PyGILE on your own country's data

The course teaches with data from Nepal, but every method in it works anywhere. There are two ways to use it for your own country:

1. **Try one project per part.** The last lesson of each part (A12, B12, C9 and D6) ends with an optional exercise, *Your own country*, which repeats the part's main skills on a place you choose. No setup is needed.
2. **Run the whole course on your data.** Replace the course data with your country's, and every lesson runs on it. This guide shows how, step by step.

This guide is for teachers, and for learners who have finished at least Part A. It takes an afternoon for the data, plus some time per lesson for step 3.

---

## The one idea to understand first

The lessons read their data from the folder `PyGILE_course/data/` **by file name**, for example:

```python
districts = gpd.read_file(DATA / "nepal_districts.geojson")
```

So if you replace `nepal_districts.geojson` with a file **of the same name and with the same columns**, this line reads your districts instead, and the code after it runs on your country.

**Keep the file names**, even the ones that say `nepal_` or `melamchi`. Up to 18 lessons read each file, and keeping the names means none of them has to change its paths.

---

## Before you start

1. **Work in your own copy.** Fork the repository on GitHub, or copy the whole `PyGILE_course` folder, and change only the copy.
2. **Decide four things** and write them down:

| What | Nepal's value | Yours |
| --- | --- | --- |
| Your country's 3-letter code | `NPL` | for example `LKA`, `IND`, `KEN` ([list of codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)) |
| A **study area** with hills or mountains, for Part C: a box about 0.6° wide and 0.45° high, inside one whole-degree square (no whole number between west and east, or between south and north) | 85.2° to 85.8° E, 27.55° to 28.0° N (Kathmandu to Melamchi) | west, south, east, north |
| A **smaller box**, about 0.15° × 0.15°, inside the study area, for the satellite images of Part D. Choose a place where something changed that you can see from space: a flood, a fire, a new reservoir, a growing town | 85.48° to 85.62° E, 27.80° to 27.98° N (the Melamchi valley) | west, south, east, north |
| The **UTM zone** of your study area (a projected CRS in metres) | UTM zone 45 N, `EPSG:32645` | zone = `int((longitude + 180) // 6) + 1`; the code is 32600 + zone north of the equator, 32700 + zone south of it |

3. **You need the internet** for the downloads. Run the scripts in the PyGILE-Plus Docker image: in JupyterLab, choose **File → New → Terminal**, then `cd PyGILE-Plus/PyGILE_course/data`.

---

## Step 1 · Replace the data files

Every file in `data/` is listed below, with the lessons that read it, the columns your file must have, and how to make it. Files marked ⭐ are made by the helper script `data/make_my_country_data.py`.

### The helper script

Open `data/make_my_country_data.py`, change the **SETTINGS** at the top (your country code, your study area box, a few places for rainfall), and run it from the `data` folder:

```
python make_my_country_data.py                  # every part
python make_my_country_data.py boundaries dem   # only these parts
```

Run `boundaries` first: the other parts use your new districts. Before it replaces a course file for the first time, it copies the Nepal original to `data/_nepal_original/`.

### Country files

| File | Read by | Must contain | How to make yours |
| --- | --- | --- | --- |
| `nepal_districts.geojson` ⭐ | A12, B1, B3–B12, C2, C3, C6–C9 | polygons in WGS84 (`EPSG:4326`); columns `district`, `district_code`, `province_code` | `boundaries`: your country's units at level ADM2 from [geoBoundaries](https://www.geoboundaries.org). If your country's ADM2 units are very small or very many, set `UNITS = "ADM1"` and `GROUPS` to a coarser grouping you make yourself |
| `nepal_provinces.geojson` ⭐ | B3, B4, B6, B7, B9–B12, C8 | polygons; column `province_code` | `boundaries`: the districts dissolved by province, so their borders match exactly |
| `province_names.csv` ⭐ | B6, B7, B9, B11, B12, C8 | columns `province_code`, `province_number`, `province` | `boundaries`: the ADM1 names from geoBoundaries |
| `district_headquarters.geojson` ⭐ | B3, B7–B9, B12, C1–C3, C6, C7 | points; column `name` | `boundaries` puts a point inside each district, named after it. Better: replace them with the real district towns, if you have their coordinates. Lessons B9, B12, C1 and C3 pick real towns by name (such as Chautara), so change those names in step 2 either way |
| `world_countries.geojson` | B4, B7, B11 | (the whole world already) | **Keep it.** It covers every country |

### Tables for Parts A and B

| File | Read by | Must contain | How to make yours |
| --- | --- | --- | --- |
| `landslides_nepal.csv` ⭐ | A7, A9, A10, A12, B2–B12 | `id`, `date` (YYYY-MM-DD), `district`, `province`, `lat`, `lon`, `fatalities`, `size`, `trigger` | `landslides`: your country's records from the NASA Global Landslide Catalog (2007–2016). Download the catalog once in a browser; the script prints the link. For a country with few records, add `"10km"` to `GLC_ACCURACY`. Any other table of events with points works too: floods, fires, earthquakes, if you keep the column names |
| `rainfall_monthly_2025.csv` ⭐ | A7, A9, A10, A12 | `station`, `district`, `province`, `elevation_m`, `jan_mm` … `dec_mm` | `rainfall`: one year of monthly rain at about six places from [Open-Meteo](https://open-meteo.com), modelled from the ERA5 reanalysis. Real station totals from your national weather service are better, in the same columns |
| `nepal_peaks.csv` | A7–A10, A12, B1–B4, B7, B8, B12 | 8 rows: `name`, `height_m`, `first_ascent` (a year), `province`, `lat`, `lon` | By hand, from an atlas, Wikipedia or [OpenStreetMap](https://www.openstreetmap.org): your country's highest mountains. With no famous climbs, use other landmarks, and put another year in `first_ascent`, such as the year a park was founded |
| `everest_trek.csv` | A12, B1–B4, B7, B8, B11, B12 | 8 rows: `order` (1 to 8), `place`, `lat`, `lon`, `elevation_m` | By hand: 8 stops along a route you know, such as a trek, a bus route or a river. [Open-Meteo](https://open-meteo.com/en/docs/elevation-api) or Google Earth gives the elevations |

### Files for Part C (your study area)

| File | Read by | Must contain | How to make yours |
| --- | --- | --- | --- |
| `dem_kathmandu_melamchi.tif` ⭐ | C1–C7, C9, D2, D3, D5 | one band of elevation in whole metres (`int16`, no data = −32768), in **degrees** (`EPSG:4326`), about 30 m cells. Keep it in degrees: the lessons reproject it themselves | `dem`: clipped from the [Copernicus DEM GLO-30](https://registry.opendata.aws/copernicus-dem/). Download the one tile it names once in a browser |
| `landslides_melamchi.csv` | C2, C7, C9 | `id`, `lat`, `lon`, `area_m2`: landslides **inside your study area** | The hardest file to replace. Look for a landslide inventory of an event in your area (the USGS publishes many: search [ScienceBase](https://www.sciencebase.gov) for "landslide inventory" and your region), or map some yourself on satellite images. Any points of something inside your box with a size also work, such as ponds or buildings. Replace it **together with** the DEM, so the points fall on it |
| `rain_gauges_monsoon_2024.csv` ⭐ | C8 | `station`, `district`, `province`, `lat`, `lon`, `elevation_m`, `monsoon_mm` (any season's total, despite the name) | `gauges`: about 100 random points in your country with the season's rain from Open-Meteo. Real rain gauges from your national weather service are much better for Lesson C8, which compares interpolation methods |

### Files for Part D (your smaller box)

These are made by the download scripts the course already uses. Change the settings at the top of each script, then run it from the `data` folder.

| File | Read by | Script and what to change |
| --- | --- | --- |
| `s2_melamchi_before.tif`, `s2_melamchi_after.tif`, `s2_melamchi_scenes.csv` | D1–D6 (`scenes`: D1, D3) | `get_sentinel2_melamchi.py`: `BBOX` (your smaller box), `CRS` (your UTM zone), and the two `PERIODS`, before and after your event, in the same season |
| `worldcover_melamchi_2021.tif` | D4, D6 | `get_worldcover_melamchi.py`: `BBOX`, a little larger than the Sentinel-2 box. Run it after the Sentinel-2 script: it copies that grid |
| `rain_daily_melamchi_kathmandu.csv` | A11 | `get_extra_data.py`, part 1: the two `places` and their coordinates, and the `timezone` |
| `osm_melamchi_roads.graphml`, `osm_melamchi.gpkg` | D5 | `get_extra_data.py`, part 2: `BBOX` |
| `s2_melamchi_timeseries_100m.nc` | D6 | `get_extra_data.py`, part 3: `BBOX` and the two `"EPSG:32645"` |

`get_extra_data.py` skips files that already exist, so move the Nepal ones to `data/_nepal_original/` before you run it.

---

## Step 2 · Change what the lessons type for Nepal

Some lesson code types Nepal's values directly, such as a district name to select or a box to clip. After step 1 these lines need your values. JupyterLab's **Find and Replace** finds them in the code and in the hidden solutions: press **Ctrl + F** (Cmd + F on a Mac), then click the small arrow to show **Replace**.

| What | Nepal's value (examples) | Lessons | Change to |
| --- | --- | --- | --- |
| The UTM CRS | `"EPSG:32645"` | B4, B11, C1, C4–C7, C9, D3, D5, D6 | your UTM zone |
| Province and district codes | `"NP03"` (Bagmati Province), `"NP0335"` | B3–B7, B9–B12 | your codes: `make_my_country_data.py` prints them, and `province_names.csv` lists them |
| An equal-area CRS | `"ESRI:102025"` (Asia North Albers) | B4 | one for your region: search [epsg.io](https://epsg.io) for "equal area" and your region |
| Coordinates and boxes typed in code | `(85.307, 27.704)` (Kathmandu), `(85.2, 27.55, 85.55, 27.82)` | B2, B3, B7, B11, B12, C1–C3, C7, C9, D5, D6 | points and boxes in your country or study area |
| Names used to select rows | districts such as `"Tanahu"`, provinces such as `"Bagmati"`, towns such as `"Chautara"`, stations such as `"Pokhara Airport"`, and `"Melamchi"` | A7, A9–A12, B1, B3–B12, C1–C3, C7–C9, D1, D3, D5 | names that exist in your files. `print(districts["district"].tolist())` lists them |
| Dates of events | `"2021-06-15"` (the Melamchi flood) | A11, D6 | the date of your event |

**Part A** (A1–A6 and A8) also types small lists of its own, such as Nepal's peaks or a trek. Those run as they are; change them only if you want local examples.

**The text around the code still describes Nepal**, and so do the numbers quoted in the solutions. That is expected: your results will be different. A teacher can rewrite the text once the code runs.

---

## Step 3 · Run every lesson

Open each lesson and choose **Kernel → Restart Kernel and Run All Cells**. Then type your own answers as usual.

When a cell fails, the cause is almost always a name or a box from step 2:

- `KeyError: 'Tanahu'` or an empty table: a Nepal name is still in the code.
- An empty plot or map, or `0` rows after a clip: a box or coordinates still point at Nepal.
- Wrong distances or areas: a CRS is still `EPSG:32645`.

A teacher can test a whole lesson with its hidden solutions in one go, from the `PyGILE_course` folder:

```
python tools/qa.py B_Vector/B06_Joins_and_dissolve.ipynb
```

---

## Step 4 · Make the marks fit your data

The tutor's ✅ 🟡 🔴 marks compare each answer with the result **for Nepal**, so on your data they say 🔴 even when your answer is right. You have two choices:

- **Turn marking off** with `%tutor off`. *Show solution* and `%tutor ask` still work.
- **Rebuild the marks for your data** (teachers). Once a lesson's solutions run on your data (step 3), run this from the top folder of the repository:

  ```
  python PyGILE_course/tools/build_answer_key.py B_Vector/B06_Joins_and_dissolve.ipynb
  ```

  It runs every hidden solution on your data and saves the results as the new answers. Leave out the lesson name to rebuild all 39. Now the marks fit your country.

---

## Credits to keep with your data

Each source asks for credit when you share your work:

- **geoBoundaries**: credit geoBoundaries and the original source; `make_my_country_data.py` prints both, with the licence.
- **Copernicus DEM**: keep the notice from the [data README](data/README.md).
- **NASA Global Landslide Catalog**: the two citations in the [data README](data/README.md).
- **Open-Meteo**: "Weather data by Open-Meteo.com (CC BY 4.0), from the ERA5 reanalysis of the Copernicus Climate Change Service."
- **Sentinel-2, WorldCover and OpenStreetMap**: the credit lines at the top of each download script.
- Your own national data: the agency that made it.

---

## Putting Nepal back

Copy the files in `data/_nepal_original/` back into `data/`. If you work in a Git copy, `git checkout -- PyGILE_course/data PyGILE_course/A_Python PyGILE_course/B_Vector PyGILE_course/C_Raster PyGILE_course/D_Imagery` restores every original file and lesson.
