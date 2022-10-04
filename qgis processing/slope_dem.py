# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)
from qgis import processing


class SlopeProcessingAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    
    FILL_DEM = 'filled_dem'
    SLOPE = 'slope'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return SlopeProcessingAlgorithm()

    def name(self):
        return 'slope_dem'

    def displayName(self):
        return self.tr('Slope')

    def shortHelpString(self):
        return self.tr("Calculate the slope of a DEM")

    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.FILL_DEM,
                self.tr('Input Dem'),
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
       
        filled_dem= self.parameterAsRasterLayer(
            parameters,
            self.FILL_DEM,
            context
        )

        # Send some information to the user
        feedback.pushInfo('Starting slope calculation')
        calculate = processing.runAndLoadResults(
            'native:slope',
            {
                'INPUT':parameters['filled_dem'],
                'Z_FACTOR':1,
                'OUTPUT':parameters['slope']
            }
        )
        feedback.pushInfo('Slope calculated correctly')
        return {'slope': calculate['OUTPUT']}