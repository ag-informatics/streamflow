# QGIS WebAPP 
PyQGIS scripts for raster operations related to hidrology and relief. 

## PyQGIS
QGIS Python API allows to run Python code in order to build processing algorithms, functions, and plugins using the QGIS interface. The code can be written on the Python Console present in QGIS or as a standalone script.

## Workflow
1. Download a Digital Elevation Model from Alos Palsar satelite that intersects with our polygon. 
![alsvrtx]("img/alaska_vertex.jpg")
2. Clip the DEM to match the extent of our polygon shapefile.
3. Fill the missing data gaps present in the DEM, using GDAL tools.
4. Calculate the slope value from the DEM altitude values.

Geopandas and ASF Search packages should be installed in the Pyhton QGIS environment. Tutorial for installing Python Packages on QGIS: https://landscapearchaeology.org/2018/installing-python-packages-in-qgis-3-for-windows/

### ASF_Search


### QGIS Processing
