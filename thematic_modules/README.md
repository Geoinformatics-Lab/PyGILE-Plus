# Thematic modules

A thematic module applies geospatial analysis to one field, from data to a finished result. Each module builds on the [PyGILE core curriculum](../PyGILE_course/README.md) (Python, vector data, rasters and satellite imagery) and runs in the same [computing environment](../docker/README.md) as the rest of PyGILE-Plus.

| Thematic module | Outcome | Prerequisites |
| --- | --- | --- |
| [Landslide Susceptibility Mapping](landslide_susceptibility/README.md) | A landslide susceptibility map of a real area, from a DEM and a landslide inventory | Core curriculum, Parts A to C |

Further thematic modules can be added here. Each module has its own folder and a README that states its outcome and prerequisites, uses real data with full citations, and runs in the PyGILE-Plus Docker image. If a module needs a package that the image lacks, add it to `docker/Dockerfile` with a pinned version.
