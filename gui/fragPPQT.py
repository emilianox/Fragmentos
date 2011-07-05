#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import os,sys
from PyQt4 import QtCore, QtGui, uic# Importamos los módulos de Qt
import fragmentos_rc #Importo los iconos

class Main(QtGui.QMainWindow):
    """La ventana principal de la aplicación."""
    def __init__(self,parent):
    #Boludeces de instancias
        self.SM = parent.SM
    #Cargar archivo ui
        FILENAME = 'fragPP.ui'
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        QtGui.QMainWindow.__init__(self)
        uic.loadUi(uifile, self)
    #Treeview agregado
        self.mytreeview = TreeViewModel(self.tvLenguajes,self.on_tvLenguajes_selectedItem,self.connect)
        self.mytreeview.insertarEnArbol(self.SM.getLengsAndTitles())
    #Detalles de armado interfaz
      #Widget codigo
        self.widgetcodigo = TheCodeWidget()
        self.spPrincipal.addWidget(self.widgetcodigo.editor)
        #Reordenamiento  y expancion
        self.spPrincipal.setSizes([50,900])#ni idea pero no tocar
        #colores x defecto
        self.colorBusqueda = MyQcolorTextEdit(self.eBusqueda)

        bds = self.SM.getBDNames()
        for item in bds:
            self.cbBD.addItem(item)

        self.mmm.setMenu(self.menuHello)


############
## Metods ##
############
    def mostrar_snippet(self,lenguaje,titulo):
        snippet = self.SM.getSnippet(lenguaje,titulo)
        #con lo anterior busca en SM el codigo
        self.widgetcodigo.agregar_codigo(snippet.getLenguaje(),snippet.getCodigo())

    def __convertir_a_unicode(self,myQstring):
        return str(myQstring.toUtf8())

############
## Events ##
############
    def on_eBusqueda_textChanged(self,cadena):
        #campo de pruebas en la busqueda
        datos = self.SM.getLengsAndTitles(str(self.__convertir_a_unicode(cadena)))
        if datos != []:
            self.colorBusqueda.set_color_busqueda()
            self.mytreeview.insertarEnArbol(datos)
            self.tvLenguajes.expandAll()
        else:
            self.colorBusqueda.set_color_busqueda(False)
            self.mytreeview.model.clear()
            self.tvLenguajes

    def on_tvLenguajes_selectedItem(self,indice,b):
        #~ print indice.row()
        if indice.parent().row() != -1:
            lenguaje =  indice.parent().data().toString().toUtf8()#.encode('ascii','utf-8')
            titulo =  unicode(indice.data().toString().toUtf8(),'utf-8')
            self.mostrar_snippet(unicode(lenguaje,'utf-8'),titulo)



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
        font.setPointSize(10)
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
        equivalentes = {'C++':'CPP','Css':'CSS','C':'CPP','C#':'CSharp','Html':'HTML',
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

    def __init__(self, treeview,metodo,conector):
        self.__model = self.__crearmodelo()
        #~ self.__treeview = treeview
        treeview.setModel(self.__model)
        SelectionModel = QtGui.QItemSelectionModel( self.__model,treeview)
        treeview.setSelectionModel(SelectionModel)
        conector(SelectionModel, QtCore.SIGNAL(
            "currentChanged(const QModelIndex &, const QModelIndex &)"),
            metodo)
        self.__treeview = treeview


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


class MyQcolorTextEdit:
    def __init__(self,TextEdit):
        #sacarle el color a textedit
        self.__txt = TextEdit
        self.__palette = self.__txt.palette()
        self.__defaultcolortext = self.__txt.palette().color(
                                    QtGui.QPalette.Active, QtGui.QPalette.Text).getRgb()[:-1]
        self.__defaultcolorbase = self.__txt.palette().color(
                                    QtGui.QPalette.Active, QtGui.QPalette.Base).getRgb()[:-1]
        #colores
        self.__blanco = QtGui.QColor(255, 255, 255)
        self.__rojito = QtGui.QColor(255, 102, 102)
        self.__defaulttext = QtGui.QColor(self.__defaultcolortext[0],self.__defaultcolortext[1],
                                        self.__defaultcolortext[2])
        self.__defaultbase = QtGui.QColor(self.__defaultcolorbase[0],self.__defaultcolorbase[1],
                                        self.__defaultcolorbase[2])

    def set_color_busqueda(self,estado=True):
        if estado:
            textcolor = self.__defaulttext
            basecolor = self.__defaultbase
        else:
            textcolor = self.__blanco
            basecolor = self.__rojito

        self.__palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Text,textcolor)
        self.__palette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base,basecolor)
        self.__txt.setPalette(self.__palette)

        return True
        #return confirmacion si cambio de color

def main():
    pass

if __name__ == "__main__":
    main()
