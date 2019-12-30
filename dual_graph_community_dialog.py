# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Dual_Graph_Community_Analysis
                                 A QGIS plugin
 This plugin applies the louvain method on the dual of a line network in qgis.
                              -------------------
        begin                : 2017-08-23
        author               : Stephen Law
        copyright            : Stephen Law (C) 2017
        email                : stephenlawdesign@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#notes - to create temp layer in QGIS
#https://gis.stackexchange.com/questions/30261/how-to-create-a-new-empty-vector-layer-programmatically

import os
from PyQt4 import QtGui, uic
import os.path
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#import external library
import community
import networkx as nx
from osgeo import ogr, osr

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dual_graph_community_dialog_base.ui'))


class Dual_Graph_CommunityDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Dual_Graph_CommunityDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        # define globals
        #self.iface = iface
        #self.canvas = self.iface.mapCanvas()

    # get layer - retrieving the value of the current selected layer
    def get_layer(self):
        index = self.layer_comboBox.currentIndex()
        layer = self.layer_comboBox.itemData(index)
        return layer

    # update layer - fill combo with layer lists
    def update_layer(self, layer_objects):
        for layer in layer_objects:
            self.layer_comboBox.addItem(layer[0], layer[1])

