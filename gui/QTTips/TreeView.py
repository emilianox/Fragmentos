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


from PyQt4 import QtGui,QtCore
class TreeView:

    def __init__(self, treeview,metodo,conector):
        '''Buscar doc de esto'''
        self.__model = self.__crearmodelo()
        #~ self.__treeview = treeview
        treeview.setModel(self.__model)
        SelectionModel = QtGui.QItemSelectionModel( self.__model,treeview)
        treeview.setSelectionModel(SelectionModel)
        conector(SelectionModel, QtCore.SIGNAL(
            "currentChanged(const QModelIndex &, const QModelIndex &)"),
            metodo)
        self.__treeview = treeview


    def __getModel(self):
       return self.__model

    def __setModel(self, model = None):
       self.__model = model

    def __crearmodelo(self):
        model = QtGui.QStandardItemModel()
        return model

    def insertarEnArbol(self,listaparainsertar):
        #TODO:Limpiar arbol
        self.__model.clear()
        dicdenodos = {}
        for elemento in listaparainsertar:
            if not dicdenodos.has_key(elemento[0]):
                temp = self.__model.invisibleRootItem()
                dicdenodos[elemento[0]] = QtGui.QStandardItem(QtCore.QString(elemento[0]))
                temp.appendRow(dicdenodos[elemento[0]])
            item = QtGui.QStandardItem(QtCore.QString(elemento[1]))
            dicdenodos[elemento[0]].appendRow(item)


    model = property(fget = __getModel, fset = __setModel, doc = None)


def main():

    return 0

if __name__ == '__main__':
    main()

