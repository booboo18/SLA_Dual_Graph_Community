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
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from PyQt4.QtCore import *
from qgis.core import *
import math
import community
import networkx as nx
from osgeo import ogr, osr

# analysis class
class dual_graph_community_analysis(QObject):

    # initialise class with self and iface
    def __init__(self,iface):
        #QObject.__init__(self)
        self.iface=iface
    def read_graph(self,layer):
        path = layer.dataProvider().dataSourceUri()
        print path
        if "|" in str(path):
            path = path[:path.rfind('|')]
        input = str(path)
        G = nx.read_shp(input)
        H = G.to_undirected()
        LG = nx.line_graph(H)
        return LG

    # community analysis function
    def Community_Analysis(self,LG):
        partition = community.best_partition(LG)
        nx.set_node_attributes(LG, '1_comm', partition)
        return LG

    def dendro_community(self,LG):
        dendro = community.generate_dendrogram(LG)
        length = len(dendro)
        i = 0
        SG = {}
        while i < length:
            SG[i] = community.partition_at_level(dendro, i)
            i = i + 1
        j = 0
        while j < length:
            name = 'louvain_part_' + str(j)
            nx.set_node_attributes(LG, name, SG[j])
            j = j + 1
        return LG

    # basic centrality analysis function
    def Centrality_Analysis(self,LG):
        closeness = nx.closeness_centrality(LG)
        nx.set_node_attributes(LG, '2_cc', closeness)
        betweenness = nx.betweenness_centrality(LG)
        nx.set_node_attributes(LG, '3_bc', betweenness)
        eigenvector = nx.eigenvector_centrality(LG)
        nx.set_node_attributes(LG, '4_ec', eigenvector)
        return LG

    
    def unfinished_blockmodel(self,LG):
        #http://networkx.readthedocs.io/en/latest/auto_examples/algorithms/plot_blockmodel.html#sphx-glr-auto-examples-algorithms-plot-blockmodel-py
        #https://networkx.github.io/documentation/networkx-1.10/examples/algorithms/blockmodel.html

        # this returns for each node the partition membership
        best = community.best_partition(LG)

        # this turns the partition into a dict of the subgraph
        v = {}
        for key, value in sorted(best.iteritems()):
            v.setdefault(value, []).append(key)

        #this returns the subgraph as a list of list
        partition = v.values()
        #this creates the blockmodel for the partition
        M = nx.blockmodel(LG, partition)
        #M.nodes(data=True)

        #create a node,edge for each partition to visualise

        #run centrality analysis on the reduced graph

    # add_comm_attributes
    def create_layer(self,LG):
        output = str(os.getcwd()) + '//' + "temp.shp"
        # output = "C:/Users/s.law/Desktop/SSx/urban_value/shp/Process3.shp"
        driver = ogr.GetDriverByName('ESRI Shapefile')
        datasource = driver.CreateDataSource(output)
        layer = datasource.CreateLayer('layerName', geom_type=ogr.wkbLineString)
        layer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        layer.CreateField(ogr.FieldDefn('1_comm', ogr.OFTInteger))
        layer.CreateField(ogr.FieldDefn('2_cc',ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn('3_bc',ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn('4_ec', ogr.OFTReal))
        featureIndex = 0
        defn = layer.GetLayerDefn()
        for i in LG.nodes_iter(data=True):
            # L.node[i]['louvain']=partition[i]
            myLine = ogr.Geometry(type=ogr.wkbLineString)
            myLine.AddPoint_2D(i[0][0][0], i[0][0][1])
            myLine.AddPoint_2D(i[0][1][0], i[0][1][1])
            feature = ogr.Feature(defn)
            feature.SetGeometry(myLine)
            feature.SetFID(featureIndex)
            feature.SetField('id', featureIndex)
            feature.SetField('1_comm', i[1].values()[0])
            feature.SetField('2_cc', i[1].values()[1])
            feature.SetField('3_bc', i[1].values()[2])
            feature.SetField('4_ec', i[1].values()[3])
            layer.CreateFeature(feature)
            featureIndex = featureIndex + 1
        datasource.Destroy()

        # finish
        return output


    # visualise layer
    def visualise_layer(self,output):
        #output = str(os.getcwd()) + '//' + "temp.shp"
        self.iface.addVectorLayer(output, 'temp_layer', 'ogr')
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