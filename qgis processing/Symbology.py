fn = r'C:\Users\Claudia Becerra\OneDrive - Universidad Nacional de Colombia\Documentos\GIS Project\FarmA\Clip.tif'
rlayer = iface.addRasterLayer(fn,'Clip')
stats = rlayer.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
min = stats.minimumValue
max = stats.maximumValue
symbol = QgsColorRampShader()
symbol.setColorRampType(QgsColorRampShader.Discrete)
breaks = []
labels = []
lst = []
colors = [QColor(77,80,87),QColor(78,110,93),QColor(77,161,103),QColor(59,193,74),QColor(207, 207, 207)] 

gap = max - min
jump = int(round(gap/5,0))
i = 1
val = min
breaks.append(val)

while i < 5:
    i= i + 1
    val = val + jump
    breaks.append(val)

for i in breaks:
    if i+jump < max:
        labels.append(str(i)+" to "+ str(i + jump))
    else:
        labels.append(str(i)+" to "+ str(max))

for i,j,k in (zip(breaks,colors,labels)):
    lst.append(QgsColorRampShader.ColorRampItem(i,j,k))    

symbol.setColorRampItemList(lst) 

shader = QgsRasterShader()
shader.setRasterShaderFunction(symbol)

renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
rlayer.setRenderer(renderer)

    
