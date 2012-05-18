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
from PyQt4 import QtGui

class QcolorTextEdit:
    def __init__(self,TextEdit):
        #sacarle el color a textedit
        self.__txt = TextEdit
        self.__palette = self.__txt.palette()
        self.__defaultcolortext = self.__txt.palette().color(
                                    QtGui.QPalette.Active, QtGui.QPalette.Text).getRgb()[:-1]
        self.__defaultcolorbase = self.__txt.palette().color(
                                    QtGui.QPalette.Active, QtGui.QPalette.Base).getRgb()[:-1]
        #colores
        self.__blanco = QtGui.QColor(255, 255, 255)
        self.__rojito = QtGui.QColor(255, 102, 102)
        self.__defaulttext = QtGui.QColor(self.__defaultcolortext[0],self.__defaultcolortext[1],
                                        self.__defaultcolortext[2])
        self.__defaultbase = QtGui.QColor(self.__defaultcolorbase[0],self.__defaultcolorbase[1],
                                        self.__defaultcolorbase[2])

    def set_color_busqueda(self,estado=True):
        return True

#    def set_color_busquedaold(self,estado=True):
#        if estado:
#            textcolor = self.__defaulttext
#            basecolor = self.__defaultbase
#        else:
#            textcolor = self.__blanco
#            basecolor = self.__rojito
#
#        self.__palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text,textcolor)
#        self.__palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base,basecolor)
#        self.__txt.setPalette(self.__palette)
#
#        return True
#        #return confirmacion si cambio de color
