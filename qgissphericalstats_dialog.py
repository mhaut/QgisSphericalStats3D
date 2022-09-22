# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgissphericalstatsDialog
                                 A QGIS plugin
 qgissphericalstats
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Juan M Haut
        email                : juanmariohaut@unex.es
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

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets


from qgis.PyQt import QtCore, QtGui
import numpy as np
import pysphericalstats.draw as pySpDraw
import pysphericalstats.math as pySpMath
import pysphericalstats.fileIO as pySpFileIO
from matplotlib.backends.backend_qt5agg import FigureCanvas

from qgis.core import QgsProject



# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'qgissphericalstats_dialog_base.ui'))


class qgissphericalstatsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(qgissphericalstatsDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.sceneGrahics = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.sceneGrahics)
        pySpDraw.DPIEXPORT = 150
        #print(self.imageicono.geometry())
        self.imageicono.setPixmap(QtGui.QPixmap('./images/logo.png').scaled(202,191, QtCore.Qt.KeepAspectRatio))
        self.buttonload.clicked.connect(self.load_data)
        self.buttonmap.clicked.connect(self.load_data_maps)
        self.calculate.clicked.connect(self.exec_func)
        self.Files.toggled.connect(self.change_load_options)



    def show_message(self, typeSMS, info):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(typeSMS)
        msg.setInformativeText(info)
        msg.setWindowTitle(typeSMS + " pySpericalStudio")
        msg.exec_()

    def resizeEvent(self, event):
        bounds = self.sceneGrahics.itemsBoundingRect()
        #bounds.setWidth(bounds.width()*0.9)
        #bounds.setHeight(bounds.height()*0.9)
         #IgnoreAspectRatio, KeepAspectRatio, KeepAspectRatioByExpanding
        self.graphicsView.fitInView(bounds, QtCore.Qt.KeepAspectRatioByExpanding);

    def drawObject(self, objectReturn):
        if objectReturn != []:
            self.sceneGrahics.clear()
            self.graphicsView.items().clear()
            try:
                canvas = FigureCanvas(objectReturn)
                canvas.setGeometry(0, 0, self.graphicsView.width(), self.graphicsView.height())
                self.sceneGrahics.addWidget(canvas)
                #canvas = FigureCanvas(objectReturn)
                #self.sceneGrahics.addWidget(canvas)
            except: # its text
                self.sceneGrahics.addText(str(objectReturn), QtGui.QFont('Arial Black', 15, QtGui.QFont.Light))
            self.resizeEvent(None)
        else:
            self.showMessageInView("ERROR: No information wind in region")

    # cambiar este load data por el load 3d
    def load_data(self):
        print(self.imageicono.geometry())
        fpath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
            '../../datasets',"Image files (*.txt)")[0]
        if fpath:
            if self.type3D.isChecked() == False:
                self.show_message("ERROR", "select type")
            else:
                #try:
                    vectorsMatrix    = pySpFileIO.read_file(fpath)
                    self.data        = pySpFileIO.load_data(vectorsMatrix)
                    #print(self.data.shape)
                    #exit()
                    #self.modules     = pySpFileIO.getColumnAsArray(0, self.data)
                    #self.coordinates =  (pySpMath.getColumnAsArray(3, self.data),
                                        #pySpMath.getColumnAsArray(4, self.data),
                                        #pySpMath.getColumnAsArray(5, self.data))
                    self.modules     = self.data[:,0]
                    self.coordinates = np.array([self.data[:,3], self.data[:,4],self.data[:,5]]).T
                    #self.coordinates =  (pySpMath.getColumnAsArray(3, self.data),
                                        #pySpMath.getColumnAsArray(4, self.data),
                                        #pySpMath.getColumnAsArray(5, self.data))

                    fname = fpath.split("/")[-1]
                    #self.labelpath.setText(fname)
                    self.calculate.setEnabled(True)
                #except:
                    #self.show_message("ERROR", "invalid text format")


    def change_load_options(self):
        if self.Files.isChecked():
            self.type3D.setEnabled(True)
            self.buttonload.setEnabled(True)
            self.buttonmap.setEnabled(False)
            #self.Map.setEnabled(False)
            self.comboBoxSource1.setEnabled(False)
            self.comboBoxSource2.setEnabled(False)
        else:
            self.type3D.setEnabled(False)
            self.buttonload.setEnabled(False)
            self.buttonmap.setEnabled(True)
            #self.Map.setEnabled(False)
            self.comboBoxSource1.setEnabled(True)
            self.comboBoxSource2.setEnabled(True)
            layers = QgsProject.instance().mapLayers()
            layersName = [layers[key].name() for key in layers.keys()]
            self.comboBoxSource1.addItems(layersName)
            self.comboBoxSource2.addItems(layersName)

    
    def load_data_maps(self):
        import pysphericalstats.convert as pySpCconvert
        nameLs1 = self.comboBoxSource1.currentText()
        nameLs2 = self.comboBoxSource2.currentText()
        dataS1 = []; dataS2 = []
        for idlayer, layername in enumerate([nameLs1, nameLs2]):
            layer = QgsProject.instance().mapLayersByName(layername)[0]
            for feature in layer.getFeatures():
                x = feature.geometry().get().x()
                y = feature.geometry().get().y()
                z = feature.geometry().get().z()
                if idlayer == 0:
                    dataS1.append([x,y,z])
                else:
                    dataS2.append([x,y,z])
        dataS1 = np.array(dataS1)
        dataS2 = np.array(dataS2)
        
        vectors_matrix = np.hstack((dataS1, dataS2))
        axis_inc = np.zeros((vectors_matrix.shape[0], vectors_matrix.shape[1]//2))
        for i in range(3):
            axis_inc[:, i] = vectors_matrix[:, i+3] - vectors_matrix[:, i]
        polar_vectors = pySpCconvert.vectorsToPolar(axis_inc) # TODO: CAMBIADO DE calculatePolarFormVector
        rectangular_vectors = axis_inc

        self.data = np.zeros((len(polar_vectors), 12))
        for i, polar_element in enumerate(polar_vectors):
            self.data[i,:] = [pySpCconvert.calculate_vector_module(*vectors_matrix[i]),  # module
                        *polar_element[:2],                                            # colatitud, longitud
                        *rectangular_vectors[i],                                   # Ax, Ay, Az
                        *vectors_matrix[i]]                                        # x0, y0, z0, x1, y1, z1
        self.modules = self.data[:,0]
        self.coordinates = np.array([self.data[:,3], self.data[:,4],self.data[:,5]]).T
        self.calculate.setEnabled(True)

    # cada radiobuton
    def exec_func(self):
        if self.densityGraph.isChecked():
            self.drawdensityGraph() 
        elif self.angledistribution.isChecked():
            self.drawangledistribution() 
        elif self.vectorgraph.isChecked():
            self.drawvectorgraph() 
        elif self.modstats.isChecked():
            self.modulestats()
        elif self.angstats.isChecked():
            self.anglestats()

    def drawdensityGraph(self):
        figure = pySpDraw.draw_density_graph(self.data)
        self.drawObject(figure)

    def drawangledistribution(self):
        figure = pySpDraw.draw_module_angle_distrib(self.data)
        self.drawObject(figure)

    def drawvectorgraph(self):
        figure = pySpDraw.draw_vector_graph(self.data)
        self.drawObject(figure)

    def modulestats(self):
        figure = pySpMath.allmodulestatistics(self.modules)
        self.drawObject(figure)

    def anglestats(self):
        figure = pySpMath.allanglesstatistics(self.modules, self.coordinates)
        self.drawObject(figure)
