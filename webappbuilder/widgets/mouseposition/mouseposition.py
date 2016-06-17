from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json

class MousePosition(WebAppWidget):

    _parameters = {"projection": "EPSG:4326",
                   "coordinateFormat": "ol.coordinate.createStringXY(4)",
                   "undefinedHTML": "&nbsp;"}

    def write(self, appdef, folder, app, progress):
        projection = self._parameters["projection"]
        epsg = projection.split(":")[-1]
        if epsg not in ["3857", "4326"]:
            app.scripts.append('<script src="./proj4.js"></script>')
            app.scripts.append('<script src="http://epsg.io/%s.js"></script>' % epsg)
        coord = str(self._parameters["coordinateFormat"])
        s = json.dumps(self._parameters)
        s = s.replace('"%s"' % coord, coord)
        app.ol3controls.append("new ol.control.MousePosition(%s)" % s)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "mouse-position.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "mouse-position.png")

    def description(self):
        return "Mouse position"
