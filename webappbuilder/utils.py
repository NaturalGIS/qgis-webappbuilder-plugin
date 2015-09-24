import os
import re
from PyQt4.QtCore import *
from qgis.core import *
import subprocess
import uuid

METHOD_FILE= 0
METHOD_WMS = 1
METHOD_WFS = 2
METHOD_WMS_POSTGIS = 3
METHOD_WFS_POSTGIS = 4
METHOD_DIRECT = 5

MULTIPLE_SELECTION_DISABLED = 0
MULTIPLE_SELECTION_ALT_KEY = 1
MULTIPLE_SELECTION_SHIFT_KEY = 2
MULTIPLE_SELECTION_NO_KEY = 3



TYPE_MAP = {
    QGis.WKBPoint: 'Point',
    QGis.WKBLineString: 'LineString',
    QGis.WKBPolygon: 'Polygon',
    QGis.WKBMultiPoint: 'MultiPoint',
    QGis.WKBMultiLineString: 'MultiLineString',
    QGis.WKBMultiPolygon: 'MultiPolygon',
    }

class Layer():

    def __init__(self, layer, visible, popup, method, clusterDistance, clusterColor,
                 allowSelection, refreshInterval, showInOverview, timeInfo, showInControls,
                 singleTile):
        self.layer = layer
        self.visible = visible
        self.popup = popup
        self.method = method
        self.clusterDistance = clusterDistance
        self.clusterColor = clusterColor
        self.allowSelection = allowSelection
        self.refreshInterval = refreshInterval
        self.showInOverview = showInOverview
        self.timeInfo = timeInfo
        self.showInControls = showInControls
        self.singleTile = singleTile

    @staticmethod
    def fromDict(d):
        layer = Layer(*[None] * 11)
        for a, b in d.iteritems():
            setattr(layer, a, b)
        layer.layer = findProjectLayerByName(layer.layer)
        return layer


def replaceInTemplate(template, values):
    path = os.path.join(os.path.dirname(__file__), "templates", template)
    with open(path) as f:
        lines = f.readlines()
    s = "".join(lines)
    for name,value in values.iteritems():
        s = s.replace(name, value)
    return s

def tempFolder():
    tempDir = os.path.join(unicode(QDir.tempPath()), 'webappbuilder')
    if not QDir(tempDir).exists():
        QDir().mkpath(tempDir)
    return unicode(os.path.abspath(tempDir))

def tempFilenameInTempFolder(basename):
    path = tempFolder()
    folder = os.path.join(path, str(uuid.uuid4()).replace("-",""))
    if not QDir(folder).exists():
        QDir().mkpath(folder)
    filename =  os.path.join(folder, basename)
    return filename

def tempFolderInTempFolder():
    path = tempFolder()
    folder = os.path.join(path, str(uuid.uuid4()).replace("-",""))
    if not QDir(folder).exists():
        QDir().mkpath(folder)
    return folder

def exportLayers(layers, folder, progress, precision, crsid):
    progress.setText("Writing local layer files")
    destCrs = QgsCoordinateReferenceSystem(crsid)
    layersFolder = os.path.join(folder, "data")
    QDir().mkpath(layersFolder)
    reducePrecision = re.compile(r"([0-9]+\.[0-9]{%s})([0-9]+)" % precision)
    removeSpaces = lambda txt:'"'.join( it if i%2 else ''.join(it.split())
                         for i,it in enumerate(txt.split('"')))
    for i, appLayer in enumerate(layers):
        if appLayer.method == METHOD_FILE:
            layer = appLayer.layer
            if layer.type() == layer.VectorLayer:
                path = os.path.join(layersFolder, "lyr_%s.json" % safeName(layer.name()))
                QgsVectorFileWriter.writeAsVectorFormat(layer,  path, "utf-8", destCrs, 'GeoJson')
                with open(path) as f:
                    lines = f.readlines()
                with open(path, "w") as f:
                    for line in lines:
                        line = reducePrecision.sub(r"\1", line)
                        line = line.strip("\n\t ")
                        line = removeSpaces(line)
                        if layer.geometryType() == QGis.Point:
                            line = line.replace("MultiPoint", "Point")
                            line = line.replace("[ [", "[")
                            line = line.replace("] ]", "]")
                            line = line.replace("[[", "[")
                            line = line.replace("]]", "]")
                        f.write(line)
            elif layer.type() == layer.RasterLayer:
                destFile = os.path.join(layersFolder, safeName(layer.name()) + ".jpg").replace("\\", "/")
                img = layer.previewAsImage(QSize(layer.width(),layer.height()))
                img.save(destFile)
        progress.setProgress(int(i*100.0/len(layers)))


def findLayerByName(name, layers):
    for layer in layers:
        if layer.layer.name() == name:
            return layer

def safeName(name):
    #TODO: we are assuming that at least one character is valid...
    validChars = '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    return ''.join(c for c in name if c in validChars).lower()


def findProjectLayerByName(name):
    layers = QgsProject.instance().layerTreeRoot().findLayers()
    for layer in layers:
        mapLayer = layer.layer()
        if mapLayer.name() == name:
            return mapLayer