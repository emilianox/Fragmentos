#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
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

import os
import sys

from PyQt4 import QtCore, QtGui, uic
from QTTips.Scintilla import Scintilla
import icons_rc


class agregarSnippet(QtGui.QMainWindow):

    """Ventana agregar Snippet."""

    def __init__(self, parent, titulo):
        # carga la interfaz desded el archivo ui
        FILENAME = 'wAgregarSnippet.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        self.setWindowIcon(QtGui.QIcon(':/icons/linedpaperplus32.png'))
        # centra la ventana 
        self.__centerOnScreen()
        
        # establece el titulo de la ventana
        self.setWindowTitle(titulo)
        
        # crear el widget de codigo
        self.widgetcodigo = Scintilla()        
        
        # agregar el widget de codigo a este layout
        
        self.verticalLayout_7.addWidget(self.widgetcodigo.getEditor())
        self.widgetcodigo.setFocus() 
        
        # cargar lenguajes en combo
        self.__cargarLenguajesEnCombo()
        
        # carga los atajos de teclado 
        self.__loadAppShortcuts()
        
        # instancia de SnippetManager desde GUI
        self.SM = parent.SM
        self.Padre = parent # GUI
        
        # variable usada para saber si se trata de una operacion de
        # agregar o modicar. Se usa como string.
        self.operacion = None

########################
## Metodos de Eventos ##
########################

    @QtCore.pyqtSlot()
    def on_btAbrirDesdeArchivo_clicked(self):
        # muestra el dialogo para seleccionar un archivo
        # la funcion retorna el contenido del archivo
        contenido = self.__showFileDialog()
        
        # se muestra el contenido en el widget de codigo
        if contenido:
            self.widgetcodigo.setCode(contenido)

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        # segun la operacion, ejecuta el metodo correspondiente 
        if self.operacion == "agregar":
            self.__guardarSnippet()
            self.close()
        if self.operacion == "modificar":
            self.__modificarSnippet()
            self.close()
        # hace que refresque el arbol de la interfaz principal
        self.Padre.refreshTreeMainWindow()
        

    @QtCore.pyqtSlot()
    def on_btLimpiarCampos_clicked(self):
        self.__cleanFields()
        
    @QtCore.pyqtSlot(int)
    def on_cbLenguajes_currentIndexChanged(self):
        # recupera el texto actualmente mostrado en el combo
        lenguaje = str(self.cbLenguajes.itemText(
                            self.cbLenguajes.currentIndex()).toUtf8())
        
        # establece el lenguaje segun el seleccionado
        self.widgetcodigo.setLanguage(lenguaje)
        
        
    def on_eTags_editingFinished(self):
        # aplica esta funcion al texto en el campo tags
        self.eTags.setText(
            self.__normalizarTags(
                self.__toUnicode(self.eTags.text())))
    
    def on_eTitulo_editingFinished(self):
        # aplica esta funcion al texto en el campo titulo
        self.eTitulo.setText(
            self.__normalizarTitulo(
                self.__toUnicode(self.eTitulo.text())))
        
    def closeEvent(self, event):
            event.ignore()
            self.hide()
                
    def destroyed(self):
        ''' Hace volar la ventana. '''
        #TODO: hacer que cierre todas las ventanas
        #sys.exit(0)
        self.close()
        pass
        
