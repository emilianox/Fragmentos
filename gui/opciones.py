#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
#       Copyright 2011 Emiliano Fernandez <emilianohfernandez@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import os
from PyQt4 import QtCore, QtGui, uic

from pathtools import PathTools
from gui.images import icons_rc #@UnusedImport


class Opciones(QtGui.QMainWindow):
    """Clase que maneja las interacciones entre la interfaz grafica y
    la logica de las configuraciones del programa."""

    def __init__(self, parent, configs, dbutils):
        # carga la interfaz desded el archivo ui
        FILENAME = 'uis/wOpciones.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        self.setWindowIcon(QtGui.QIcon(':/toolbar/gear32.png'))
        
        # centra la ventana 
        self.__centerOnScreen()
        
        # instancias desde la clase fragmentos
        self.__Config = configs
        self.__DBU = dbutils
        self.__PT = PathTools()
        self.__Padre = parent
        
        # usado para saber si hay que refrescar el combo 
        # de bds de la interfaz principal, en caso
        # de que se haya agregado alguna
        self.__countBdsIsChanged = False
        # 
        self.__cargarValoresEnGUI()

        self.tabWidget.setCurrentIndex(0)
        
        self.cbBDsCargaInicio.setEnabled(False)
               
########################
## Metodos de Eventos ##
########################

    #~ 
    #~ BOTONES GENERALES
    #~ 
    
    @QtCore.pyqtSlot()
    def on_btAgregarBDReferencia_clicked(self):
        self.__agregarBDReferencia()            
        
    @QtCore.pyqtSlot()
    def on_btQuitarBDReferencia_clicked(self):
        
        pass
        
    @QtCore.pyqtSlot()
    def on_btAceptar_clicked(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_btAgregarBDDefault_clicked(self):
        self.__agregarBDDefault()        
    
    @QtCore.pyqtSlot()
    def on_btQuitarBDDefault_clicked(self):
        self.__quitarBDDefault()
        
    def closeEvent(self, event):    
        self.on_eNombreUsuario_editingFinished()
        
    #~ 
    #~ TAB: GENERALES
    #~ 
    
    @QtCore.pyqtSlot(bool)
    def on_cbxBuscarTags_clicked(self, valor):        
        # refleja el cambio en el CFG
        self.__Config.searchPresitionTags = int(valor)
            
    @QtCore.pyqtSlot(bool)   
    def on_cbxMaximizado_clicked(self, valor):
        
        # refleja el cambio en el CFG
        self.__Config.windowStateStartup = int(valor)
        
    @QtCore.pyqtSlot(bool)   
    def on_cbxExpandirArbol_clicked(self, valor):
        # refleja el cambio en el CFG
        self.__Config.expandTree = int(valor)
        
    def on_eNombreUsuario_editingFinished(self):
        # obtiene el valor actual
        nombre = unicode(self.eNombreUsuario.text(), 'utf-8')
        # lo refleja en el CFG
        self.__Config.userUploader = nombre
    
    #~ 
    #~ TAB: BASES DE DATOS
    #~ 
    
    
########################
## Metodos Auxiliares ##
########################
            
    def __centerOnScreen(self):
        u"""Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        
    def __toUnicode(self,myQstring):
        u""" Convierte a UTF8 el objeto QString recibido. """
        #~ print myQstring
        return unicode(myQstring.toUtf8(),'utf-8')

    def __cargarValoresEnGUI(self) :
        ''' Llama a los metodos que se encargan de reflejar los valores 
        actuales  de las configuraciones en la interfaz. '''
        
        # Tab: General
        
        self.__chequearOpcionesGenerales()
        self.__cargarNombreUsuario()
        
        # Tab: Bases de datos
        
        self.__setPathDefaultBDsInGUI()
        self.__cargarBDsDesdeDatabases()
        self.__cargarBDsDesdeCFG()
        self.__cargarComboBDsDefault()
        
    #~ 
    #~ TAB: GENERALES
    #~ 
    
    def __cargarNombreUsuario(self):
        ''' Recupera el valor para este campo desde el CFG y 
        lo muestra en la interfaz. '''
        self.eNombreUsuario.setText(
                self.__Config.userUploader)
    
    def __chequearOpcionesGenerales(self):
        
        self.cbxBuscarTags.setChecked(
            int(self.__Config.searchPresitionTags))
            
        self.cbxMaximizado.setChecked(
            int(self.__Config.windowStateStartup))
            
        self.cbxExpandirArbol.setChecked(
            int(self.__Config.expandTree))
    #~ 
    #~ TAB: CATALOGOS
    #~ 
    def __agregarBDDefault(self):
        dialog = QtGui.QFileDialog(self, 'Agregar catalogo')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Catalogo Fragmentos (*.db)')
        
        if dialog.exec_():
            filename = dialog.selectedFiles()[0] # convierte a unicode el string
            filename = unicode(filename, 'utf-8') # persiste la nueva refrencia en el cfg
            
            if self.__DBU.validarBD(filename):
                self.__DBU.agregarBDADefault(filename)
                self.__cargarBDsDesdeDatabases()
                
                # refresca el combo de la interfaz principal
                self.__Padre.refreshBdsInComboMainWindow()
            else:
                QtGui.QMessageBox.critical(self,"Agregar catalogo",
                "Este archivo no es un catalogo valido de Fragmentos.")
        
    def __agregarBDReferencia(self):
        dialog = QtGui.QFileDialog(self, 'Agregar referencia a catalogo')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Catalogo Fragmentos (*.db)')
        if dialog.exec_():
            filename = dialog.selectedFiles()[0] # convierte a unicode el string
            filename = unicode(filename, 'utf-8') # persiste la nueva refrencia en el cfg
            
            if self.__DBU.validarBD(filename):
                self.__agregarBDReferenciaInCFG(filename) # refresca la gui
                self.__cargarBDsDesdeCFG()  
                
                # refresca el combo de la interfaz principal
                self.__Padre.refreshBdsInComboMainWindow()
            else:
                QtGui.QMessageBox.critical(self,"Agregar referencia a catalogo",
                "Este archivo no es un catalogo valido de Fragmentos.")
            
    def __agregarBDReferenciaInCFG(self, pathCatalogo):
        ''' Agrega el nuevo catalogo seleccionado a en el archivo CFG'''

        # recupera el string guardado en el cfg
        referencias = self.__Config.referencesToBds
        # separa los paths
        referencias = referencias.split(',')
        # agrega el nuevo path a los existentes
        referencias.append(pathCatalogo)
        # vuelve a juntar los path en un solo string
        # y lo guarda nuevamente en el cfg
        self.__Config.referencesToBds = ','.join(referencias)
                
    def __cargarBDsDesdeDatabases(self):
        ''' Carga en la lista las bds existentes en el directorio 
        establecido por defecto. '''
        
        self.lstBdsDefault.clear()
        bds = self.__DBU.getBDsNamesDatabasesDir()
        if bds : 
            map(self.lstBdsDefault.addItem,bds)
        
    def __cargarBDsDesdeCFG(self):
        ''' '''
        self.lstBdsReferences.clear()
        bds = self.__Config.getDBsInCFGReferences()
        if bds : 
            map(self.lstBdsReferences.addItem,bds)
                
    def __cargarComboBDsDefault(self):
        ''' '''
        databases_dir = self.__DBU.getBDsNamesDatabasesDir()
        cfg_file = self.__Config.getDBsNamesCFGReferences()
        nombres = databases_dir + cfg_file
        map(self.cbBDsCargaInicio.addItem,nombres)
        
    def __quitarBDDefault(self):
        ''' '''
        if self.lstBdsDefault.currentRow() != -1 :
            pass
    
    def __quitarBDReferencia(self):
        ''' '''
        if self.lstBdsReferences.currentRow() != -1 :
            pass
            
    def __setPathDefaultBDsInGUI(self):
        ''' Obtiene la ruta del directorio por defecto y 
        lo muestra en el campo correspondiente en la interfaz. '''
        self.eDefaultDir.setText(
                        self.__PT.getPathDatabasesDir())
                    
#~ def main():
    #~ app = QtGui.QApplication(sys.argv)
    #~ m = Opciones()
    #~ m.show()
    #~ sys.exit(app.exec_())
#~ 
#~ 
#~ if __name__ == "__main__":
    #~ main()
