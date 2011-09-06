#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
#
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

import MainForm
from QTTips import TrayIcon
from PyQt4 import QtGui, QtCore
import sys

class GUI():
    
    def __init__(self, parent):
        self.fragmentos = parent
        self.SM = parent.SM

        app = QtGui.QApplication(sys.argv)
        
        ## Look and feel changed to CleanLooks
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        #~ QtGui.QApplication.setStyle("plastique")
        app.setPalette(QtGui.QApplication.style().standardPalette())
    
        self.window = MainForm.Main(self)
        # segun el estado de estado del valor <windowStateStartup>
        # se maximiza o no la ventana
        
        if int(self.fragmentos.ConfigsApp.windowStateStartup) : # si es = 0
            from PyQt4 import QtCore
            self.window.setWindowState(QtCore.Qt.WindowMaximized)
            
        # muestra la ventana
        self.window.show()
        sys.exit(app.exec_())

    def __convertPath(self, path):
        """Convierte el path a el específico de la plataforma (separador)"""
        import os
        if os.name == 'posix':
            return "/" + apply(os.path.join, tuple(path.split('/')))
        elif os.name == 'nt':
            return apply(os.path.join, tuple(path.split('/')))
            
    def refrescarArbolMainWindow(self):
        self.window.refrescarArbol()
        
    def setTrayIcon(self, mainforminstance):
        icon = QtGui.QIcon(self.__convertPath('gui/images/save.png'))
        self.__trayIcon = TrayIcon.SystemTrayIcon(icon, mainforminstance)
        self.__trayIcon.show()

    def newSnippetManager(self, pathDB):
        u""" Recrea una instancia de SnippetManager 
        a partir de la pathDB indicado."""
        self.SM = self.fragmentos.newSnippetManager(pathDB)
        #~ print 'nueva instancia de SM creada desde -GUI-'
        return self.SM

    def setSMInstance(self, newSM):
        u""" Establece la referencia de la nueva instancia creada. """
        self.SM = newSM

    def showAgregarSnippet(self):
        u""" """
        from agregarSnippet import agregarSnippet

        self.agregar = agregarSnippet(self, "Agregar Snippet")
        self.agregar.operacion = "agregar"
        # lee desde el cfg y carga el nombre del usuario actual
        self.agregar.eAutor.setText(self.fragmentos.ConfigsApp.userUploader)
        self.agregar.show()

    def showModificarSnippet(self, unSnippet):
        u""" """
        from agregarSnippet import agregarSnippet
        
        # instancia de agregarSnippet
        self.modificar = agregarSnippet(self, "Modificar Snippet")
        self.modificar.operacion = "modificar"
        
        # carga los valores del snippet en los campos
        self.modificar.eTitulo.setText(unSnippet.titulo)
        self.modificar.eDescripcion.setText(unSnippet.descripcion)
        self.modificar.eAutor.setText(unSnippet.uploader)
        self.modificar.eTags.setText(unSnippet.tags)
        #~ print 'holaaa: ',type(unSnippet.referencias),unSnippet.referencias
        if unSnippet.referencias == None: 
            unSnippet.referencias = ''
            
        self.modificar.eReferencias.setText(unSnippet.referencias)
        self.modificar.widgetcodigo.setCode(unSnippet.codigo)
        self.modificar.cbLenguajes.setCurrentIndex(
            self.modificar.cbLenguajes.findText(unSnippet.lenguaje))
        self.modificar.chkFavorito.setChecked(bool(unSnippet.favorito))
        self.modificar.show()
        
    def showOpciones(self):
        """ """     
        from opciones import Opciones
        self.opciones = Opciones(self.fragmentos.ConfigsApp ,self.fragmentos.BDU)
        self.opciones.show()
        
    def showAcercaDe(self):
        from acercade import AcercaDe
        acerca = AcercaDe()
        acerca.show()
        
def main():
    G = GUI()


if __name__ == '__main__':
    main()

