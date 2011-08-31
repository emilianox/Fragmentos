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
from members import Members
from dbutils import DBUtils
from configurations import Configurations

class Validator :
    
    def __init__(self) :
        self.dbu = DBUtils()
        self.config = Configurations()
        
        
    def checkFolders (self) :
        """ Verifica que existan los directorios de la aplicación """
        
        # obtiene la ruta del directorio /databases
        databases_dir = self.dbu.convertPath(
                            self.dbu.getPathDatabasesDir())
        
        # si no existe el directorio, lo crea
        if not os.path.exists(databases_dir) :
            print 'El directorio /databases no existia, ha sido creado nuevamente.'
            os.mkdir(databases_dir)
            
        # obtiene la ruta del directorio /data
        data_dir = self.dbu.convertPath(
                        self.dbu.getPathProgramFolder() + \
                                Members.CONFIG_DIR )
        
        # si no existe el directorio, lo crea
        if not os.path.exists(data_dir) :
            print 'El directorio /data no existia, ha sido creado nuevamente.'
            os.mkdir(data_dir)
        
    def checkExistCfg (self) :
        """ Verifica la existencia del archivo de configuracion """
        
        existe = False
        path_cfg = self.dbu.convertPath(
                        self.dbu.getPathProgramFolder() + \
                        Members.CONFIG_DIR + '/' + Members.CFG_FILE)
        if not os.path.exists(path_cfg):
            self.config.regenerateNewCFG()
            existe = True
        return existe
        
    def checkIntegrityCfg (self) :
        """ Verifica la integridad del archivo de configuracion """
        # returns
        pass
        
    def check (self) :
        
        # verifica la existencia de los directorios
        self.checkFolders()
        
        # verifica la existencia del archivo de configuracion 
        self.checkExistCfg()
        
        # verifica la integridad del archivo de configuracion 
        self.checkIntegrityCfg()
        


def main():

    v = Validator()
    v.checkFolders()
    

if __name__ == '__main__':
    main()

