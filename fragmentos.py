#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from gui import GUI
from snippetmanager import SnippetManager
from configurations import Configurations

class Fragmentos :
    ''' Clase que hace de puente entre la logica del programa con las interfaces graficas. '''
    
    def __init__(self) :
        self.BDU = DBUtils()
        self.ConfigsApp = Configurations()
        self.SM = SnippetManager(self.BDU, self.ConfigsApp)
        self.GUI = GUI(self)
        
def main():
    Fragmentos()

if __name__ == '__main__':
    main()

