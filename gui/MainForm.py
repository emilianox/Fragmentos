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

    #Cargar archivo ui
        FILENAME = 'MainForm.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
    #conectar salir
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.destroyed)
    #Treeview agregado
        self.mytreeview = TreeView(self.tvLenguajes,self.on_tvLenguajes_selectedItem,self.connect)
    #Detalles de armado interfaz
        #Widget codigo
        self.widgetcodigo = Scintilla()
        self.spPrincipal.addWidget(self.widgetcodigo.getEditor())
        #Reordenamiento  y expancion
        self.spPrincipal.setSizes([50,900])#ni idea pero no tocar
        #colores x defecto
        self.colorBusqueda = QcolorTextEdit(self.eBusqueda)
    #Boludeces de instancias
        self.Padre = parent
        self.SM = self.Padre.newSnippetManager(None)


        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())
    #carga las bds en el combo
        self.PasePorAca = False
        bds = self.SM.getBDNames()
        for item in bds:
            print item
            self.cbBD.addItem(item)
        #self.mmm.setMenu(self.menuHello)

    #icon
        self.Padre.settrayIcon(self)
############
## Metods ##
############

    def __mostrar_snippet(self,lenguaje,titulo):
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

    def __centerOnScreen (self):
        '''Centers the window on the screen.'''
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __eliminarSnippet(self):
        ''' Ejecuta las instrucciones para eliminar el snippet actual. '''
        actual = self.SM.getSnippetActual()
        if actual is None:
            QtGui.QMessageBox.warning(self, "Eliminar snippet",
        "Debes seleccionar un snippet para eliminarlo.")
        else:
            result = QtGui.QMessageBox.warning(self, "Eliminar snippet",
            "Esta seguro que desea eliminar este snippet?.\n\n" + \
            actual.getTitulo() + '\n' + actual.getLenguaje(),
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:
                if self.SM.eliminarSnippet(actual):
                    QtGui.QMessageBox.information(self, "Eliminar snippet",
                    "Snippet eliminado.")
                else:
                    QtGui.QMessageBox.critical(self, "Eliminar snippet",
                    "Se produjo un error al intentar eliminar este snippet.")

############
## Events ##
############
    def on_eBusqueda_textChanged(self,cadena):
        #campo de pruebas en la busqueda
        datos = self.SM.getLengsAndTitles(str(self.__convertir_a_unicode(cadena)))
        if datos:
            self.colorBusqueda.set_color_busqueda()
            self.mytreeview.insertarEnArbol(datos)
            self.tvLenguajes.expandAll()
        else:
            self.colorBusqueda.set_color_busqueda(False)
            self.mytreeview.model.clear()

    def on_tvLenguajes_selectedItem(self,indice,b):
        #~ print indice.row()
        if indice.parent().row() != -1:
            lenguaje =  indice.parent().data().toString().toUtf8()#.encode('ascii','utf-8')
            titulo =  unicode(indice.data().toString().toUtf8(),'utf-8')
            self.__mostrar_snippet(unicode(lenguaje,'utf-8'),titulo)

    @QtCore.pyqtSlot()
    def on_btAgregarSnippet_clicked(self):
        print 'mostrando agregar...'
        self.Padre.showAgregarSnippet()

    @QtCore.pyqtSlot()
    def on_btCopiarAlPortapapeles_clicked(self):

        self.__eliminarSnippet()


    @QtCore.pyqtSlot(int)
    def on_cbBD_currentIndexChanged(self,index):
        if self.PasePorAca:
            self.__cargarBDSeleccionada(self.cbBD.currentIndex())
        else:
            self.PasePorAca = True

    #~ #@QtCore.pyqtSlot()
    def destroyed(self):
        ''' Hace volar la ventana. '''
        #TODO: hacer que cierre todas las ventanas
        sys.exit(0)

def main():
    pass

if __name__ == "__main__":
    main()
