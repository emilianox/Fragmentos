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

from dbutils import DBUtils
from snippetmanager import SnippetManager
from gui import GUI
from configurations import Configurations

class Fragmentos :

    def __init__(self) :
        self.BDU = DBUtils()
        self.ConfigsApp = Configurations()
        self.SM = None #SnippetManager()
        self.GUI = GUI(self)

    def newSnippetManager(self, pathDB):
        ''' Recrea una instancia de SnippetManager 
        a partir de la pathDB indicado.'''
        # recrea la instancia de SM
        self.SM = SnippetManager(pathDB, self.BDU)
        return self.SM
        
def main():
    fragmentos = Fragmentos()

if __name__ == '__main__':
    main()

