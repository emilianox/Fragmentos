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

import os
from sys import argv

from members import Members


class PathTools:
    ''' Clase para el manejo de rutas/paths y ubicacion de carpetas. '''
    def __init__(self):
        pass
        
    def getPathDatabasesDir(self):
        ''' Obtiene la ruta del directorio databases segun el so. '''
        program_folder = self.convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
        bd_folder = self.convertPath(os.path.dirname(program_folder[:-1])+'/'+Members.DATABASES_DIR +'/')
        return bd_folder

    def getPathProgramFolder(self):
        ''' Obtiene la ruta de la carpeta del programa. '''
        program_folder = self.convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
        return program_folder

    def getPathCFGFile(self):
        ''' '''
        return self.convertPath(
                            self.getPathProgramFolder() + \
                            Members.CONFIG_DIR + '/' + Members.CFG_FILE)
    
    def getPathDataDir(self):
        ''' '''
        return self.convertPath(
                        self.getPathProgramFolder() + \
                                Members.CONFIG_DIR )
                                
    def convertPath(self,path):
        '''Convierte el path a el específico de la plataforma (separador)'''
        if os.name == 'posix':
            return "/"+apply( os.path.join, tuple(path.split('/')))
        elif os.name == 'nt':
            return apply( os.path.join, tuple(path.split('/')))


if __name__ == '__main__':
    pt = PathTools()
    print pt.getPathCFGFile()
    pass
