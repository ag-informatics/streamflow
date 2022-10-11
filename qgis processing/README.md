# QGIS Processing
QGIS Python API otherwise known as PyQGIS allows programmers to create new tools, plugins, processing scripts within the software interface. 

PyQGIS has 4 libraries:
- core: contains all basic GIS functionality
- gui: provides reusable GUI widgets
- analysis: provides high level tools for carrying out spatial analysis on vector and raster data, additonally it allows to create network topologies. 
- server: adds map server components to QGIS. 
- 3d: supports display of 3d data.

Within these libraries are multiple Python classes that are built to execute all QGIS functionalities. All classes must be named with the prefix 'Qgs'.

## Processing Algorithm
QGIS comes with established method that are found in the Toolbox window. It is possible to create new tools by writing a processing algorithm from the Python console inside QGIS using the PyQGIS classes. Processing algortihms can use the already existent tools to create new workflows and spatial operations . 

In order to make things easier and structured QGIS allows to create processing algorithms following a template. On the *Toolbox* window, click on the Python icon and select *Create New Script from Template*.

The goal is to build a processing script that will:
- Clip the previously downloaded DEM file to the extent of the area of interest.
- Fill the pixels that have no data using interpolation.
- Calculate the slope and aspect of the terrain.
- Adjust the symbology in order to display the results in a more comprehensible way.

This repository contains a separate code for each step (clipping, filling, & calculating), and one consolidated script that joins the three together. 

### Script structure
Let's disect the strucuture of the 'clip_dem' script

First the class 'QCoreApplication', is imported from the Qt framework. This class is used to provide and contain a main event loop, in which other events from the operating system and QGIS can be processed and dispatched.  Next, qgis classes needed are imported from the qgis core module. 

        from qgis.PyQt.QtCore import QCoreApplication
        from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)
        from qgis import processing

A Python class is created, it contains all the parameters and methods needed in the processing algorithm. This class is named according to the purpose of the algorithm.  

        class ClipDemProcessingAlgorithm(QgsProcessingAlgorithm):
            DEM = 'dem'
            FARM_SHP = 'farm_shape'
            CLIP_DEM = 'clipped_dem'



            def tr(self, string):
                return QCoreApplication.translate('Processing', string)

            def createInstance(self):
                return ClipDemProcessingAlgorithm()

            def name(self):
                return 'clip_dem'

            def displayName(self):
                return self.tr('Clip Dem')

            def shortHelpString(self):
                return self.tr("Clip Raster by Mask Layer")


        def initAlgorithm(self, config=None):
            self.addParameter(
                QgsProcessingParameterFeatureSource(
                    self.FARM_SHP,
                    self.tr('Input Farm Shape'),
                    [QgsProcessing.TypeVectorAnyGeometry]
                )
            )

  
        def processAlgorithm(self, parameters, context, feedback):
            
                farm_shape= self.parameterAsSource(
                    parameters,
                    self.FARM_SHP,
                    context
                )
                dem = self.parameterAsRasterLayer(
                    parameters,
                    self.DEM,
                    context
                )

        clipping = processing.runAndLoadResults(
                    'gdal:cliprasterbymasklayer',
                    {
                        'INPUT':parameters['dem'],
                        'MASK':parameters['farm_shape'],
                        'SOURCE_CRS':None,
                        'TARGET_CRS':None,
                        'TARGET_EXTENT':None,
                        'NODATA':-9999,
                        'ALPHA_BAND':False,
                        'CROP_TO_CUTLINE':True,
                        'KEEP_RESOLUTION':False,
                        'SET_RESOLUTION':False,
                        'X_RESOLUTION':None,
                        'Y_RESOLUTION':None,
                        'MULTITHREADING':False,
                        'OPTIONS':'',
                        'DATA_TYPE':0,
                        'EXTRA':'',
                        'OUTPUT':parameters['clipped_dem']
                    }
                )

        return {'clipped_dem': clipping['OUTPUT']}
