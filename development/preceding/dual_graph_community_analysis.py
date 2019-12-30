# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GateTransformer
                                 A QGIS plugin
 This plugin performs basic transformation on a line in qgis.
                              -------------------
        begin                : 2016-02-29
        author               : Stephen Law
        copyright            : (C) 2016 by Space Syntax Limited
        email                : s.law@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from PyQt4.QtCore import *
from qgis.core import *
import math
import networkx as nx
import community

# analysis class
class dual_graph_community_analysis(QObject):

    # initialise class with self and iface
    def __init__(self,iface):
        #QObject.__init__(self)
        self.iface=iface

    # rotate_line_scripts
    def Community_Analysis(self,layer):
        #layer = self.get_layer()
        path = layer.dataProvider().dataSourceUri()
        print path

        if "|" in str(path):
            path = path[:path.rfind('|')]
        print path
        input = str(path)
        G = nx.read_shp(input)
        H = G.to_undirected()
        LG = nx.line_graph(H)
        partition = community.best_partition(LG)
        nx.set_node_attributes(LG, 'comm', partition)
        return LG

    def visualise_layer(self):
        shp = str(os.getcwd()) + '//' + "temp.shp"
        self.iface.addVectorLayer(shp, 'temp_layer', 'ogr')
        # this sets style
        layer = self.iface.activeLayer()
        plugin_path = os.path.dirname(__file__)
        #print plugin_path
        qml_path = plugin_path + "\community.qml"
        #print qml_path
        layer.loadNamedStyle(qml_path)
        #layer.commitChanges()
        layer.updateExtents()
        layer.triggerRepaint()
        self.iface.mapCanvas().refresh()