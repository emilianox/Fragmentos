#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Informática MEG <contacto@informaticameg.com>
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
from PyQt4 import QtGui, QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        """ """
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        menu.addAction("&Ocultar/&Mostrar",self.menuShowHide)
        menu.addSeparator()
        menu.addAction("B&uscar",self.menuSearch)
        menu.addAction("&Agregar Snippet",self.menuAdd)
        menu.addSeparator()
        menu.addAction("&Salir",self.menuExit)
        self.setContextMenu(menu)
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        QtCore.QObject.connect(self, QtCore.SIGNAL(traySignal), self.__icon_activated)

        self.__window_parent = parent

    def windowIsShowing(self):
        return self.__window_parent.isVisible ()

    def menuShowHide(self):
        '''menu show'''
        if self.windowIsShowing():
            self.__window_parent.hide()
        else:
            self.__window_parent.show()
            self.__window_parent.eBusqueda.setFocus()

    def menuSearch(self):
        '''menu show'''
        # establece el foco en la barra de busqueda
        self.__window_parent.eBusqueda.setFocus()
        # si la ventana esta oculta, la muestra
        if not self.windowIsShowing():
            self.__window_parent.show()           

    def menuAdd(self):
        '''menu show'''
        # abre la ventana de agregar snippet
        self.__window_parent.Padre.showAgregarSnippet()

    def menuExit(self):
        '''menu show'''
        sys.exit(0)

    def __icon_activated(self,reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.menuShowHide()

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    SystemTrayIcon(QtGui.QIcon("star.png"), w)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
