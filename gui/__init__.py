#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
#
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

#TODO: por ahoraaaaaaaaaaaa!!!!
#~ from tips import *
import MainForm
from PyQt4 import QtGui
import sys
#~ from fragmentos import Fragmentos

class GUI():
    def __init__(self,parent) :
        self.fragmentos = parent
        self.SM = parent.SM

        app = QtGui.QApplication(sys.argv)
        self.window = MainForm.Main(self)
        self.window.show()
        sys.exit(app.exec_())

    def newSnippetManager(self,pathDB):
        ''' Recrea una instancia de SnippetManager 
        a partir de la pathDB indicado.'''
        self.SM = self.fragmentos.newSnippetManager(pathDB)
        return self.SM
        print 'nueva instancia de SM creada desde -GUI-'
        
    def setSMInstance(self,newSM):
        ''' Establece la referencia de la nueva instancia creada. '''
        self.SM = newSM
    
    def showAgregarSnippet(self):
        ''' '''
        from agregarSnippet import agregarSnippet
        self.agregar = agregarSnippet(self)
        self.agregar.show()
        
        
def main():
    G = GUI()


if __name__ == '__main__':
    main()

