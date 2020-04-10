import processing

def CSVtoPoint():
    # Imports CSV file to point and loads in QGIS
    csvFile = r"file:///C:\Users\imper\Documents\new_GISfiles\pointBufferTool\xyPoints.csv?\
        delimiter={}&crs=epsg:4326&xyDms=yes &xField={}&yField={}&quote={}".format(",", "x_long", "y_lat", "")
    loadLayer = QgsVectorLayer(csvFile, "CalapanPts_4326", "delimitedtext") # 
    print(loadLayer.isValid())
    QgsProject.instance().addMapLayer(loadLayer)
    
    # Saves point layer as EPSG:32651 
    path = r"C:\Users\imper\Documents\new_GISfiles\pointBufferTool\shapefiles\CalapanPts_32651.shp"
    destCrs = QgsCoordinateReferenceSystem(32651)
    saveLayer = QgsVectorFileWriter.writeAsVectorFormat(loadLayer,path,"utf-8"\
    ,destCrs,driverName = "ESRI Shapefile")    
    pointFile = r"C:\Users\imper\Documents\new_GISfiles\pointBufferTool\shapefiles\CalapanPts_32651.shp"
    vLayer = iface.addVectorLayer(pointFile, "CalapanPts_32651", "ogr")
    
def bufferPoint():
    layerName = 'CalapanPts_32651'
    outFn = r'C:\Users\imper\Documents\new_GISfiles\pointBufferTool\shapefiles\pointBuffered_32651.shp'
    bufferDist = 1000 # meters
    layers = QgsProject.instance().mapLayersByName(layerName)
    layer = layers[0]

    processing.runAndLoadResults('qgis:buffer', \
    {'INPUT': layer, 'DISTANCE': bufferDist, 'OUTPUT': outFn})
    
def dissolveBuffer():
    bufferLayer = r'C:\Users\imper\Documents\new_GISfiles\pointBufferTool\shapefiles\pointBuffered_32651.shp'
    bufferOutput = r'C:\Users\imper\Documents\new_GISfiles\pointBufferTool\shapefiles\bufferDissolved_32651.shp'
    processing.run("native:dissolve", {'INPUT': bufferLayer, 'OUTPUT': bufferOutput})
    vLayer = iface.addVectorLayer(bufferOutput, "bufferDissolved_32651", "ogr")
    
CSVtoPoint()
bufferPoint()
dissolveBuffer()