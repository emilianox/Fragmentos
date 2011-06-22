#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys
# Importamos los módulos de Qt
from PyQt4 import QtCore, QtGui, uic
import snippetmanager,utils
class Main(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    def __init__(self):
    #Boludeces de instancias
        mainUtils = utils.Utils()
        print 'instancia de UTILS generada...'
        pathbd_volador = mainUtils.getPathDatabasesDir()+'SourceCode.db'
        self.SM = snippetmanager.SnippetManager(pathbd_volador)
    #Cargar archivo ui
        FILENAME = 'fragPP.ui'
        QtGui.QMainWindow.__init__(self)
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
    #Treeview agregado
        self.mytreeview = TreeViewModel()
        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitlesFromBD())
        self.tvLenguajes.setModel(self.mytreeview.model)
    #Detalles de armado interfaz
      #Widget codigo
        self.widgetcodigo = TheCodeWidget()
        self.spPrincipal.addWidget(self.widgetcodigo.editor)
      #Reordenamiento
        self.spPrincipal.setSizes([50,900])#ni idea
        print self.spPrincipal.sizes()#ni idea


    def mostrar_snippet(self,lenguaje,titulo):
        #hacerlo a lo bruto
        #~ import codecs
        #~ self.widgetcodigo.agregar_codigo('aaa', codecs.open("fragPPQT.py", "r", "utf-8" ).read())

        snippet = self.SM.getSnippetFromBD(lenguaje,titulo)

        #~ tags,codigo = 1#con lo anterior busca en SM el codigo
        self.widgetcodigo.agregar_codigo(snippet.getLenguaje(),snippet.getCodigo())

        #################
        #~ import PyQt4.Qsci
        #~ langs = [i for i in dir(PyQt4.Qsci) if i.startswith('QsciLexer')]
        ##################



    @QtCore.pyqtSlot()
    @QtCore.pyqtSlot()
    def on_btPrueba_clicked(self):
        print "hello!!"
        print self.eBusqueda.text()

    def on_eBusqueda_textChanged(self,cadena):
        #~ print self.__convertir_a_unicode(cadena)
        datos = self.SM.getLengsAndTitlesFromBD(str(self.__convertir_a_unicode(cadena)))
        self.mytreeview.insertarEnArbol(datos)

    def on_tvLenguajes_clicked(self,indice):
        #~ print indice.row()
        if indice.parent().row() != -1:
            lenguaje = self.__convertir_a_unicode(indice.parent().data().toString())
            titulo = self.__convertir_a_unicode(indice.data().toString())

            self.mostrar_snippet(lenguaje,titulo)


    def __convertir_a_unicode(self,myQstring):
        return str(myQstring.toUtf8())






from PyQt4.Qsci import *
class TheCodeWidget:
    def __init__(self):

        editor = QsciScintilla()
        self.editor = editor
        self.editor.setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)


        ## define the font to use
        font = QtGui.QFont()
        #~ font.setFamily("Default")
        #~ font.setFixedPitch(True)
        #~ font.setPointSize(10)
        # the font metrics here will help
        # building the margin width later
        fm = QtGui.QFontMetrics(font)

        ## set the default font of the editor
        ## and take the same font for line numbers
        editor.setFont(font)
        editor.setMarginsFont(font)

        ## Line numbers
        # conventionnaly, margin 0 is for line numbers
        editor.setMarginWidth(0, fm.width( "000" ))
        editor.setMarginLineNumbers(0, True)

        ## Edge Mode shows a red vetical bar at 80 chars
        editor.setEdgeMode(QsciScintilla.EdgeLine)
        editor.setEdgeColumn(80)
        editor.setEdgeColor(QtGui.QColor("#FF0000"))

        ## Folding visual : we will use boxes
        #~ editor.setFolding(QsciScintilla.BoxedTreeFoldStyle)

        ## Braces matching
        editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        ## Editing line color
        editor.setCaretLineVisible(True)
        editor.setCaretLineBackgroundColor(QtGui.QColor("#F5F5DC"))

        ## Margins colors
        # line numbers margin
        editor.setMarginsBackgroundColor(QtGui.QColor("#E5E5E5"))
        editor.setMarginsForegroundColor(QtGui.QColor("#1A1A1A"))

        # folding margin colors (foreground,background)
        editor.setFoldMarginColors(QtGui.QColor("#99CC66"),QtGui.QColor("#333300"))

        self.font = font


    def agregar_codigo(self,lenguaje,codigo):
        #diccionario con reemplazos
        equivalentes = {'C++':'CPP','C':'CPP','C#':'CSharp','Html':'HTML',
                        'MsSql':'SQL','Sql':'SQL','Xml':'XML'}
        if lenguaje in equivalentes:
            lenguaje = equivalentes[lenguaje]


        import PyQt4.Qsci
        langs = [i for i in dir(PyQt4.Qsci) if i.startswith('QsciLexer')]

        if 'QsciLexer'+lenguaje in langs:
            ## Choose a lexer
            lexer = globals()['QsciLexer'+lenguaje]()#cargador magico de clases
            #~ lexer.setDefaultFont(self.font)
            self.editor.setLexer(lexer)
            ## Render on screen
            self.editor.show()
            ## Show this file in the editor
            self.editor.setText(codigo)
            pass
        else:
            print 'QsciLexer'+lenguaje+ ' no fue encontrado'
            print langs

    def copiar_al_portapapeles(self):
        pass

    def limpiar(self):
        pass

class TreeViewModel:

    def __init__(self):
        self.__model = self.__crearmodelo()

    def __getModel(self):
       return self.__model

    def __setModel(self, model = None):
       self.__model = model

    def __crearmodelo(self):
        model = QtGui.QStandardItemModel()
        return model

    def insertarEnArbol(self,listaparainsertar):
        #TODO:Limpiar arbol
        self.__model.clear()
        dicdenodos = {}
        for elemento in listaparainsertar:
            if not dicdenodos.has_key(elemento[0]):
                temp = self.__model.invisibleRootItem()
                dicdenodos[elemento[0]] = QtGui.QStandardItem(QtCore.QString(elemento[0]))
                temp.appendRow(dicdenodos[elemento[0]])
            item = QtGui.QStandardItem(QtCore.QString(elemento[1]))
            dicdenodos[elemento[0]].appendRow(item)

    model = property(fget = __getModel, fset = __setModel, doc = None)

def main():
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
