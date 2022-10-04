# PyQGIS
- **Dem Download**: Explains how to create a polygon that represents the area of interest and how to download sensor data from QGIS.
- **QGIS Processing**: Explains the basic structure of a PyQGIS processing script. 

## Download and Install QGIS
QGIS is an open source GIS application. If you already QGIS installed in your computer please update it to the latest version or latest stable release. If you don't have QGIS installed you can download it here: [Download QGIS](https://www.qgis.org/en/site/forusers/download.html)

## Register at NASA Earthdata 
We will work with raster files, specifically a digital elevation model (DEM). The images will be obtained through Alaska Satelite Facility ASF, it contains imagery from various sensors. In our case we want the data from the Alos Palsar sensor. 

In order to download data, you must create a Nasa Earthdata Account here: [Nasa Earthddata Registration](https://urs.earthdata.nasa.gov/users/new?client_id=BO_n7nTIlMljdvU6kRRB3g&redirect_uri=https%3A%2F%2Fauth.asf.alaska.edu%2Flogin&response_type=code&state=https%3A%2F%2Fsearch.asf.alaska.edu)