# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterVectorDestination,
                       QgsCoordinateReferenceSystem)
from qgis import processing


class VertixProcessingAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    
    FARM_SHP = 'farm_shape'
    VERTICES = 'vertices'
    COORDINATES = 'coordinates'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return VertixProcessingAlgorithm()

    def name(self):
        return 'vertix'

    def displayName(self):
        return self.tr('Vertices and Coordinates')

    def shortHelpString(self):
        return self.tr("Extract the vertices of a shape and calculate the points coordinates")

    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.FARM_SHP,
                self.tr('Input Plygon'),
                [QgsProcessing.TypeVectorPolygon]
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
    def processAlgorithm(self, parameters, context, feedback):
       
        farm_shape= self.parameterAsSource(
            parameters,
            self.FARM_SHP,
            context
        )

        # Send some information to the user
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
        return {'vertices': extracting['OUTPUT']}
        return{'coordinates': coordianting['OUTPUT']}