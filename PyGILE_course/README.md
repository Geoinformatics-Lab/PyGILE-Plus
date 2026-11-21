# The PyGILE Course

A complete, hands-on course in Python and geospatial science for **absolute beginners**: no coding and no GIS experience needed. Every example uses data from Nepal and the Himalaya.

> **Status:** complete: 39 lessons and 1,061 practice questions, from your first line of Python to satellite time series. The course ends with Part D; [PyGILE-Plus](https://github.com/Geoinformatics-Lab/PyGILE-Plus) continues from there.

Every lesson has a navigation bar at the top and bottom, so you can move through the course like a book: **← Previous · Course home · Next →**.

## How every lesson works

Each lesson is a Jupyter notebook made of short **steps**. Every step has:

1. **Theory:** one idea, explained in plain English.
2. **Example:** code you run, on Nepal data.
3. **Practice:** three questions that get harder:
   - **Q1** needs one line of code,
   - **Q2** needs two lines,
   - **Q3** needs about three lines.

Type your answer in the empty cell under each question, run it, then click **Show solution** to check. Each lesson also shows a real error message and how to read it, ends with longer **mixed review** exercises, and finishes with a recap and a glossary of new words.

**Your answers are marked as you go.** Run the first code cell of a lesson, and every answer you run gets a small box: ✅ Correct, 🟡 Nearly there or 🔴 Not yet, with a plain-English explanation of any error. It works offline, with no account. You can also add a **free AI tutor** that writes a short, personal hint for you, and answers your follow-up questions when something is unclear: see **[The PyGILE tutor: marks, hints and a free AI helper](AI_TUTOR.md)** for step-by-step help.

**Try it on your own country.** The last lesson of each part ends with an optional exercise that repeats the part's main skills on a place you choose, anywhere in the world. It is not marked; the AI tutor gives feedback on it. To run **the whole course** on your country's data, see **[Run PyGILE on your own country's data](YOUR_OWN_DATA.md)**.

**The rule that makes it work:** try every question before you open the solution. Being stuck for a few minutes is not failure; it is how the skill is built.

## Part A · Python for geoscientists

| Lesson | You will learn | Questions |
| --- | --- | --- |
| [A1 · Python as your calculator](A_Python/A01_Python_as_your_calculator.ipynb) | Running code, arithmetic, variables, your first error | 25 |
| [A2 · Numbers and text](A_Python/A02_Numbers_and_text.ipynb) | Types, converting, comparisons, strings, f-strings | 28 |
| [A3 · Lists and loops](A_Python/A03_Lists_and_loops.ipynb) | Lists, indexing, slicing, `for` loops, building results | 28 |
| [A4 · Dictionaries and decisions](A_Python/A04_Dictionaries_and_decisions.ipynb) | Dictionaries, `if`/`elif`/`else`, tables of records | 28 |
| [A5 · Functions](A_Python/A05_Functions.ipynb) | Writing your own tools, `return`, the `math` module, slopes | 28 |
| [A6 · Errors are friends](A_Python/A06_Errors_are_friends.ipynb) | Reading tracebacks, the common errors, debugging, `try`/`except` | 25 |
| [A7 · Files, folders and paths](A_Python/A07_Files_folders_and_paths.ipynb) | `pathlib`, reading and writing text and CSV files | 28 |
| [A8 · NumPy arrays](A_Python/A08_NumPy_arrays.ipynb) | Grids of numbers, masks, a first look at slope | 29 |
| [A9 · Pandas tables](A_Python/A09_Pandas_tables.ipynb) | Reading, filtering, grouping and saving tables | 28 |
| [A10 · Plotting with Matplotlib](A_Python/A10_Plotting_with_Matplotlib.ipynb) | Line, bar and scatter charts; honest, readable figures | 28 |
| [A11 · Dates and time series](A_Python/A11_Dates_and_time_series.ipynb) | Dates in pandas, `resample`, monthly climatology, rolling rainfall totals, extremes; 24 years of daily rainfall at Melamchi and Kathmandu | 28 |
| [A12 · Scripts, modules and good habits](A_Python/A12_Scripts_modules_and_good_habits.ipynb) | `while` loops, tuples and sets, your own module, getting help, notebooks you can trust, checking code (also from AI) | 28 |

**Part A total: 331 questions with worked solutions.**

## Part B · Vector GIS: the map of Nepal

| Lesson | You will learn | Questions |
| --- | --- | --- |
| [B1 · Maps, coordinates, latitude and longitude](B_Vector/B01_Maps_and_coordinates.ipynb) | What a map is, latitude and longitude, degrees to km, map scale | 25 |
| [B2 · Points, lines and polygons](B_Vector/B02_Points_lines_and_polygons.ipynb) | Shapely geometries: the Everest trek as a line, boxes, distances | 25 |
| [B3 · GeoDataFrames and file formats](B_Vector/B03_GeoDataFrames_and_file_formats.ipynb) | Districts as a table, points from CSV, GeoPackage, Shapefile, GeoJSON | 25 |
| [B4 · Coordinate reference systems](B_Vector/B04_Coordinate_reference_systems.ipynb) | EPSG codes, UTM 45N, `set_crs` vs `to_crs`, areas in km² | 28 |
| [B5 · Selecting by attribute](B_Vector/B05_Selecting_by_attribute.ipynb) | Filtering districts, `.isin`, `.str`, boxes with `.cx` | 25 |
| [B6 · Joins and dissolve](B_Vector/B06_Joins_and_dissolve.ipynb) | Joining tables, fixing name mismatches, districts into provinces | 28 |
| [B7 · Clip and select by location](B_Vector/B07_Clip_and_select_by_location.ipynb) | Spatial predicates, neighbours, clipping | 25 |
| [B8 · Buffers and nearest features](B_Vector/B08_Buffers_and_nearest_features.ipynb) | Buffers in metres, nearest headquarters to every landslide | 25 |
| [B9 · Spatial joins and overlays](B_Vector/B09_Spatial_joins_and_overlays.ipynb) | Landslides per district, intersection, union, difference | 28 |
| [B10 · Counting points and density maps](B_Vector/B10_Counting_points_and_density_maps.ipynb) | Grids, hexagons, density, honest map classification | 28 |
| [B11 · Making a beautiful map](B_Vector/B11_Making_a_beautiful_map.ipynb) | Layers, colours, labels, scale bar, north arrow, inset map | 27 |
| [B12 · Interactive web maps](B_Vector/B12_Interactive_web_maps.ipynb) | `explore()` and folium: layers, tooltips, popups, choropleths; [lat, lon] order; sharing maps as HTML | 25 |

**Part B total: 314 questions with worked solutions.**

## Part C · Rasters: the terrain of the Kathmandu Valley and Melamchi

All eight lessons use one real elevation model: a 30 m Copernicus DEM from the Kathmandu Valley to the Melamchi valley (85.2–85.8°E, 27.55–28.0°N).

| Lesson | You will learn | Questions |
| --- | --- | --- |
| [C1 · What a raster is](C_Raster/C01_What_a_raster_is.ipynb) | Cells, resolution, bands, nodata, the transform; reading and writing GeoTIFFs | 28 |
| [C2 · Plotting rasters](C_Raster/C02_Plotting_rasters.ipynb) | `imshow`, colour maps, `extent`, colour bars, stretches, hillshade under colour | 28 |
| [C3 · Clip, mask and subset](C_Raster/C03_Clip_mask_and_subset.ipynb) | Windows, clipping to a box, masking with district polygons | 28 |
| [C4 · Reproject, resample and mosaic](C_Raster/C04_Reproject_resample_and_mosaic.ipynb) | The DEM on a 30 m UTM grid, resampling methods, coarser cells, mosaics | 28 |
| [C5 · Raster algebra and reclassification](C_Raster/C05_Raster_algebra_and_reclassification.ipynb) | Arithmetic on whole grids, conditions, elevation zones, filling gaps | 28 |
| [C6 · Terrain analysis](C_Raster/C06_Terrain_analysis.ipynb) | Slope, aspect and hillshade, and the degrees-versus-metres trap | 28 |
| [C7 · Vector and raster together](C_Raster/C07_Vector_and_raster_together.ipynb) | Sampling slope at landslides, zonal statistics, rasterizing, distance grids | 28 |
| [C8 · Interpolation](C_Raster/C08_Interpolation.ipynb) | Nearest neighbour, IDW and kriging from 109 DHM rain stations, tested honestly | 26 |
| [C9 · Spatial autocorrelation](C_Raster/C09_Spatial_autocorrelation.ipynb) | Neighbours and weights, spatial lag, Moran's I, permutation tests, local clusters, why random test splits mislead on maps | 28 |

**Part C total: 250 questions with worked solutions.**

## Part D · Satellite imagery: the 2021 Melamchi flood

Sentinel-2 images of the Melamchi valley in Sindhupalchok, before and after the June 2021 debris flow and flood, with OpenStreetMap roads and a five-year image time series.

| Lesson | You will learn | Questions |
| --- | --- | --- |
| [D1 · Satellite images and spectral bands](D_Imagery/D01_Satellite_images_and_spectral_bands.ipynb) | What a satellite measures, multi-band images, reflectance, true and false colour, spectral profiles | 28 |
| [D2 · Spectral indices](D_Imagery/D02_Spectral_indices.ipynb) | Safe band maths, NDVI, NDWI and MNDWI, thresholds and areas, NDVI against elevation | 25 |
| [D3 · Change detection: the 2021 Melamchi flood](D_Imagery/D03_Change_detection_Melamchi_flood.ipynb) | Image differencing, thresholds and their effect on area, cleaning masks, false change, a terrain rule, flood polygons and a final map | 28 |
| [D4 · Land-cover classification](D_Imagery/D04_Land_cover_classification.ipynb) | Images as tables, k-means, random forests with ESA WorldCover labels, honest accuracy, spatial tests, land-cover change | 29 |
| [D5 · Roads and networks: what the flood cut](D_Imagery/D05_Roads_and_networks.ipynb) | OpenStreetMap with osmnx and networkx: road types, shortest routes, roads in the flood strip, detours and accessibility | 28 |
| [D6 · Image time series and data cubes](D_Imagery/D06_Image_time_series_and_data_cubes.ipynb) | Five years of Sentinel-2 as an xarray cube: cloud masks, NDVI time series, seasons, before and after the flood, dask | 28 |

**Part D total: 166 questions with worked solutions.**

## After the course

Continue with the **landslide susceptibility workflow** in this repository's [`notebooks/`](../notebooks/) folder: six notebooks that go from a DEM to watersheds, terrain and hydrological factors, landforms, a landslide inventory of the 2015 Gorkha earthquake, and a final susceptibility map. They use SAGA, GRASS and WhiteboxTools, which the same Docker image already contains.

## Folders

| Folder | Contents |
| --- | --- |
| `A_Python/`, `B_Vector/`, `C_Raster/`, `D_Imagery/` | The lessons |
| `data/` | Small datasets used by the lessons, with sources and licences (see `data/README.md`) |
| `images/` | Concept diagrams used by the lessons (see `images/README.md`) |
| `outputs/` | Files the lessons write. Created when you run them and ignored by git |
| `tools/` | For course authors: `qa.py` checks a lesson and all its solutions, `check_repo.py` runs the fast repository checks (outputs cleared, navigation, question counts, and that the Docker image installs every package the course uses), `add_nav.py` refreshes the navigation bars, `lessonkit.py` builds lessons in the standard format |
| `STYLE_GUIDE.md` | How lessons are written |

## Before you start

Start the PyGILE-Plus Docker image with this repository mounted, as the main [README](../README.md#start-the-course) shows, open `PyGILE_course` in JupyterLab, and start with **A1**. In each notebook, use **Kernel → Restart Kernel and Run All Cells** if results ever look strange.
