#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import os,sys
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt
#Importo los iconos
import fragmentos_rc  #@UnusedImport

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
        # establece el icono de la ventana
        #~ self.setWindowIcon(QtGui.QIcon(":/app.png"))

        # centra la ventana en la pantalla
        self.__centerOnScreen()

        # conectar salir
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.destroyed)

        # agrega y crea el Treeview
        self.mytreeview = TreeView(self.tvLenguajes,self.on_tvLenguajes_selectedItem,self.connect)

        # agrega el Widget de codigo
        self.widgetcodigo = Scintilla()
        self.wgtDetalles.setVisible(False)
        self.vlCodigo.insertWidget(0,self.widgetcodigo.getEditor())

        # Reordenamiento  y expancion
        self.spPrincipal.setSizes([50,900])#ni idea pero no tocar

        # colores x defecto
        self.colorBusqueda = QcolorTextEdit(self.eBusqueda)

        # Instancia y variables usadas
        self.Padre = parent # esto es GUI
        self.SM = self.Padre.newSnippetManager(None) # esto es GUI.SM
        self.PasePorAca = False
        self.fullScreen = False
        self.snippetsAnteriores = [None]
        self.snippetsSiguientes = [None]

        # establece el trayicon
        self.Padre.setTrayIcon(self)

        self.refrescarArbol()

        # carga las bds en el combo
        self.cargarBDsEnCombo()

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
        self.refrescarArbol()
                
    def cargarBDsEnCombo(self):
        bds = self.SM.getBDNames()
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

    def destroyed(self):
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
        #Add Snippet Shortcut
        QtGui.QShortcut(QtGui.QKeySequence("F9"), self, self.on_btAgregarSnippet_clicked)
        QtGui.QShortcut(QtGui.QKeySequence("F11"), self, self.__toogleFullScreen)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+M"), self, self.__modificarSnippet)
        QtGui.QShortcut(QtGui.QKeySequence("Supr"), self, self.__eliminarSnippet)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+O"), self, self.__mostrarOpciones)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.destroyed)

    def __limpiarCampos(self) :
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

    def __mostrar_snippet(self, lenguaje, titulo):
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

    def refrescarArbol(self):
        """ A partir de la instancia actual de SM,
        refresca el arbol cargando nuevamente los snippets. """

        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())

        self.lbEstado.setText(
            str(self.SM.getSnippetsCount()) + ' snippet(s) cargados.')

    def __toogleFullScreen(self):
        if not self.fullScreen :
            self.showFullScreen()
        else:
            self.showNormal()
        self.fullScreen = not self.fullScreen
    
    ################################################################
    #   Metodos usados en el menu de la aplicacion
    ################################################################
    
    def __createMenu(self):
        """Crea el main menu"""
        menu = QtGui.QMenu(self.btMenu)
        snippet = menu.addAction("Snippet")
        database= menu.addAction("Database")
        busqueda = menu.addAction("Buscar")
        menu.addSeparator()
        menu.addAction("Opciones", self.__mostrarOpciones,QtGui.QKeySequence("Ctrl+O"))
        menu.addAction("Ayuda")
        menu.addSeparator()
        menu.addAction("Acerca de", self.__mostrarAcercaDe)


        menusnippet = QtGui.QMenu()
        menusnippet.addAction("Agregar",self.__agregarSnippet,QtGui.QKeySequence("F9"))
        menusnippet.addAction("Modificar",self.__modificarSnippet,QtGui.QKeySequence("Ctrl+M"))
        menusnippet.addAction("Eliminar", self.__eliminarSnippet,QtGui.QKeySequence("Supr"))
        snippet.setMenu(menusnippet)
        
        menudatabase = QtGui.QMenu()
        menudatabase.addAction("Nueva...",self.__nuevaBDFragmentos)
        menudatabase.addAction("Eliminar")
        database.setMenu(menudatabase)

        menubusqueda = QtGui.QMenu()
        menubusqueda.addAction("'t=' Por Titulo")
        menubusqueda.addAction("'l=' Por Lenguaje")
        menubusqueda.addAction("'g=' Por Tags")
        menubusqueda.addAction("'c=' Por Codigo")
        menubusqueda.addAction("'d=' Por Descripcion")
        menubusqueda.addAction("'r=' Por Referencias")
        menubusqueda.addAction("'n=' Por Fecha creacion")
        menubusqueda.addAction("'m=' Por Fecha modificacion")
        menubusqueda.addAction("'u=' Por Autor")
        
        busqueda.setMenu(menubusqueda)
        
        self.btMenu.setMenu(menu)
        #        .showMenu (self)
        
    def __mostrarOpciones(self):
        ''' '''
        self.Padre.showOpciones()
        
    def __mostrarAyuda(self) : 
        ''' '''
        QtGui.QMessageBox.information(self, "Ayuda",
                "Opcion todavia no disponible es esta version.")
    
    def __mostrarAcercaDe(self):
        ''' '''
        self.Padre.showAcercaDe()
        
    def __nuevaBDFragmentos(self) :
        ''' Abre un dialogo de archivos, para guardar el 
        archivo de la bd creada.'''
        
        dialog = QtGui.QFileDialog(self, 'Nueva base de datos')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen | QtGui.QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Fragmentos Databases (*.db)')
        if dialog.exec_():
            filename = self.__convertir_a_unicode(
                            dialog.selectedFiles()[0])
            print filename, type(filename)
            
            # llamamos al metodo que crea la bd
            estado = self.Padre.fragmentos.BDU.newDataBase(filename)
            if estado :
                QtGui.QMessageBox.information(self, "Nueva base de datos",
                "Base de datos creada con exito en : \n\n" + filename)
            else:
                QtGui.QMessageBox.critical(self, "Nueva base de datos",
                "Se ha producido un error al intentar crear la base de datos.")
        

                
                
                
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
        pass
        
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

    @QtCore.pyqtSlot()
    def on_btSptAnterior_clicked(self):

        # si la cantidad es > a 0
        if len(self.snippetsAnteriores) >= 1 :
            # obtiene el anterior snippet mostrado
            valores = self.snippetsAnteriores.pop()

            # agrega este snippet a los siguientes
            #~ self.snippetsSiguientes.append(valores)

            #~ print "agregado de lista de siguientes: ", valores


            # muestra en la interfaz el snippet
            self.__mostrar_snippet(valores[0],valores[1])

            #~ print "quitado de anteriores: ", valores,len(self.snippetsAnteriores) 
        else:
            self.__limpiarCampos()


        # estado de los botones
        #~ if len(self.snippetsAnteriores) > 2 :
            #~ self.btSptAnterior.setEnabled(True)
        #~ elif len(self.snippetsAnteriores) == 1 :
            #~ self.btSptAnterior.setEnabled(False)


    @QtCore.pyqtSlot()
    def on_btSptSiguiente_clicked(self):
        pass
        # si la cantidad es > a 0
        #~ if len(self.snippetsSiguientes) > 0 :
            # obtiene el anterior snippet mostrado
            #~ valores = self.snippetsSiguientes.pop()
            
            #~ if not valores is None :
            # muestra en la interfaz el snippet
                #~ self.__mostrar_snippet(valores[0],valores[1])

            #~ print "quitado de siguientes: ", valores
            
        # estado de los botones
        #~ if len(self.snippetsSiguientes) > 2 :
            #~ self.btSptSiguiente.setEnabled(True)
        #~ else:
            #~ self.btSptSiguiente.setEnabled(False)
        
        
    ###############
    ### ENTRYES ###
    ###############
    
    def on_eBusqueda_textChanged(self,cadena):
        # campo de pruebas en la busqueda
        datos = self.SM.getLengsAndTitles(
            str(self.__convertir_a_unicode(cadena)),
                self.btBuscarEnFavoritos.isChecked())
        if datos:
            # si hubieron resultados en la busqueda
            self.colorBusqueda.set_color_busqueda()
            self.mytreeview.insertarEnArbol(datos)
            #~ self.tvLenguajes.expandAll()
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
            
            #~ sptAnterior = self.SM.getSnippetActual()
            self.__mostrar_snippet(lenguaje,titulo)
            #~ self.sprMostrado = self.SM.getSnippetActual()
            
            #~ if sptAnterior is not None:
                #~ self.snippetsAnteriores.append([
                                    #~ sptAnterior.lenguaje,
                                    #~ sptAnterior.titulo])
            #~ self.snippetsSiguientes.append([
                                    #~ self.sprMostrado.lenguaje,
                                    #~ self.sprMostrado.titulo])
                #~ print "agregado a anteriores: ",[lenguaje,titulo],len(self.snippetsAnteriores) 
            #~ else :
                #~ self.__limpiarCampos()
            
            #~ if len(self.snippetsAnteriores) > 2 :
                #~ self.btSptAnterior.setEnabled(True)
            #~ else:
                #~ self.btSptAnterior.setEnabled(False)
                
            #~ if len(self.snippetsSiguientes) > 2 :
                #~ self.btSptSiguiente.setEnabled(True)
            #~ else:
                #~ self.btSptSiguiente.setEnabled(False)
            #~ self.btSptSuiguiente.setEnabled(False)
            
    ################
    ### COMBOBOX ###
    ################
    
    @QtCore.pyqtSlot(int)
    def on_cbBD_currentIndexChanged(self,index):
        if self.PasePorAca:
            self.__cargarBDSeleccionada(self.cbBD.currentIndex())
        else:
            self.PasePorAca = True
        
def main():
    pass

if __name__ == "__main__":
    main()
