# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Dual_Graph_Community
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox, QProgressBar,QComboBox
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from dual_graph_community_dialog import Dual_Graph_CommunityDialog
import os.path
from qgis.core import *
import dual_graph_community_analysis

#import external library
import community
import networkx as nx
from osgeo import ogr, osr


class Dual_Graph_Community:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # transformer analysis class initialisation
        self.dual_graph_community_analysis = dual_graph_community_analysis.dual_graph_community_analysis(self.iface)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Dual_Graph_Community_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference *creates new dialog object runs dialog __init__
        # click pushButtons
        self.dlg = Dual_Graph_CommunityDialog()






        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Street_Local_Area')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Dual_Graph_Community')
        self.toolbar.setObjectName(u'Dual_Graph_Community')



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Dual_Graph_Community', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = Dual_Graph_CommunityDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Dual_Graph_Community/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Street_Local_Area'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()

        ###### YOUR OWN CODE ######
        # put current layers into comboBox
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_objects = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Line:
                layer_objects.append((layer.name(), layer))
        self.dlg.update_layer(layer_objects)


        # click pushButtons
        self.dlg.pushButton.clicked.connect(self.run_method)
        self.dlg.close_button.clicked.connect(self.close_method)

    def run_method(self):
        layer = self.dlg.get_layer()
        #LG=self.dlg.Community_Analysis(layer)
        LG=self.dual_graph_community_analysis.Community_Analysis(layer)
        self.dlg.update_attributes(LG)
        self.dual_graph_community_analysis.visualise_layer()
        #self.open_layer()
        self.dlg.close()

    def close_method(self):
        self.dlg.close()





'''
    def open_layer(self):
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

    def Community_Analysis(self):

        layer = self.dlg.get_layer()
        path = layer.dataProvider().dataSourceUri()
        print path

        if "|" in str(path):
            path = path[:path.rfind('|')]
        print path
        input=str(path)
        #input = "C:/Users/s.law/Desktop/SSx/urban_value/shp/CrouchHill.shp"
        G = nx.read_shp(input)
        H = G.to_undirected()
        LG = nx.line_graph(H)
        partition = community.best_partition(LG)
        nx.set_node_attributes(LG, 'comm', partition)
        return LG

    def add_attributes(self,LG):

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

            # layer.SetFeature(i)

        # finish
        datasource.Destroy()
        print 'finished'

'''




