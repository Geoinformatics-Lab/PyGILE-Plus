# Course data

Small files used by the lessons, kept tiny so the course works offline.

To replace them with your own country's data, see [Run PyGILE on your own country's data](../YOUR_OWN_DATA.md) and the helper script `make_my_country_data.py`.

## Part A

| File | What it is | Source |
| --- | --- | --- |
| `nepal_peaks.csv` | Nepal's eight peaks above 8,000 m: height, first ascent year, province, approximate summit coordinates (WGS84) | Heights and ascent years are standard published values; coordinates are approximate |
| `rainfall_monthly_2025.csv` | Monthly rainfall of 2025 at six stations from the plains to the trans-Himalaya: `station`, `district`, `province`, `elevation_m`, then `jan_mm` to `dec_mm`, rounded to whole millimetres. Pokhara Airport, Kathmandu Airport, Jomsom, Biratnagar Airport, Jumla and Chautara | Department of Hydrology and Meteorology (DHM), Government of Nepal: the twelve monthly *Preliminary precipitation and temperature summary* reports of 2025, Annex 1, published free at [dhm.gov.np](https://www.dhm.gov.np/climate-services/climate%20reports/monthly-reports). Preliminary values, which DHM may still correct. 2025 is used rather than 2024 because page 8 of the December 2024 report (the stations Jalesor to Rara, including Pokhara and Kathmandu airports) is a repeat of page 9 of the October 2024 report. DHM's reports state no terms of reuse; this small table is kept here with full credit, and will be removed if DHM asks |
| `landslides_nepal.csv` | 166 landslides in Nepal, 2008–2016: NASA event `id`, `date`, `district`, `province`, `lat`, `lon`, `fatalities` (deaths reported), `size` and `trigger`, as NASA recorded them | NASA Global Landslide Catalog, export of 7 March 2016 ([data.nasa.gov](https://data.nasa.gov/dataset/global-landslide-catalog-export)), compiled from news and other reports. Kept: the records located to 5 km or better and with a known number of deaths; 2012 has none that pass. District and province added by locating each point in `nepal_districts.geojson`; district names written in the Government of Nepal's current spelling (for example **Tanahun**, which the boundary layer spells **Tanahu**). Cite: Kirschbaum, D.B., Adler, R., Hong, Y., Hill, S. and Lerner-Lam, A. (2010), A global landslide catalog for hazard applications, *Natural Hazards* 52, 561–575; Kirschbaum, D.B., Stanley, T. and Zhou, Y. (2015), Spatial and temporal analysis of a global landslide catalog, *Geomorphology* 249, 4–15 |

## Part B

| File | What it is | Source and licence |
| --- | --- | --- |
| `nepal_districts.geojson` | The 77 districts of Nepal: `district`, `district_code`, `province_code` | [geoJSON-Nepal](https://github.com/mesaugat/geoJSON-Nepal) by Saugat Acharya (MIT licence), derived from the OCHA common operational boundaries produced by the Survey Department of Nepal. Simplified to about 300 m so the file stays small; neighbouring districts still share exactly the same borders |
| `nepal_provinces.geojson` | The 7 provinces, made by dissolving the districts above | As above |
| `province_names.csv` | Province code, number and name (a plain table, joined to the maps in Lesson B6) | Official province names |
| `district_headquarters.geojson` | 75 district headquarters (points). There are 75, not 77, because this layer predates the split of Nawalparasi and Rukum | geoJSON-Nepal (MIT licence) |
| `world_countries.geojson` | Countries of the world at 1:110 million scale, for location maps | [Natural Earth](https://www.naturalearthdata.com/) (public domain) |
| `everest_trek.csv` | Eight stops on the Lukla–Everest Base Camp trek with elevation | Approximate coordinates and commonly cited elevations, for teaching |

## Part C

| File | What it is | Source and licence |
| --- | --- | --- |
| `dem_kathmandu_melamchi.tif` | Digital elevation model of the Kathmandu Valley and Sindhupalchok (85.2–85.8° E, 27.55–28.0° N), 1 arc-second (about 30 m) cells, WGS84, elevations in whole metres (`int16`) | Clipped from the Copernicus DEM GLO-30 tile N27 E085 (see the notice below) |
| `landslides_melamchi.csv` | 283 landslides triggered by the Gorkha earthquake of 25 April 2015: `id`, `lat`, `lon` (a point inside each landslide's mapped outline) and `area_m2`. All landslides of 5,000 m² or more whose point lies at least about 1 km inside the DEM's edges | U.S. Geological Survey, public domain: Zekkos, D., Clark, M.K., Roback, K., Gallen, S.F., West, A.J., Li, G., Chamlagain, D. and Godt, J.W. (2017), Map data of landslides triggered by the 25 April 2015 Mw 7.8 Gorkha, Nepal earthquake, U.S. Geological Survey data release, https://doi.org/10.5066/F7DZ06F9 (file `Full20170209.shp`) |
| `rain_gauges_monsoon_2024.csv` | 109 meteorological stations with their total rainfall of the monsoon of 2024, June to September: `station`, `district`, `province`, `lat`, `lon`, `elevation_m`, `monsoon_mm` | Department of Hydrology and Meteorology (DHM), Government of Nepal: *Preliminary precipitation and temperature summary, Monsoon (June–September) 2024*, Annex 1, published free at [dhm.gov.np](https://www.dhm.gov.np/climate-services/climate%20reports/monthly-reports). The 3 stations without a total are left out. District and province added from `nepal_districts.geojson`. DHM's report states no terms of reuse; this small table is kept here with full credit, and will be removed if DHM asks |

**Copernicus DEM notice (required by its licence).** `dem_kathmandu_melamchi.tif` was produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. The organisations in charge of the Copernicus programme by law or by delegation do not incur any liability for any use of the Copernicus WorldDEM-30. This course is not endorsed by the Copernicus programme, the European Union, ESA, DLR or Airbus. Anyone who redistributes this file must keep this notice.

## Part D

| File | What it is | Source and licence |
| --- | --- | --- |
| `s2_melamchi_before.tif` | Sentinel-2 Level-2A surface reflectance of the Melamchi valley, 29 October 2020: 10 bands (B02, B03, B04, B05, B06, B07, B08, B8A, B11, B12), resampled to one 20 m grid in UTM 45N (EPSG:32645), 1006 × 702 cells, `uint16`, nodata 0. Multiply by 0.0001 for reflectance | Copernicus Sentinel-2 (free and open), through Microsoft Planetary Computer; made with `get_sentinel2_melamchi.py` |
| `s2_melamchi_after.tif` | The same grid and bands, 11 November 2021, after the June 2021 Melamchi flood | As above |
| `s2_melamchi_scenes.csv` | The two scenes used, with dates and cloud cover | As above |
| `worldcover_melamchi_2021.tif` | ESA WorldCover 2021 land cover on the same 20 m grid as the Sentinel-2 images (the most common 10 m class in each 20 m cell), `uint8`, nodata 0. Codes: 10 tree cover, 30 grassland, 40 cropland, 50 built-up, 60 bare or sparse vegetation, 80 permanent water | [ESA WorldCover](https://esa-worldcover.org/) 2021 (v200), CC BY 4.0, through Microsoft Planetary Computer; made with `get_worldcover_melamchi.py` |

**Sentinel-2 credit (required).** Contains modified Copernicus Sentinel data 2020–2021, processed by ESA.

**WorldCover credit (required, CC BY 4.0).** © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium.

## Extra lessons (A11, D5, D6)

| File | What it is | Source and licence |
| --- | --- | --- |
| `rain_daily_melamchi_kathmandu.csv` | Daily rainfall (`rain_mm`) and mean air temperature (`temp_mean_c`) for 2001–2024 at two places, Melamchi (27.83° N, 85.57° E) and Kathmandu (27.70° N, 85.32° E): 8,766 days each. Columns `date`, `place`, `rain_mm`, `temp_mean_c` | Open-Meteo historical weather API (CC BY 4.0), values from the **ERA5 reanalysis** of the Copernicus Climate Change Service. ERA5 cells are about 25–30 km wide: these are model estimates for a large area, not rain-gauge measurements, and they smooth out local extremes |
| `osm_melamchi_roads.graphml` | The road network of the Melamchi valley (854 junctions, 1,942 road segments): motorable roads and tracks, as a graph for osmnx and networkx | © OpenStreetMap contributors, ODbL; downloaded with osmnx |
| `osm_melamchi.gpkg` | The same roads as lines (layer `roads`), rivers and streams (`rivers`) and named places (`places`) | © OpenStreetMap contributors, ODbL |
| `s2_melamchi_timeseries_100m.nc` | Sentinel-2 L2A time series of the Part D box, 2019–2023: the 2 clearest dates of each month (112 dates), bands B04, B08, B11 and the scene classification `SCL`, 100 m cells, UTM 45N, NetCDF. Reflectance = value × 0.0001 (ESA's 2022 offset removed), 0 = no data | Copernicus Sentinel-2 (free and open), through Microsoft Planetary Computer |

**Credits (required).** Weather data by Open-Meteo.com (CC BY 4.0), from the ERA5 reanalysis of the Copernicus Climate Change Service. Map data © OpenStreetMap contributors, available under the Open Database Licence (ODbL). Contains modified Copernicus Sentinel data 2019–2023, processed by ESA.

Spellings differ between sources: the boundary layer follows older OCHA spellings, such as **Tanahu** and **Chitawan**, while the landslide and rainfall tables use the Government of Nepal's current ones, **Tanahun** and **Chitwan**. Lesson B6 shows how to find and fix such mismatches, a very common problem with real data.

`make_data.py` rebuilds the Part B files and the Part C DEM from the original sources. `make_observed_data.py` rebuilds the landslide and rainfall tables from the files downloaded from NASA, the USGS and DHM; its first lines say where to get them.

`get_sentinel2_melamchi.py` downloads the two Sentinel-2 images of Part D, `get_worldcover_melamchi.py` the ESA WorldCover 2021 land-cover map on the same grid, and `get_extra_data.py` the files of lessons A11, D5 and D6. They use Microsoft Planetary Computer, Open-Meteo and OpenStreetMap, none of which needs an account; run them once in the PyGILE-Plus container or the `pygile` environment.
