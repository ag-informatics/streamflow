# -*- coding: utf-8 -*-


from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterVectorDestination,
                       QgsCoordinateReferenceSystem)
from qgis import processing

class FarmReliefProcessingAlgorithm(QgsProcessingAlgorithm):
    DEM = 'dem'
    VERTICES = 'vertices'
    COORDINATES = 'coordinates'
    FARM_SHP = 'farm_shape'
    CLIP_DEM = 'clipped_dem'
    FILL_DEM = 'filled_dem'
    SLOPE = 'slope'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FarmReliefProcessingAlgorithm()

    def name(self):
        return 'farm_relief'

    def displayName(self):
        return self.tr('Farm Relief')

    def shortHelpString(self):
        return self.tr("Clip DEM accorgin to a farm shape and then calculate slope values for the area of interest")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.FARM_SHP,
                self.tr('Input Farm Shape'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.VERTICES,
                self.tr('Output Vertices')
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.COORDINATES,
                self.tr('Output Coordinates')
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.DEM,
                self.tr('Input Raster DEM')
                [QgsProcessing.TypeRaster]
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.CLIP_DEM,
                self.tr('Output Clipped DEM')
                [QgsProcessing.TypeRaster]
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.FILL_DEM,
                self.tr('Output Fill Dem')
                [QgsProcessing.TypeRaster]
            )
        )
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.SLOPE,
                self.tr('Output Slope Raster')
                [QgsProcessing.TypeRaster]
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
        clipped_dem= self.parameterAsRasterLayer(
            parameters,
            self.CLIP_DEM,
            context
        )
        filled_dem= self.parameterAsRasterLayer(
            parameters,
            self.FILL_DEM,
            context
        )
        
        feedback.pushInfo('Extracting vertices')
        extracting = processing.run(
            'native:extractvertices',
            {
                'INPUT':parameters['farm_shape'],
                'OUTPUT':parameters['vertices']
            }
        )
        feedback.pushInfo('Vertices extracted correctly')
        
        feedback.pushInfo('Adding X and Y coordinates')
        coordinating = processing.run(
            "native:addxyfields",
            {
                'INPUT':extracting['OUTPUT'],
                'CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
                'PREFIX':'',
                'OUTPUT':parameters['coordinates']
            }
        )
        feedback.pushInfo('Coordinates added sucessfully')
        
        feedback.pushInfo('Starting clipping')
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
        
        feedback.pushInfo('DEM clipped correctly')
        
        # Send some information to the user
        feedback.pushInfo('Starting filling')
        filling = processing.runAndLoadResults(
            'gdal:fillnodata',
            {
                'INPUT':clipping['OUTPUT'],
                'BAND':1,
                'DISTANCE':10,
                'ITERATIONS':5,
                'NO_MASK':True,
                'MASK_LAYER':None,
                'OPTIONS':'',
                'EXTRA':'',
                'OUTPUT':parameters['filled_dem']
            }
        )
        
        feedback.pushInfo('DEM filled correctly')

        # Send some information to the user
        feedback.pushInfo('Starting slope calculation')
        calculate = processing.runAndLoadResults(
            'native:slope',
            {
                'INPUT':filling['OUTPUT'],
                'Z_FACTOR':1,
                'OUTPUT':parameters['slope']
            }
        )
        feedback.pushInfo('Slope calculated correctly')
        return {'vertices': extracting['OUTPUT']}
        return{'coordinates': coordianting['OUTPUT']}
        return {'filled_dem': filling['OUTPUT']}
        return {'clipped_dem': clipping['OUTPUT']}
        return {'slope': calculate['OUTPUT']}