########################
## Metodos Auxiliares ##
########################

    def __cargarLenguajesEnCombo(self):
        u""" Carga los lenguajes disponibles, en la lista desplegable."""
        
        # le pide al widget de codigo que le devuelva los lenguajes
        # disponibles y los carga en el combo de lenguajes
        lenguajes = self.widgetcodigo.getLanguages()
        for lenguaje in lenguajes:
            self.cbLenguajes.addItem(lenguaje)
            
    def __centerOnScreen(self):
        u"""Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
        
    def __guardarSnippet(self):
        """ """
        #FIXME: frutea el tema de la codificacion, ver q onda.
        
        # valida que los campos obligatorios no esten vacios
        if self.__validarCampos():
            
            # obtiene los datos en un diccionario
            datosSnippet = self.__leerDatosDeLosCampos()
            
            # ejecuta el proceso de agregar
            resultado, mensaje = self.SM.agregarSnippet(datosSnippet)
            if resultado:
                # limpia el contenido en los campos
                self.__cleanFields()
                # muestra un mensaje con la confirmacion de la operacion
                QtGui.QMessageBox.information(self, "Agregar snippet","Snippet agregado correctamente.")
                
                #TODO: actualizar el arbol de la interfaz principal

            else:
                # muestra un aviso de error con el mensaje de error
                # capturado desde la bd
                QtGui.QMessageBox.critical(self, "Agregar snippet",
                "Se ha producido un error.\n\nMensaje del error: " + mensaje)

    def __leerDatosDeLosCampos(self):
        """ Recupera la informacion cargada en los campos de la interfaz. """

        from datetime import datetime
        # convierte a 0 o 1 segun el estado del check
        favorito = None
        if self.chkFavorito.isChecked(): 
            favorito = "1" 
        else:
            favorito = "0"
            
        # carga los datos de los campos en un diccionario,
        # convirtiendo a utf8 el texto
        titulo = self.__toUnicode(self.eTitulo.text())
        lenguaje =  self.__toUnicode(self.cbLenguajes.itemText(self.cbLenguajes.currentIndex()))
        tags = self.__toUnicode(self.eTags.text())
        codigo = self.widgetcodigo.getCode()
        descripcion = unicode(self.eDescripcion.toPlainText().toUtf8(),'utf-8')
        referencias = self.__toUnicode(self.eReferencias.text())
        fcreacion = unicode(datetime.today().strftime('%d/%m/%Y %H:%M:%S'))
        uploader = self.__toUnicode(self.eAutor.text())
        
        # cree el diccionario con los valores leidos
        snippet = {
        'title': titulo,'language': lenguaje,'tags' : tags,
        'contens' : codigo,'description' : descripcion,
        'reference' : referencias,'creation' : fcreacion,
        'modified' : "",'uploader' : uploader,'starred' : favorito
        }
        
        return snippet
        
    def __cleanFields(self):
        u""" Limpia los valores de los campos."""
        
        self.eTitulo.setText("")
        self.widgetcodigo.setCode("")
        self.eTags.setText("")
        self.eDescripcion.setText("")
        self.eReferencias.setText("")
        self.eAutor.setText("")
        self.chkFavorito.setChecked(False)
        
    def __loadAppShortcuts(self):
        u""" Load shortcuts used in the application. """
        # atajo : guardar
        QtGui.QShortcut(QtGui.QKeySequence("F10"), self, self.on_btGuardar_clicked)
        # atajo : cerrar/salir
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)
        # atajo : limpiar los campos
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+L"), self, self.__cleanFields)

    def __normalizarTitulo(self, titulo):
        u""" """
        # quita mas de un espacio entre las palabras
        while titulo.find("  ") != -1:
                titulo = titulo.replace("  "," ")
        # quita espacios al comienzo y final
        titulo = titulo.strip()
        # pone la primer letra a Mayuscula
        #~ titulo = titulo.capitalize()
        
        return titulo
        
    def __normalizarTags(self, tags):
        u""" 
            Normaliza los tags: quitando espacios, 
            quitando acentos, etc.
        """
        # quita todo espacio en blanco de la palabra
        tags = ''.join(tags.split())
        # pasa todas las letras a minuscula
        tags = tags.lower()
        # reemplaza las dobles comas por una sola
        while tags.find(",,") != -1:
            tags = tags.replace(",,",",")
        # si llegaran a existe comas al principio y final, las quita
        tags = tags.strip(",")
        
        return tags

    def __modificarSnippet(self):
        # valida que los campos obligatorios no esten vacios
        if self.__validarCampos():
            # obtiene los datos en un diccionario
            datosSnippet = self.__leerDatosDeLosCampos()
            # obtiene el snippet actual
            snippetActual = self.SM.getSnippetActual()
            
            lenguaje_viejo =  snippetActual.lenguaje 
            titulo_viejo = snippetActual.titulo

            # pregunta por cada uno de los campos del snippet
            # si ha havido algun cambio, y en caso afirmativo
            # se setean los valores
            if datosSnippet["title"] != snippetActual.titulo :
                snippetActual.titulo = datosSnippet["title"]
            if datosSnippet["language"] != snippetActual.lenguaje :
                snippetActual.lenguaje = datosSnippet["language"]
            if datosSnippet["tags"] != snippetActual.tags :
                snippetActual.tags = datosSnippet["tags"]
            if datosSnippet["contens"] != snippetActual.codigo :
                snippetActual.codigo = datosSnippet["contens"]
            if datosSnippet["description"] != snippetActual.descripcion :
                snippetActual.descripcion = datosSnippet["description"]
            if datosSnippet["reference"] != snippetActual.referencias :
                snippetActual.referencias = datosSnippet["reference"]
            if datosSnippet["uploader"] != snippetActual.uploader :
                snippetActual.uploader = datosSnippet["uploader"]
            if datosSnippet["starred"] != snippetActual.favorito :
                snippetActual.favorito = datosSnippet["starred"]
            
            # como esto es una modificacion, obtiene la fecha del sistema
            # y guarda esta fecha en la campo de modificacion
            from datetime import datetime
            fecha_Modificacion = unicode(datetime.today().strftime('%d/%m/%Y %H:%M:%S'))
            snippetActual.fechaModificacion = fecha_Modificacion
            
            self.__cleanFields()
            
            # actualiza el snippet en RAM
            self.SM.modificarSnippet((lenguaje_viejo,titulo_viejo),snippetActual)
            
            # refresca el arbol en la interfaz principal
            self.Padre.refreshTreeMainWindow()
            
            QtGui.QMessageBox.information(self, "Modificar snippet","Snippet modificado correctamente.")


    def __showFileDialog(self):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Abrir desde archivo')
        if filename: 
            fname = open(filename)
            data = fname.read()
            #devuelve los datos leidos desde el archivo
            return data
        else:
            return ''
        
    def __toUnicode(self,myQstring):
        u""" Convierte a UTF8 el objeto QString recibido. """
        #~ print myQstring
        return unicode(myQstring.toUtf8(),'utf-8')

    def __validarCampos(self):
        u""" Verifica que los campos obligatorios no estén vacíos. """
        valido = False
        
        # pregunta que el titulo, codigo y lenguaje no esten vacios
        if self.__toUnicode(self.eTitulo.text()) != '' and \
           self.__toUnicode(self.cbLenguajes.itemText(self.cbLenguajes.currentIndex())) != '' and \
           self.widgetcodigo.getCode() != '':
            valido = True
        else:
            mensaje = """Alguno de estos campos no pueden estar en blanco:

            - Titulo
            - Lenguaje
            - Codigo"""
            QtGui.QMessageBox.warning(self, "Agregar snippet",mensaje)
        return valido

def main():
    app = QtGui.QApplication(sys.argv)
    m = agregarSnippet()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
