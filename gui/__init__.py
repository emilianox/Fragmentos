#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import sys
import MainForm
from QTTips import TrayIcon
from PyQt4 import QtGui, QtCore
from pathtools import PathTools
try:
    import dbus
    import dbus.service as servicio
    from dbus.mainloop.qt import DBusQtMainLoop
    from dbus.service import Object as DObject
except ImportError:
    from estafador import Vacia as DObject
    import estafador as servicio


class GUI(DObject):
    ''' Clase encargada de administrar y gestionar todas las ventanas
    y operaciones, entre la interfaz gráfica y la lógica de la aplicación.'''

    def __init__(self, parent):
        self.fragmentos = parent
        self.SM = parent.SM
        self.trayIcon = None

        app = QtGui.QApplication(sys.argv)
        self.clipboard = app.clipboard()

#------------------ Look and feel changed to CleanLooks-----------------------#
        #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        #~ QtGui.QApplication.setStyle("plastique")
        app.setPalette(QtGui.QApplication.style().standardPalette())
#------------------ DBus -----------------------#
        try:
            mainloop = DBusQtMainLoop(set_as_default=True) #@UnusedVariable
            bus_name = dbus.service.BusName('ar.fragmentos.service', bus=dbus.SessionBus())
            dbus.service.Object.__init__(self,bus_name, '/ar/fragmentos/service')
        except Exception:
            print "hay un error en dbus!"


#------------------------------------------------------------------------------
        self.window = MainForm.Main(self)
#-----------------------------------------------------------------------------#
        # segun el estado de estado del valor <windowStateStartup>
#----------se maximiza o no la ventana----------------------------------------#
        windowStateCFG = self.fragmentos.ConfigsApp.windowStateStartup
        if not windowStateCFG is None and \
            int(windowStateCFG) == 1: # si es = 1
            self.window.setWindowState(QtCore.Qt.WindowMaximized)
#-----------------------------------------------------------------------------#
        # muestra la ventana
        self.window.show()
        sys.exit(app.exec_())

    def refreshTreeMainWindow(self):
        self.window.refreshTree()

    def refreshBdsInComboMainWindow(self):
        self.window.loadBDsInCombo()

    def setTrayIcon(self, mainforminstance):
        icon = QtGui.QIcon(':/icons/logo.png')
        self.trayIcon = TrayIcon.SystemTrayIcon(icon, mainforminstance)
        self.trayIcon.show()

    @servicio.method('ar.fragmentos.service')
    def showAgregarSnippet(self):
        u""" """
        from agregarSnippet import agregarSnippet

        self.agregar = agregarSnippet(self, "Agregar Snippet")
        self.agregar.operacion = "agregar"
        # lee desde el cfg y carga el nombre del usuario actual
        self.agregar.eAutor.setText(self.fragmentos.ConfigsApp.userUploader)
        self.agregar.show()

    @servicio.method('ar.fragmentos.service')
    def showBuscarSnippet(self):
        if self.window.isVisible():
            self.window.hide()
        else:
            self.window.show()
            self.window.__centerOnScreen()
            self.window.eBusqueda.setFocus()




    def showModificarSnippet(self, unSnippet):
        u""" """
        from agregarSnippet import agregarSnippet

        # instancia de agregarSnippet
        self.modificar = agregarSnippet(self, "Modificar Snippet")
        self.modificar.operacion = "modificar"

        # carga los valores del snippet en los campos
        self.modificar.eTitulo.setText(unSnippet.titulo)
        self.modificar.eDescripcion.setText(unSnippet.descripcion)
        #TODO:PARCHEEEEEEEEEEEEEEEEEE!!!!!
        if unSnippet.uploader != None:
            self.modificar.eAutor.setText(unSnippet.uploader)
        self.modificar.eTags.setText(unSnippet.tags)
        #~ print 'holaaa: ',type(unSnippet.referencias),unSnippet.referencias
        #TODO:PARCHEEEEEEEEEEEEEEEEEE!!!!!
        if unSnippet.referencias != None:
            self.modificar.eReferencias.setText(unSnippet.referencias)
        self.modificar.widgetcodigo.setCode(unSnippet.codigo)
        self.modificar.cbLenguajes.setCurrentIndex(
            self.modificar.cbLenguajes.findText(unSnippet.lenguaje))
        self.modificar.chkFavorito.setChecked(bool(unSnippet.favorito))
        self.modificar.show()

    def showOpciones(self):
        """ """
        from opciones import Opciones
        self.opciones = Opciones(self,self.fragmentos.ConfigsApp ,self.fragmentos.BDU)
        self.opciones.show()

    def showAcercaDe(self):
        """ """
        from acercade import AcercaDe
        self.acerca = AcercaDe()
        self.acerca.show()

def main():
    GUI()


if __name__ == '__main__':
    main()

