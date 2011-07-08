#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import os,sys
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt
import fragmentos_rc #Importo los iconos

from QTTips.Scintilla import Scintilla
from QTTips.TreeView import TreeView
from QTTips.QcolorTextEdit import QcolorTextEdit


class Main(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    def __init__(self,parent):
    #Boludeces de instancias
        self.SM = parent.SM
        self.Padre = parent
    #Cargar archivo ui
        FILENAME = 'MainForm.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
    #Treeview agregado
        self.mytreeview = TreeView(self.tvLenguajes,self.on_tvLenguajes_selectedItem,self.connect)
        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())
    #Detalles de armado interfaz
        #Widget codigo
        self.widgetcodigo = Scintilla()
        self.spPrincipal.addWidget(self.widgetcodigo.getEditor())
        #Reordenamiento  y expancion
        self.spPrincipal.setSizes([50,900])#ni idea pero no tocar
        #colores x defecto
        self.colorBusqueda = QcolorTextEdit(self.eBusqueda)
    #carga las bds en el combo
        bds = self.SM.getBDNames()
        for item in bds:
            self.cbBD.addItem(item)

        #self.mmm.setMenu(self.menuHello)

############
## Metods ##
############
    def mostrar_snippet(self,lenguaje,titulo):
        snippet = self.SM.getSnippet(lenguaje,titulo)
        #con lo anterior busca en SM el codigo
        self.widgetcodigo.setFullCode(snippet.getCodigo(),snippet.getLenguaje())

    def __convertir_a_unicode(self,myQstring):
        return str(myQstring.toUtf8())

    def __cargarBDSeleccionada(self,indice):
        ''' Al seleccionar otra base de datos desde el combo,
        reflejar los cambios en la interfaz. '''
        #obtiene la ruta de la bd segun el indice
        rutaNueva = self.SM.getPathDB(indice)
        #le pide a GUI que vuelva a crear la instancia
        self.SM = self.Padre.newSnippetManager(rutaNueva)
        #carga los snippets en el arbol
        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())

############
## Events ##
############
    def on_eBusqueda_textChanged(self,cadena):
        #campo de pruebas en la busqueda
        datos = self.SM.getLengsAndTitles(str(self.__convertir_a_unicode(cadena)))
        if datos != []:
            self.colorBusqueda.set_color_busqueda()
            self.mytreeview.insertarEnArbol(datos)
            self.tvLenguajes.expandAll()
        else:
            self.colorBusqueda.set_color_busqueda(False)
            self.mytreeview.model.clear()
            self.tvLenguajes

    def on_tvLenguajes_selectedItem(self,indice,b):
        #~ print indice.row()
        if indice.parent().row() != -1:
            lenguaje =  indice.parent().data().toString().toUtf8()#.encode('ascii','utf-8')
            titulo =  unicode(indice.data().toString().toUtf8(),'utf-8')
            self.mostrar_snippet(unicode(lenguaje,'utf-8'),titulo)

    @QtCore.pyqtSlot()
    def on_btAgregarSnippet_clicked(self):
        print 'mostrando agregar...'
        from agregarSnippet import agregarSnippet
        self.agregar = agregarSnippet()
        self.agregar.show()

    @QtCore.pyqtSlot(int)
    def on_cbBD_currentIndexChanged(self,index):
        #~ print 'currentIndexChanged ha cambiado...',index#,type(indice)
        self.__cargarBDSeleccionada(self.cbBD.currentIndex())


def main():
    pass

if __name__ == "__main__":
    main()
