#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
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

from snippetmanager import SnippetManager
from gtktips import Combobox
import gtk

class GUI:
    
    def __init__(self):
        self.SM = SnippetManager()
        self.Combo = Combobox()
        pass

    def crearArbol(self,caja,title):
        tree_lenguajes = gtk.TreeStore(str)
        caja.set_model(tree_lenguajes)
        column = gtk.TreeViewColumn(title, gtk.CellRendererText() , text=0)
        column.set_resizable(True)
        #column.set_sort_column_id(self.ct)
        caja.append_column(column)
        return caja, tree_lenguajes

    def cargarSnippetsEnArbol(self,tree_lenguajes):
        ''' Carga los snippets por sus respectivos lenguajes un el arbol.'''
        tree_lenguajes.clear()
        dicdeleng = {}
        listaparainsertar = self.SM.getLengsAndTitlesFromBD()
        for snippet in listaparainsertar:
            if not dicdeleng.has_key(snippet[0]):
                dicdeleng[snippet[0]] = tree_lenguajes.append(None,[snippet[0]])
            tree_lenguajes.append(dicdeleng[snippet[0]],[snippet[1]])

    def cargarLenguajesEnCombo(self,cb):
        ''' Obtiene los lenguajes de la bd y los agrega a un combo.'''
        lenguajes = self.SM.getLenguajesFromBD()
        self.Combo.setCombobox(cb,lenguajes)
        pass

    def cargarBDsEnCombo(self,cb):
        ''' Obtiene los nombres de las bds y los agrega a un combo.'''
        bds = self.SM.getBDNames()
        self.Combo.setCombobox(cb,bds)
    
    def obtenerSnippet(self,lenguaje,titulo):
        return self.SM.getSnippetFromBD(lenguaje,titulo)
