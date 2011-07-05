#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import os,sys
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt

class Main(QtGui.QDialog):
    """La ventana principal de la aplicación."""
    def __init__(self):
    #Cargar archivo ui
        FILENAME = 'wAgregar.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QDialog.__init__(self)
        uic.loadUi(uifile, self)
    #cargar lenguajes en combo

    @QtCore.pyqtSlot()
    def on_btAbrirDesdeArchivo_clicked(self):
        contenido = self.showFileDialog()
        self.eCodigo.setText(contenido)

    @QtCore.pyqtSlot()
    def on_btGuardar_clicked(self):
         QtGui.QMessageBox.information(self, "frutaaa","mas frutaaaaaa")

############
## Metods ##
############
    def showFileDialog(self):
        """ Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Abrir desde archivo')
        fname = open(filename)
        data = fname.read()
        #devuelve los datos leidos desde el archivo
        return data

def main():
    app = QtGui.QApplication(sys.argv)
    m = Main()
    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
