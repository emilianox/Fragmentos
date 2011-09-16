#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import os,sys
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt
#Importo los iconos
import fragmentos_rc  #@UnusedImport
import icons_rc #@UnusedImport @UnresolvedImport

from QTTips.Scintilla import Scintilla
from QTTips.TreeView import TreeView
from QTTips.QcolorTextEdit import QcolorTextEdit


class Main(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    
    def __init__(self,parent):
        """ Ventana Principal debe recibir una instancia de GUI """
        FILENAME = 'MainForm.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        #TODO:
        self.setWindowIcon(QtGui.QIcon(':/icons/logo.png'))
        # centra la ventana en la pantalla
        self.__centerOnScreen()

        # conectar salir
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.destroyed)

        # agrega y crea el Treeview
        #TODO:
        self.mytreeview = TreeView(self.tvLenguajes,self.on_tvLenguajes_selectedItem,
                                   self.connect,iconSub=QtGui.QIcon(':/toolbar/linedpaper32.png'),
                                                iconRoot=QtGui.QIcon(':/toolbar/lang.png'))

        # agrega el Widget de codigo
        self.widgetcodigo = Scintilla()
        self.wgtDetalles.setVisible(False)
        self.vlCodigo.insertWidget(0,self.widgetcodigo.getEditor())

        # Reordenamiento y expancion del separador tree-widgetcodigo
        self.spPrincipal.setSizes([50,900])#ni idea pero no tocar

        # colores x defecto
        self.colorBusqueda = QcolorTextEdit(self.eBusqueda)

        # Instancia y variables usadas
        self.Padre = parent # esto es GUI
        self.SM = parent.SM # esto es GUI.SM
        self.PasePorAca = False
        self.fullScreen = False
        self.historialSnippets = [[],0]

        # establece el trayicon
        self.Padre.setTrayIcon(self)        
        
        self.refreshTree()

        # carga las bds en el combo
        self.__loadBDsInCombo()

        # carga los ShortCuts de la app
        self.__loadAppShortcuts()

        # crea el MenuPrincipal
        self.__createMenu()

        #~ self.btSptAnterior.setEnabled(False)
        #~ self.btSptSiguiente.setEnabled(False)



