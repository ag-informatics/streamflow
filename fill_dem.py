# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)
from qgis import processing


class FillDemProcessingAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    
    CLIP_DEM = 'clipped_dem'
    FILL_DEM = 'filled_dem'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FillDemProcessingAlgorithm()

    def name(self):
        return 'fill_dem'

    def displayName(self):
        return self.tr('Fill Dem')

    def shortHelpString(self):
        return self.tr("Fill the gaps or pixels with no value in a raster using interpolation")

    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.CLIP_DEM,
                self.tr('Input Clip Dem'),
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

    def processAlgorithm(self, parameters, context, feedback):
       
        clipped_dem= self.parameterAsRasterLayer(
            parameters,
            self.CLIP_DEM,
            context
        )

        # Send some information to the user
        feedback.pushInfo('Starting filling')
        filling = processing.runAndLoadResults(
            'gdal:fillnodata',
            {
                'INPUT':parameters['clipped_dem'],
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
        return {'filled_dem': filling['OUTPUT']}