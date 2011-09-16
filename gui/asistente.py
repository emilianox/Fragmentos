#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtCore, QtGui, uic
import fragmentos_rc

class Asistente(QtGui.QWizard):
    def __init__(self, parent=None):
        super(Asistente, self).__init__(parent)
        
        FILENAME = 'wAsistente.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
        self.__centerOnScreen()

        self.connect(self.button(self.BackButton),QtCore.SIGNAL("clicked()"),self.back)
        self.connect(self.button(self.NextButton) ,QtCore.SIGNAL("clicked()"),self.next)
        self.connect(self, QtCore.SIGNAL('accepted()'), self.finish)
        
        # por defecto estos botones estan en ingles,
        # esto, los traduce al español
        self.setButtonText(self.BackButton,"< &Anterior")
        self.setButtonText(self.NextButton,"Siguie&nte >")
        self.setButtonText(self.FinishButton,"&Terminar")
        
        # campo para saber a que operacion se esta haciendo referencia
        self.operacion = 'abrir_catalogo'        

        self.__GUI = parent
        #~ self.__Configs = parent.fragmentos.ConfigsApp
    
    def back(self):
        print 'para atras...'
    
    def next(self):
        print 'siguiete'
           
    def finish(self):
        print 'saliendo...'
        pass
        
    @QtCore.pyqtSlot()
    def on_btExaminar_clicked(self):
        if self.operacion is 'abrir_catalogo':
            self.eUbicacion.setText(
                self.__showFileDialog(self.titulo_abrir_catalogo))
        
        if self.operacion is 'crear_catalogo':
            self.eUbicacion.setText(
                self.__showFileDialog(self.titulo_crear_catalogo))
            
    @QtCore.pyqtSlot()
    def on_rbAbrirCatalogo_pressed(self):
        self.operacion = 'abrir_catalogo'
        #~ self.lbTitulo.setText(self.titulo_abrir_catalogo)
        
    @QtCore.pyqtSlot()
    def on_rbCrearCatalogo_pressed(self):
        self.operacion = 'crear_catalogo'
        print self.currentId() 
        
    def __centerOnScreen(self):
        """Centers the window on the screen."""
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
            
    def __showFileDialog(self, titulo):
        u""" Muestra un cuadro de dialogo desde donde seleccionar un archivo. """
        
        dialog = QtGui.QFileDialog(self, titulo)
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)   
        
        if self.operacion  == 'abrir_catalogo':
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        if self.operacion == 'crear_catalogo':
            dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen | QtGui.QFileDialog.AcceptSave)
            
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Catalogo Fragmentos (*.db)')
        if dialog.exec_():
            filename = unicode(
                dialog.selectedFiles()[0],'utf-8')
            return filename
        else:
            return ''
            
    def __addBDReference(self):
        dialog = QtGui.QFileDialog(self, 'Agregar ubicacion por referencia')
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setDefaultSuffix("db")
        dialog.setNameFilter('Catalogo Fragmentos (*.db)')
        if dialog.exec_():
            filename = dialog.selectedFiles()[0] # convierte a unicode el string
            filename = unicode(filename, 'utf-8') # persiste la nueva refrencia en el cfg
            self.__agregarBDReferenciaInCFG(filename) # refresca la gui
            self.__cargarBDsDesdeCFG()
            
    def __agregarBDReferenciaInCFG(self, pathCatalogo):
        ''' Agrega el nuevo catalogo seleccionado en el archivo CFG'''

        # recupera el string guardado en el cfg
        referencias = self.__Configs.referencesToBds
        # separa los paths
        referencias = referencias.split(',')
        # agrega el nuevo path a los existentes
        referencias.append(pathCatalogo)
        # vuelve a juntar los path en un solo string
        # y lo guarda nuevamente en el cfg
        self.__Config.referencesToBds = ','.join(referencias)
        
    def __addBDDefault(self):
        pass
        
    def __newBDFragmentos(self) :
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
    def __goToPage(self):
        if self.rbAbrirCatalogo.isChecked :
            print self.currentId() 
            
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    wizard = Asistente()
    wizard.show()
    sys.exit(app.exec_())
