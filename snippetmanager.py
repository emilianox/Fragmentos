#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       Copyright 2011 Ferreyra, Jonathan <jalejandroferreyra@gmail.com>
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

from bd import BD
from bdutils import BdUtils
from snippet import Snippet

class SnippetManager:
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase GUI'''
    
    def __init__(self):
        self.BU = BdUtils()
        self.__pathBDInUse = self.BU.getPathDatabasesDir()+'SourceCode.db'#MOMENTANEOOOOOOOOOOOOOOOOOOO!!!
        self.BD = BD(self.__pathBDInUse)

##########################
## Metodos de instancia ##
##########################
    def agregarSnippet(self):
        pass

    def modificarSnippet(self):
        pass
    
    def eliminarSnippet(self):
        pass

#################
## Metodos Get ##
#################
    def getLenguajesFromBD(self):
        ''' Obtiene una lista de los lenguajes desde la bd.'''
        return self.BD.getLenguajes()

    def getBDNames(self):
        return self.BU.getBDsNames()

    def getAllSnippetsFromBD(self):
        ''' Obtiene los snippets desde la bd.'''
        return self.BD.getAllSnippets()
    
    def getLengsAndTitlesFromBD(self):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        return self.BD.getLengAndTitles()
        
    def getPathProgramFolder(self):
        ''' Obtiene la ruta de la carpeta del programa. '''
        import os
        from sys import argv
        program_folder = self.convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
        return program_folder
        
    def getSnippetFromBD(self,lenguaje,titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        from snippet import Snippet
        miSnippet = Snippet(self.BD.getSnippet(lenguaje,titulo))
        return miSnippet

#################
## Metodos Set ##
#################
    def setPathBDInUse(self,path):
        self.__pathBDInUse = path
        
######################
## Metodos Privados ##
######################
    def convertPath(self,path):
        """Convierte el path a el específico de la plataforma (separador)"""
        import os
        if os.name == 'posix':
            return "/"+apply( os.path.join, tuple(path.split('/')))
        elif os.name == 'nt':
            return apply( os.path.join, tuple(path.split('/')))
