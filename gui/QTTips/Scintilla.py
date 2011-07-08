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

from PyQt4 import QtGui
from PyQt4.Qsci import *

class Scintilla:
    
    def __init__(self):

        editor = QsciScintilla()
        editor.setSizePolicy(QtGui.QSizePolicy.Ignored,QtGui.QSizePolicy.Ignored)

        ## define the font to use
        font = QtGui.QFont()
        #~ font.setFamily("Default")
        #~ font.setFixedPitch(True)
        font.setPointSize(8)
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
        #~ editor.setEdgeMode(QsciScintilla.EdgeLine)
        #~ editor.setEdgeColumn(80)
        #~ editor.setEdgeColor(QtGui.QColor("#FF0000"))

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

        self.__editor = editor
        self.__font = font
        
        #
        self.__equivalentes = {
        'C++':'CPP',
        'Css':'CSS',
        'C':'CPP',
        'C#':'CSharp',
        'Html':'HTML',
        'MsSql':'SQL',
        'Sql':'SQL',
        'Xml':'XML'
        }
        
    def getLanguages(self):
        ''' '''
        #TODO: devolver junto con los sci lenguajes, los reemplazos
        import PyQt4.Qsci
        langs = [i for i in dir(PyQt4.Qsci) if i.startswith('QsciLexer')]
        langs = langs[1:]
        lenguajes = []
        for lang in langs:
            lenguajes.append(lang[9:])
        return lenguajes
        
        
    def getCode(self):
        ''' '''
        return self.__editor.text()
        
    def getEditor(self):
        ''' '''
        return self.__editor
    
    def setLanguage(self,lenguaje):
        ''' Establece el coloreo de sintaxis correspondiente. '''
        
        if lenguaje in self.__equivalentes:
            lenguaje = self.__equivalentes[lenguaje]
            
        import PyQt4.Qsci
        langs = [i for i in dir(PyQt4.Qsci) if i.startswith('QsciLexer')]

        if 'QsciLexer'+lenguaje in langs:
            ## Choose a lexer
            lexer = globals()['QsciLexer'+lenguaje]()#cargador magico de clases
            #~ lexer.setDefaultFont(self.__font)
            self.__editor.setLexer(lexer)
            ## Render on screen
            self.__editor.show()
            ## Show this file in the editor
            #~ self.__editor.setText(codigo)
        else:
            print 'QsciLexer'+lenguaje+ ' no fue encontrado'
            #~ print langs
            
    def setCode(self,codigo):
        ''' '''
        ## Show this file in the editor
        self.__editor.setText(codigo)

    def setFullCode(self,codigo,lenguaje):
        ''' '''
        self.setCode(codigo)
        self.setLanguage(lenguaje)
        
    def copyToClipboard(self):
        pass

    def clearCode(self):
        pass
        
