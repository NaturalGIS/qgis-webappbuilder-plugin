# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from __future__ import absolute_import
from builtins import range
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem
from .treesettingsitem import TreeSettingItem


class ParametersEditorDialog(QDialog):

    def __init__(self, params, parent = None):
        super(ParametersEditorDialog, self).__init__(parent)

        self.params = params

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                                Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle('Edit control parameters')

        layout = QVBoxLayout()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.tree = QTreeWidget()
        layout.addWidget(self.tree)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.mainItem = QTreeWidgetItem()
        self.mainItem.setText(0, "Parameters")
        for name, value in params.items():
            subitem = TreeSettingItem(self.mainItem, self.tree, name, value)
            self.mainItem.addChild(subitem)
        self.tree.addTopLevelItem(self.mainItem)

        #self.mainItem.sortChildren(0,QtCore.Qt.AscendingOrder)
        self.tree.expandAll()
        self.tree.headerItem().setText(0, "Parameter")
        self.tree.headerItem().setText(1, "Value")
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def okPressed(self):
        for i in range(self.mainItem.childCount()):
            item = self.mainItem.child(i)
            if isinstance(self.params[item.name], tuple):
                self.params[item.name] = (item.value(), self.params[item.name][1])
            else:
                self.params[item.name] = item.value()
        self.close()

    def cancelPressed(self):
        self.close()
