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

class Opciones(QtGui.QMainWindow):

    """Ventana agregar Snippet."""

    def __init__(self, configs, dbutils):
        # carga la interfaz desded el archivo ui
        FILENAME = 'wOpciones.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        
        # centra la ventana 
        self.__centerOnScreen()
        
        # instancias desde la clase fragmentos
        self.__Config = configs
        self.__DBU = dbutils
        self.__PT = PathTools()
        
        # 
        self.__cargarValoresEnGUI()

        self.tabWidget.setCurrentIndex(0)
               
########################
## Metodos de Eventos ##
########################

    #~ 
    #~ BOTONES GENERALES
    #~ 
    
    @QtCore.pyqtSlot()
    def on_btAgregarBDReferencia_clicked(self):
        dialog = QtGui.QFileDialog(self, 'Agregar referencia a base de datos')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Fragmentos Databases (*.db)')
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
            print filename
        pass
        

    @QtCore.pyqtSlot()
    def on_btQuitarBDReferencia_clicked(self):
        pass
        
    @QtCore.pyqtSlot()
    def on_btAceptar_clicked(self):
        pass
        

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
            
    #~ 
    #~ TAB: BASES DE DATOS
    #~ 
    
    def __cargarBDsDesdeDatabases(self):
        ''' Carga en la lista las bds existentes en el directorio 
        establecido por defecto. '''
        bds = self.__DBU.getBDsNamesDatabasesDir()
        for bd in bds:
            self.lstBdsDefault.addItem(bd)
        
    def __cargarBDsDesdeCFG(self):
        ''' '''
        bds = self.__Config.getDBsInCFGReferences()
        if bds :
            for bd in bds:
                self.lstBdsReferences.addItem(bd)
        
    def __cargarComboBDsDefault(self):
        ''' '''
        databases_dir = self.__DBU.getBDsNamesDatabasesDir()
        cfg_file = self.__Config.getDBsNamesCFGReferences()
        nombres = databases_dir + cfg_file
        for nombre in nombres:
            self.cbBDsCargaInicio.addItem(nombre)
        
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
