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
        """Ventana Principal debe recibir una instancia de GUI """
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
        self.wgtDetalles.setVisible(False)
        self.vlCodigo.insertWidget(0,self.widgetcodigo.getEditor())
        #Reordenamiento  y expancion
        self.spPrincipal.setSizes([50,900])#ni idea pero no tocar
        #colores x defecto
        self.colorBusqueda = QcolorTextEdit(self.eBusqueda)
    #Boludeces de instancias
        self.Padre = parent
        self.SM = self.Padre.newSnippetManager(None)

        self.lbEstado.setText('Se encontraron '+
                                self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())+
                                ' snippets')
    
    #carga las bds en el combo
        self.PasePorAca = False
        bds = self.SM.getBDNames()
        for item in bds:
            self.cbBD.addItem(item)
        
    #icon
        self.Padre.settrayIcon(self)
    #ShortCut
        self.__loadAppShortcuts()
        self.fullScreen = False
        
## Metods ##
############

    def __mostrar_snippet(self,lenguaje,titulo):
        snippet = self.SM.getSnippet(lenguaje,titulo)
        #con lo anterior busca en SM el codigo
        self.widgetcodigo.setFullCode(snippet.codigo,snippet.lenguaje)
        self.leTags.setText(snippet.tags)
        self.leTitulo.setText(snippet.titulo)
        self.leLenguaje.setText(snippet.lenguaje)
        self.txtDescripcion.setText('Descripcion: '+snippet.descripcion)
        self.lbFechaCreacion.setText('Creado: '+snippet.fechaCreacion)
        self.lbFechaModificacion.setText('Modificado: '+str(snippet.fechaModificacion))
        

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
        self.lbEstado.setText('Se encontraron '+
                            self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())+
                            ' snippets')
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
            actual.titulo + '\n' + actual.lenguaje,
            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

            if result == QtGui.QMessageBox.Yes:
                if self.SM.eliminarSnippet(actual):
                    QtGui.QMessageBox.information(self, "Eliminar snippet",
                    "Snippet eliminado.")
                else:
                    QtGui.QMessageBox.critical(self, "Eliminar snippet",
                    "Se produjo un error al intentar eliminar este snippet.")

    def __modificarSnippet(self):
        """ Ejecuta las instrucciones para modificar el snippet actual. """
        actual = self.SM.getSnippetActual()
        if actual is None:
            QtGui.QMessageBox.warning(self, "Modificar snippet",
        "Debes seleccionar un snippet para modificarlo.")
        else:
            pass           
            
    def __loadAppShortcuts(self):
        u""" Load shortcuts used in the application. """
        #Add Snippet Shortcut
        QtGui.QShortcut(QtGui.QKeySequence("F9"), self, self.on_btAgregarSnippet_clicked)
        QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self.__toogleFullScreen)

        
############
## Events ##
############

    def on_eBusqueda_textChanged(self,cadena):
        #campo de pruebas en la busqueda
        datos = self.SM.getLengsAndTitles(str(self.__convertir_a_unicode(cadena)))
        if datos:
            self.colorBusqueda.set_color_busqueda()
            self.lbEstado.setText('Se encontraron '+
                                self.mytreeview.insertarEnArbol(datos)+
                                ' snippets')
            self.tvLenguajes.expandAll()
        else:
            self.colorBusqueda.set_color_busqueda(False)
            self.mytreeview.model.clear()

    def on_tvLenguajes_selectedItem(self,indice,b):
        if indice.parent().row() != -1:
            lenguaje =  indice.parent().data().toString().toUtf8()#.encode('ascii','utf-8')
            titulo =  unicode(indice.data().toString().toUtf8(),'utf-8')
            self.__mostrar_snippet(unicode(lenguaje,'utf-8'),titulo)

    @QtCore.pyqtSlot()
    def on_btAgregarSnippet_clicked(self):
        print 'mostrando agregar...'
        self.hide()
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

    def __toogleFullScreen(self):
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()
        self.fullScreen = not self.fullScreen

    def __addKeytoBusqueda(self,cadena):
        u'''Soporte de atajos generico.Manipula los atajos
        en la barra de busqueda'''
        ubicacion = self.__convertir_a_unicode(self.eBusqueda.text)
        self.eBusqueda.setFocus()
        if ubicacion.find(cadena) == -1:
            if not len(ubicacion.strip()):
                self.eBusqueda.setText(cadena)
            else:
                self.eBusqueda.setText(ubicacion+u","+cadena)
            self.eBusqueda.setCursorPosition(self.__convertir_a_unicode(self.eBusqueda.text).find(cadena)+2)
        else:
            self.eBusqueda.setCursorPosition(ubicacion.find(cadena)+2)

    def destroyed(self):
        ''' Hace volar la ventana. '''
        #TODO: hacer que cierre todas las ventanas
        sys.exit(0)

def main():
    pass

if __name__ == "__main__":
    main()
