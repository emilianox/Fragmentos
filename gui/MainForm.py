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

        self.__refrescarArbol()
        
        self.lbEstado.setText(
            'Se encontraron ' + str(self.SM.getSnippetsCount()) + ' snippets')

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

     #MenuPrincipal
        self.__createMenu()
        
############
## Metods ##
############
        
    def __addKeytoBusqueda(self,cadena):
        u"""Soporte de atajos generico.Manipula los atajos
        en la barra de busqueda"""
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
    
    def __agregarSnippet(self):
        print 'mostrando agregar...'
        #~ self.hide()
        self.Padre.showAgregarSnippet()
        self._refrescarArbol()
    
    def __convertir_a_unicode(self,myQstring):
        return str(myQstring.toUtf8())

    def __cargarBDSeleccionada(self,indice):
        """ Al seleccionar otra base de datos desde el combo,
        reflejar los cambios en la interfaz. """
        #obtiene la ruta de la bd segun el indice
        rutaNueva = self.SM.getPathDB(indice)
        #le pide a GUI que vuelva a crear la instancia
        self.SM = self.Padre.newSnippetManager(rutaNueva)
        #carga los snippets en el arbol
        self.__refrescarArbol()
        
        self.lbEstado.setText(
            'Se encontraron ' + str(self.SM.getSnippetsCount()) + ' snippets')

    def __centerOnScreen (self):
        """Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
                  
    def __createMenu(self):
        """Crea el main menu"""
        menu = QtGui.QMenu(self.btMenu)
        snippet = menu.addAction("Snippet")
        database= menu.addAction("Database")
        busqueda = menu.addAction("Busqueda")
        menu.addSeparator()
        menu.addAction("Opciones")
        menu.addAction("Ayuda")
        menu.addSeparator()
        menu.addAction("Acerca de..")


        menusnippet = QtGui.QMenu()
        menusnippet.addAction("Agregar",self.__agregarSnippet,QtGui.QKeySequence("F9"))
        menusnippet.addAction("Editar")
        menusnippet.addAction("Eliminar", self.__eliminarSnippet)
        snippet.setMenu(menusnippet)
        
        menudatabase = QtGui.QMenu()
        menudatabase.addAction("Nueva")
        menudatabase.addAction("Eliminar")
        database.setMenu(menudatabase)

        menubusqueda = QtGui.QMenu()
        menubusqueda.addAction("'t=' por Titulo")
        menubusqueda.addAction("'g=' por Tags")
        menubusqueda.addAction("'l=' por Lenguaje")
        busqueda.setMenu(menubusqueda)
        
        self.btMenu.setMenu(menu)
        #        .showMenu (self)

    def __eliminarSnippet(self):
        """Ejecuta las instrucciones para eliminar el snippet actual."""
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

        
    def __loadAppShortcuts(self):
        u""" Load shortcuts used in the application. """
        #Add Snippet Shortcut
        QtGui.QShortcut(QtGui.QKeySequence("F9"), self, self.on_btAgregarSnippet_clicked)
        QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self.__toogleFullScreen)


    
    def __modificarSnippet(self):
        """ Ejecuta las instrucciones para modificar el snippet actual. """
        actual = self.SM.getSnippetActual()
        if actual is None:
            QtGui.QMessageBox.warning(self, "Modificar snippet",
        "Debes seleccionar un snippet para modificarlo.")
        else:
            self.Padre.showModificarSnippet(actual)
            
    def __mostrar_snippet(self,lenguaje,titulo):
        snippet = self.SM.getSnippet(lenguaje,titulo)
        #con lo anterior busca en SM el codigo
        self.widgetcodigo.setFullCode(snippet.codigo,snippet.lenguaje)
        #carga en los campos los datos del snippet
        self.leTags.setText(snippet.tags)
        self.leTitulo.setText(snippet.titulo)
        self.leLenguaje.setText(snippet.lenguaje)
        self.txtDescripcion.setText('Descripcion: '+snippet.descripcion)
        self.lbFechaCreacion.setText('Creado: '+snippet.fechaCreacion)
        if not snippet.fechaModificacion is None:
            #si existe una fecha de modificado
            self.lbFechaModificacion.setVisible(True)
            self.lbFechaModificacion.setText('Modificado: '+str(snippet.fechaModificacion))
        else:
            #oculta el label
            self.lbFechaModificacion.setVisible(False)
        #si es favorito, cambia el estado del boton
        if snippet.favorito == "0":
            self.btPonerComoFavorito.setChecked(False)
        elif snippet.favorito == "1":
            self.btPonerComoFavorito.setChecked(True)
    
    def __ponerComoFavorito(self):
        
        #obtiene la instancia actual del snippet
        snippetActual = self.SM.getSnippetActual()
        #establece el nuevo valor
        if not snippetActual is None:
            #~ print str(int(self.btPonerComoFavorito.isChecked()))
            #refleja este cambio en los datos del snippet
            snippetActual.favorito = str(int(self.btPonerComoFavorito.isChecked()))
            #establece el nuevo estado del snippet
            self.SM.setSnippetActual(snippetActual)
            self.lbEstado.setText("Establecido como favorito.")
        else:
            #no permite que el boton sea chequeado
            self.btPonerComoFavorito.setChecked(False)
        
    def __refrescarArbol(self):
        """ A partir de la instancia actual de SM, 
        refresca el arbol cargando nuevamente los snippets. """
        
        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())
        
    def __toogleFullScreen(self):
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()
        self.fullScreen = not self.fullScreen

    def destroyed(self):
        ''' Hace volar la ventana. '''
        #TODO: hacer que cierre todas las ventanas
        sys.exit(0)
    
############
## Events ##
############

    ###############
    ### BOTONES ###
    ###############
    
    @QtCore.pyqtSlot()
    def on_btAgregarSnippet_clicked(self):
       self.__agregarSnippet()

    @QtCore.pyqtSlot()
    def on_btCopiarAlPortapapeles_clicked(self):
        #~ self.__eliminarSnippet()
        self.__modificarSnippet()
    
    @QtCore.pyqtSlot()
    def on_btBuscarEnFavoritos_clicked(self):
        #carga en el arbol los snippets favoritos

        if self.btBuscarEnFavoritos.isChecked():
            #obtiene solo los favoritos
            datos = self.SM.getLengsAndTitles("s=1",True)
        else:
            datos = self.SM.getLengsAndTitles()
        #carga los snippets en el arbol
        self.mytreeview.insertarEnArbol(datos)

    @QtCore.pyqtSlot()
    def on_btPonerComoFavorito_clicked(self):
        self.__ponerComoFavorito()
        
        
    ###############
    ### ENTRYES ###
    ###############
    
    def on_eBusqueda_textChanged(self,cadena):
        #campo de pruebas en la busqueda
        datos = self.SM.getLengsAndTitles(
            str(self.__convertir_a_unicode(cadena)),
                self.btBuscarEnFavoritos.isChecked())
        if datos:
            self.colorBusqueda.set_color_busqueda()
            self.mytreeview.insertarEnArbol(datos)
            #~ self.lbEstado.setText('Se encontraron '+ str(len(datos)),' snippets')
            self.tvLenguajes.expandAll()
        else:
            self.colorBusqueda.set_color_busqueda(False)
            self.mytreeview.model.clear()

    ################
    ### TREEVIEW ###
    ################
    
    def on_tvLenguajes_selectedItem(self,indice,b):
        if indice.parent().row() != -1:
            lenguaje =  indice.parent().data().toString().toUtf8()#.encode('ascii','utf-8')
            titulo =  unicode(indice.data().toString().toUtf8(),'utf-8')
            self.__mostrar_snippet(unicode(lenguaje,'utf-8'),titulo)

    
    ################
    ### COMBOBOX ###
    ################
    
    @QtCore.pyqtSlot(int)
    def on_cbBD_currentIndexChanged(self,index):
        if self.PasePorAca:
            self.__cargarBDSeleccionada(self.cbBD.currentIndex())
        else:
            self.PasePorAca = True
        
######################
## Metodos de clase ##
######################

    
        
def main():
    pass

if __name__ == "__main__":
    main()
