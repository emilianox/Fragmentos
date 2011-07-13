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
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt
from QTTips.Scintilla import Scintilla


#~ class Main(QtGui.QDialog):
class agregarSnippet(QtGui.QMainWindow):

    """Ventana agregar Snippet."""

    def __init__(self, parent):
    #Cargar archivo ui
        FILENAME = 'wAgregarSnippet.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()
    #cargar widget de codigo
        self.widgetcodigo = Scintilla()
        self.verticalLayout_6.addWidget(self.widgetcodigo.getEditor())
        self.widgetcodigo.setFocus()
#        self.splitter.setSizes([200,200])
    #cargar lenguajes en combo
        self.__cargarLenguajesEnCombo()
        #~ print 'intentando establecer codigo...'
        #~ self.widgetcodigo.setLenguaje('Python')
        #~ print 'codigo establecido...'
        #~ self.pase_por_aca = False
    #instancia de SnippetManager desde GUI
        self.SM = parent.SM

        print 'abriendo formulario agregar Snippet...'

########################
## Metodos de Eventos ##
########################

    @QtCore.pyqtSlot()
    def on_btAbrirDesdeArchivo_clicked(self):
        contenido = self.__showFileDialog()
        #~ self.widgetcodigo.agregar_codigo('Custom',contenido)
        self.widgetcodigo.setCode(contenido)

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
        self.__guardarSnippet()

    @QtCore.pyqtSlot(int)
    def on_cbLenguajes_currentIndexChanged(self):
        lenguaje = str(self.cbLenguajes.itemText(
                            self.cbLenguajes.currentIndex()).toUtf8())
        self.widgetcodigo.setLanguage(lenguaje)
        #print 'lenguaje: ',lenguaje
        
    def on_eTags_editingFinished(self):
        #aplica esta funcion al texto en el campo tags
        self.eTags.setText(
            self.__normalizarTags(
                self.__toUnicode(self.eTags.text())))
    
########################
## Metodos Auxiliares ##
########################
    
    def __centerOnScreen(self):
        u"""Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def __guardarSnippet(self):
        """ """
        #FIXME: frutea el tema de la codificacion, ver q onda.
        
        #valida que los campos obligatorios no esten vacios
        if self.__validarCampos():
            #obtiene los datos en un diccionario
            datosSnippet = self.__leerDatosDeLosCampos()
            #ejecuta el proceso de agregar
            resultado, mensaje = self.SM.agregarSnippet(datosSnippet)
            if resultado:
                self.__limpiarCampos()
                QtGui.QMessageBox.information(self, "Agregar snippet","Snippet agregado correctamente.")
                #actualiza el arbol de la interfaz principal

            else:
                QtGui.QMessageBox.critical(self, "Agregar snippet",
                "Se ha producido un error.\n\nMensaje del error: " + mensaje)

    def __showFileDialog(self):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Abrir desde archivo')
        fname = open(filename)
        data = fname.read()
        #devuelve los datos leidos desde el archivo
        return data

    def __cargarLenguajesEnCombo(self):
        u""" Carga los lenguajes disponibles, en la lista desplegable."""
        
        lenguajes = self.widgetcodigo.getLanguages()
        for lenguaje in lenguajes:
            self.cbLenguajes.addItem(lenguaje)

    def __leerDatosDeLosCampos(self):
        u""" Recupera la informacion cargada en los campos de la interfaz. """

        from datetime import datetime
        #carga los datos de lso campos en un diccionario,
        #convirtiendo a utf8 el texto
        snippet = {
        'title': self.__toUnicode(self.eTitulo.text()),
        'language': self.__toUnicode(
                        self.cbLenguajes.itemText(
                            self.cbLenguajes.currentIndex())),
        'tags' : self.__toUnicode(self.eTags.text()),
        'contens' : self.__toUnicode(self.widgetcodigo.getCode()),
        'description' : unicode(self.eDescripcion.toPlainText()),
        'reference' : self.__toUnicode(self.eReferencias.text()),
        'creation' : datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
        'modified' : None,
        'uploader' : self.__toUnicode(self.eAutor.text()),
        'starred' : self.chkFavorito.isChecked()
        }

        return snippet

    def __limpiarCampos(self):
        u""" Limpia los valores de los campos."""
        
        self.eTitulo.setText("")
        self.widgetcodigo.setCode("")
        self.eTags.setText("")
        self.eDescripcion.setText("")
        self.eReferencias.setText("")
        self.eAutor.setText("")
        self.chkFavorito.setChecked(False)
        
    def __toUnicode(self,myQstring):
        u""" Convierte a UTF8 el objeto QString recibido. """
        return str(myQstring.toUtf8())

    def __validarCampos(self):
        u""" Verifica que los campos obligatorios no estén vacíos. """
        valido = False
        #TODO: acortar esta condicion
        if self.__toUnicode(self.eTitulo.text()) != '' and self.__toUnicode(self.cbLenguajes.itemText(self.cbLenguajes.currentIndex())) != '' and self.__toUnicode(self.widgetcodigo.getCode()) != '':
            valido = True
        else:
            mensaje = """Alguno de estos campos no pueden estar en blanco:

            - Titulo
            - Lenguaje
            - Codigo"""
            QtGui.QMessageBox.warning(self, "Agregar snippet",mensaje)
        return valido

    def __normalizarTags(self, tags):
        u""" 
            Normaliza los tags: quitando espacios, 
            quitando acentos, etc.
        """
        #quita todo espacio en blanco de la palabra
        tags = ''.join(tags.split())
        #pasa todas las letras a minuscula
        tags = tags.lower()
        #reemplaza las dobles comas por una sola
        while tags.find(",,") != -1:
            tags = tags.replace(",,",",")
        #si llegaran a existe comas al principio y final, las quita
        tags = tags.strip(",")
        #vuelve a unir todas las palabras
        return tags
            
def main():
    app = QtGui.QApplication(sys.argv)
    m = agregarSnippet()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
