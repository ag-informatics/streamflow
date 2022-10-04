# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)
from qgis import processing


class ClipDemProcessingAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    
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

        # Send some information to the user
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
        return {'clipped_dem': clipping['OUTPUT']}