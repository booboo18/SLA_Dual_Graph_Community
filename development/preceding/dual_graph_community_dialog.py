# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Dual_Graph_CommunityDialog
                                 A QGIS plugin
 application of louvain method on the dual graph
                             -------------------
        begin                : 2017-08-09
        git sha              : $Format:%H$
        copyright            : (C) 2017 by UCL
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




    # add_comm_attributes
    def update_attributes(self,LG):
        output = str(os.getcwd())+'//'+"temp.shp"
        #output = "C:/Users/s.law/Desktop/SSx/urban_value/shp/Process3.shp"
        driver = ogr.GetDriverByName('ESRI Shapefile')
        datasource = driver.CreateDataSource(output)
        layer = datasource.CreateLayer('layerName', geom_type=ogr.wkbLineString)
        layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        layer.CreateField(ogr.FieldDefn('comm', ogr.OFTInteger))
        defn = layer.GetLayerDefn()
        featureIndex = 0

        # create features
        for i in LG.nodes_iter(data=True):
            # L.node[i]['louvain']=partition[i]
            myLine = ogr.Geometry(type=ogr.wkbLineString)
            myLine.AddPoint_2D(i[0][0][0], i[0][0][1])
            myLine.AddPoint_2D(i[0][1][0], i[0][1][1])
            feature = ogr.Feature(defn)
            feature.SetGeometry(myLine)
            feature.SetFID(featureIndex)
            feature.SetField('id', featureIndex)
            feature.SetField('comm', i[1].values()[0])
            layer.CreateFeature(feature)
            featureIndex = featureIndex + 1

        # finish
        return output

        datasource.Destroy()
        print 'finished'

'''
    # open layers
    def open_layer(self):
        shp='C:/Users/s.law/Desktop/SSx/urban_value/shp/Process3.shp'
        shp = str(os.getcwd()) + '//'+"temp.shp"
        self.iface.addVectorLayer(shp, 'temp_layer', 'ogr')
        self.iface.addVectorLayer(shp, 'temp_layer', 'ogr')


    # community analysis
    def Community_Analysis(self, layer):

        # layer = self.get_layer()
        path = layer.dataProvider().dataSourceUri()
        print path

        if "|" in str(path):
            path = path[:path.rfind('|')]
        print path
        input = str(path)
        # input = "C:/Users/s.law/Desktop/SSx/urban_value/shp/CrouchHill.shp"
        G = nx.read_shp(input)
        H = G.to_undirected()
        LG = nx.line_graph(H)
        partition = community.best_partition(LG)
        nx.set_node_attributes(LG, 'comm', partition)
        return LG

'''