######################
## Metodos de clase ##
######################

    def __addKeytoBusqueda(self,cadena):
        """Soporte de atajos generico.Manipula los atajos
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
        if self.SM.getDB():
            self.Padre.showAgregarSnippet()
        else:
            QtGui.QMessageBox.warning(self, "Fragmentos",
            "No se ha seleccionado una base de datos donde guardar snippets.")       
    
    def __convertir_a_unicode(self,myQstring):
        return str(myQstring.toUtf8())

    def __cargarBDSeleccionada(self,indice):
        """ Al seleccionar otra base de datos desde el combo,
        reflejar los cambios en la interfaz. """
        
        #obtiene la ruta de la bd segun el indice
        rutaNueva = self.SM.getPathDB(indice)
        
        # vuelva a crear la instancia de bd con la nueva ruta
        self.SM.setDB(rutaNueva)
        
        # carga los snippets en el arbol
        self.refreshTree()
        self.historialSnippets = [[],0]
                
    def __loadBDsInCombo(self):
        ''' ''' 
        
        if self.SM.getDB() :
            bds = self.SM.getBDNames()
            if bds :
                for item in bds:
                    self.cbBD.addItem(item)
            
    def __centerOnScreen (self):
        """Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __createMenu(self):
        """Crea el main menu"""
        
        menu = QtGui.QMenu(self.btMenu)
        menusnippet = menu.addMenu("Snippet")
        menudatabase= menu.addMenu("Catalogo")
        menubusqueda = menu.addMenu("Busqueda")
        menu.addSeparator()
        menu.addAction("Opciones", self.__showOptions, QtGui.QKeySequence("Ctrl+O"))
        menu.addAction("Ayuda")
        menu.addSeparator()
        menu.addAction("Acerca de..", self.__mostrarAcercaDe)

        menusnippet.addAction("Agregar",self.__agregarSnippet,QtGui.QKeySequence("F9"))
        menusnippet.addAction("Editar", self.__modificarSnippet,QtGui.QKeySequence("Ctrl+M"))
        menusnippet.addAction("Eliminar", self.__eliminarSnippet)


        menudatabase.addAction("Nuevo... ", self.__nuevaBDFragmentos)
        #~ menudatabase.addAction("Eliminar")

        menubusqueda.addAction("'t=' Por Titulo")
        menubusqueda.addAction("'g=' Por Tags")
        menubusqueda.addAction("'l=' Por Lenguaje")
        menubusqueda.addAction("'n=' Por Fecha creacion")
        menubusqueda.addAction("'m=' Por Fecha modificacion")
        menubusqueda.addAction("'a=' Por Autor")

        self.btMenu.setMenu(menu)

    def __destroyed(self):
        ''' Hace volar la ventana. '''
        #TODO: hacer que cierre todas las ventanas
        sys.exit(0)
    
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
                
        QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self.__toogleFullScreen)
        QtGui.QShortcut(QtGui.QKeySequence("Supr"), self, self.__eliminarSnippet)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+M"), self, self.__modificarSnippet)
        # atajo : cerrar/salir
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
            
    def __cleanFields(self) :
        
        self.widgetcodigo.clearCode()
        self.txtDescripcion.setText("")
        self.btPonerComoFavorito.setChecked(False)
        self.leLenguaje.setText("")
        self.leTitulo.setText("")
        self.leTags.setText("")

    def __modificarSnippet(self):
        """ Ejecuta las instrucciones para modificar el snippet actual. """
        
        actual = self.SM.getSnippetActual()
        if actual is None:
            QtGui.QMessageBox.warning(self, "Modificar snippet",
        "Debes seleccionar un snippet para modificarlo.")
        else:
            self.Padre.showModificarSnippet(actual)

    def __showSnippet(self, lenguaje, titulo):
        
        # obtiene el snippet segun titulo y lenguaje
        snippet = self.SM.getSnippet(lenguaje,titulo)

        # muestra el codigo en el visor de codigo
        self.widgetcodigo.setFullCode(snippet.codigo,snippet.lenguaje)
        
        # carga en los campos los datos del snippet
        self.leTags.setText(snippet.tags)
        self.leTitulo.setText(snippet.titulo)
        self.leLenguaje.setText(snippet.lenguaje)
        self.txtDescripcion.setText('Descripcion: '+snippet.descripcion)
        self.lbFechaCreacion.setText('Creado: '+snippet.fechaCreacion)
        if not snippet.fechaModificacion is None:
            # si existe una fecha de modificado
            self.lbFechaModificacion.setVisible(True)
            self.lbFechaModificacion.setText('Modificado: '+str(snippet.fechaModificacion))
        else:
            #oculta el label
            self.lbFechaModificacion.setVisible(False)
            
        # si es favorito, cambia el estado del boton
        if snippet.favorito == "0":
            self.btPonerComoFavorito.setChecked(False)
        elif snippet.favorito == "1":
            self.btPonerComoFavorito.setChecked(True)
        
    def __setAsFavorite(self):
        
        #obtiene la instancia actual del snippet
        snippetActual = self.SM.getSnippetActual()
        
        #establece el nuevo valor
        if not snippetActual is None:
            #~ print str(int(self.btPonerComoFavorito.isChecked()))
            # refleja este cambio en los datos del snippet
            snippetActual.favorito = str(int(self.btPonerComoFavorito.isChecked()))
            
            # establece el nuevo estado del snippet
            self.SM.setSnippetActual(snippetActual)
            self.lbEstado.setText("Establecido como favorito.")
        else:
            # permite que el boton no sea chequeado
            self.btPonerComoFavorito.setChecked(False)

    def __historial(self,tipo,tLengTit=None):
        historial = self.historialSnippets[0]
        indice = self.historialSnippets[1]
        if tipo == 'add':
            historial = historial[:indice+1]
            historial.append(tLengTit)
            indice = len(historial)-1    
        
        elif tipo == 'forw':
            if (len(historial)-1) > indice:
                lenguaje,titulo = historial[indice+1]
                indice += 1
                self.__showSnippet(lenguaje,titulo)

        elif tipo == 'back':
            if indice:
                lenguaje,titulo = historial[indice-1]
                indice += -1
                self.__showSnippet(lenguaje,titulo)
        else:
            print "opcion incorrecta"
        self.historialSnippets = [historial,indice]

    def refreshTree(self):
        """ A partir de la instancia actual de SM,
        refresca el arbol cargando nuevamente los snippets. """
                
        lengs_and_titles = self.SM.getLengsAndTitles()
        # intancia el hilo que se encargara de refrescar el arbol 
        treeview = TreeViewThread(self, lengs_and_titles)        
        treeview.start()
        
        self.lbEstado.setText(
            str(self.SM.getSnippetsCount()) + ' snippet(s) cargados.')

    def __toogleFullScreen(self):
        ''' '''
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()
        self.fullScreen = not self.fullScreen
    
    ################################################################
    #   Metodos usados en el menu de la aplicacion
    ###############################################################        
    
    def __showOptions(self):
        ''' '''
        self.Padre.showOpciones()
        
    def __mostrarAyuda(self) : 
        ''' '''
        QtGui.QMessageBox.information(self, "Ayuda",
                "Opcion todavia no disponible en esta version.")
    
    def __mostrarAcercaDe(self):
        ''' '''
        self.Padre.showAcercaDe()
        
    def __nuevaBDFragmentos(self) :
        ''' Abre un dialogo de archivos, para guardar el 
        archivo de la bd creada.'''
        
        dialog = QtGui.QFileDialog(self, 'Nuevo catalogo de Fragmentos')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen | QtGui.QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Catalogo Fragmentos (*.db)')
        if dialog.exec_():
            filename = self.__convertir_a_unicode(
                            dialog.selectedFiles()[0])
            print filename, type(filename)
            
            # llamamos al metodo que crea la bd
            estado = self.Padre.fragmentos.BDU.newDataBase(filename)
            if estado :
                QtGui.QMessageBox.information(self, "Nuevo catalogo",
                "Catalogo creado con exito en : \n\n" + filename)
            else:
                QtGui.QMessageBox.critical(self, "Nuevo catalogo",
                "Se ha producido un error al intentar crear el catalogo.")

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
        self.Padre.clipboard.setText(self.widgetcodigo.getCode())
        
    @QtCore.pyqtSlot()
    def on_btBuscarEnFavoritos_clicked(self):
        ''' carga en el arbol los snippets favoritos'''
        
        if self.btBuscarEnFavoritos.isChecked():
            #obtiene solo los favoritos
            datos = self.SM.getLengsAndTitles("s=1",True)
        else:
            datos = self.SM.getLengsAndTitles()
        #carga los snippets en el arbol
        self.mytreeview.insertarEnArbol(datos)

    @QtCore.pyqtSlot()
    def on_btPonerComoFavorito_clicked(self):
        self.__setAsFavorite()

    @QtCore.pyqtSlot()
    def on_btSptAnterior_clicked(self):
        self.__historial('back')
        self.btSptSiguiente.setEnabled(True)
        if not self.historialSnippets[1]:#si no hay cosas para volver
            self.btSptAnterior.setEnabled(False)


    @QtCore.pyqtSlot()
    def on_btSptSiguiente_clicked(self):
        self.__historial('forw')
        self.btSptAnterior.setEnabled(True)
        if (len(self.historialSnippets[0])-1)==self.historialSnippets[1]:#si no hay cosas para adelantar
            self.btSptSiguiente.setEnabled(False)
        
    ###############
    ### ENTRYES ###
    ###############
    
    def on_eBusqueda_textChanged(self,cadena):
        # campo de pruebas en la busqueda
        
        datos = [] #@UnusedVariable
        datos = self.SM.getLengsAndTitles(
            str(self.__convertir_a_unicode(cadena)),
                self.btBuscarEnFavoritos.isChecked())
        if datos:
            # si hubieron resultados en la busqueda
            self.colorBusqueda.set_color_busqueda()
            self.mytreeview.insertarEnArbol(datos)
        else:
            self.colorBusqueda.set_color_busqueda(False)
            self.mytreeview.model.clear()
        self.lbEstado.setText(str(len(datos))+' snippet(s) encontrados...')
        if cadena == "":
            self.lbEstado.setText(
                str(self.SM.getSnippetsCount()) + ' snippet(s) cargados...')

    ################
    ### TREEVIEW ###
    ################
    
    def on_tvLenguajes_selectedItem(self,indice,b):
        if indice.parent().row() != -1:
            lenguaje =  unicode(
                            indice.parent().data().toString().toUtf8(),
                            'utf-8')
            titulo =  unicode(
                            indice.data().toString().toUtf8(),
                            'utf-8')
        #History zone
            self.btSptAnterior.setEnabled(True)
            self.btSptSiguiente.setEnabled(False)
            self.__historial('add', (lenguaje,titulo))
            self.__showSnippet(lenguaje,titulo)
            
    ################
    ### COMBOBOX ###
    ################
    
    @QtCore.pyqtSlot(int)
    def on_cbBD_currentIndexChanged(self,index):
        if self.PasePorAca:
            self.__cargarBDSeleccionada(self.cbBD.currentIndex())
        else:
            self.PasePorAca = True
            
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        
class TreeViewThread(QtCore.QThread):
    ''' Este hilo se encarga de cargar los snippets en el arbol de la interfaz.'''
    
    def __init__(self, parent, lengs_and_titles):
        QtCore.QThread.__init__(self, parent)
        self.Padre = parent
        # lengs_and_titles, viene desde MainForm y es el resultado 
        # de SM.getLengsAndTitles()
        self.datos = lengs_and_titles
        
    def run(self):        
        self.Padre.mytreeview.insertarEnArbol(self.datos)
        
def main():
    pass

if __name__ == "__main__":
    main()
