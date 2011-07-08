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

import os,sys
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt
from QTTips.Scintilla import Scintilla

#~ class Main(QtGui.QDialog):
class agregarSnippet(QtGui.QMainWindow):
    """Ventana agregar Snippet."""
    
    def __init__(self):
    #Cargar archivo ui
        FILENAME = 'wAgregarSnippet.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
    #cargar widget de codigo
        self.widgetcodigo = Scintilla()
        self.verticalLayout_6.addWidget(self.widgetcodigo.getEditor())
        #~ self.splitter_2.setSizes([200,50])
    #cargar lenguajes en combo
        self.__cargarLenguajesEnCombo()
        #~ print 'intentando establecer codigo...'
        #~ self.widgetcodigo.setLenguaje('Python')
        #~ print 'codigo establecido...'
        #~ self.pase_por_aca = False
        
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
        QtGui.QMessageBox.information(self, "frutaaa","los datos son: \n "+str(self.__leerDatosDeLosCampos()))

    def on_cbLenguajes_currentIndexChanged(self):
        lenguaje = str(self.cbLenguajes.itemText(
                            self.cbLenguajes.currentIndex()).toUtf8())
        self.widgetcodigo.setLanguage(lenguaje)
        print 'lenguaje: ',lenguaje
    
########################
## Metodos Auxiliares ##
########################

    def __showFileDialog(self):
        """ Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Abrir desde archivo')
        fname = open(filename)
        data = fname.read()
        #devuelve los datos leidos desde el archivo
        return data
    
    def __cargarLenguajesEnCombo(self):
        ''' Carga los lenguajes disponibles en la lista desplegable.'''
        lenguajes = self.widgetcodigo.getLanguages()
        for lenguaje in lenguajes: 
            self.cbLenguajes.addItem(lenguaje)

    def __leerDatosDeLosCampos(self):
        ''' Recupera la infromacion cargada en los campos de la interfaz. '''
        
        from datetime import datetime
        snippet = {
        'title': self.__toUnicode(self.eTitulo.text()),
        'language': self.__toUnicode(
                        self.cbLenguajes.itemText(
                            self.cbLenguajes.currentIndex())),
        'tags' : self.__toUnicode(self.eTags.text()),
        'contents' : self.__toUnicode(self.widgetcodigo.getCode()),
        'description' : str(self.eDescripcion.toPlainText()),
        'references' : self.__toUnicode(self.eReferencias.text()),
        'creation' : datetime.today().strftime('%d/%m/%Y %H:%M:%S'),
        'modified' : None,
        'uploader' : self.__toUnicode(self.eAutor.text()),
        'starred' : self.chkFavorito.isChecked()
        }
        return snippet
        
    def __toUnicode(self,myQstring):
        ''' Convierte a UTF8 el objeto QString recibido. '''
        return str(myQstring.toUtf8())

def main():
    app = QtGui.QApplication(sys.argv)
    m = agregarSnippet()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
