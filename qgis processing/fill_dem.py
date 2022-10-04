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

class FillDemProcessingAlgorithm(QgsProcessingAlgorithm):

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    
    FILL_DEM = 'filled_dem'
    CLIP_DEM = 'clipped_dem'
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return FillDemProcessingAlgorithm()

    def name(self):
        return 'fill_dem'

    def displayName(self):
        return self.tr('Fill Dem')

    def shortHelpString(self):
        return self.tr("Fill missing data cells using interpolation")

    def initAlgorithm(self, config=None):
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CLIP_DEM,
                self.tr('Input DEM'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.FILL_DEM,
                self.tr('Output Filled DEM')
                [QgsProcessing.TypeRaster]
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
       
        farm_shape= self.parameterAsRasterLayer(
            parameters,
            self.CLIP_DEM,
            context
        )

        # Send some information to the user
        feedback.pushInfo('Starting filling')

        filledgaps = processing.runAndLoadResults(
            'gdal:fillnodata', 
            {
                'INPUT':parameters['clipped_dem'],
                'BAND':1,
                'DISTANCE':10,
                'ITERATIONS':0,
                'NO_MASK':False,
                'MASK_LAYER':None,
                'OPTIONS':'',
                'EXTRA':'',
                'OUTPUT':parameters['filled_dem']
            }
        )
        
        feedback.pushInfo('DEM filled correctly')
        return {'filled_dem': filledgaps['OUTPUT']}