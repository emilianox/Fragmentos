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
from pathtools import PathTools
from configurations import Configurations

class Validator :
    ''' Clase que valida el estado de distintas partes del programa. '''
    
    def __init__(self) :
        self.pt = PathTools()
        self.config = Configurations()
        
        
    def checkFolders (self) :
        """ Verifica que existan los directorios de la aplicación """
        
        # obtiene la ruta del directorio /databases
        databases_dir = self.pt.getPathDatabasesDir()
        
        # si no existe el directorio, lo crea
        if not os.path.exists(databases_dir) :
            print 'El directorio /databases no existia, ha sido creado nuevamente.'
            os.mkdir(databases_dir)
            
        # obtiene la ruta del directorio /data
        data_dir = self.pt.getPathDataDir()
        
        # si no existe el directorio, lo crea
        if not os.path.exists(data_dir) :
            print 'El directorio /data no existia, ha sido creado nuevamente.'
            os.mkdir(data_dir)
        
    def checkExistCfg (self) :
        """ Verifica la existencia del archivo de configuracion """
        
        existe = False
        path_cfg = self.pt.getPathCFGFile()
        
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
        #self.checkIntegrityCfg()
 
import gconf #@UnresolvedImport
import types
class ValidarShorcuts:
    """"""
    def __init__(self):
        self.search_key = 'F7'
        self.add_key = 'F9'
        self.file = self.__validar_file()
        self.client = gconf.client_get_default()
        self.__validar_keys()
        
        
 
    def __check_search_key(self):
        self.set_key('/desktop/gnome/keybindings/fragmentos-search/binding',self.search_key)
        self.set_key('/desktop/gnome/keybindings/fragmentos-search/action','python ' + self.file + ' -search')
        self.set_key('/desktop/gnome/keybindings/fragmentos-search/name','search into fragmentos')
        pass
    
    def __check_add_key(self):
        self.set_key('/desktop/gnome/keybindings/fragmentos-add/binding',self.add_key)
        self.set_key('/desktop/gnome/keybindings/fragmentos-add/action','python ' + self.file +' -add')
        self.set_key('/desktop/gnome/keybindings/fragmentos-add/name','add to fragmentos')
        pass

    def __validar_keys(self):
        self.__check_search_key()
        self.__check_add_key()
        pass

    def __validar_file(self):
        p= PathTools()
        return p.getPathProgramFolder()+'cliente_dbus.py'
        

    def set_key(self,key,value):
        casts = {types.BooleanType: gconf.Client.set_bool,
                 types.IntType:     gconf.Client.set_int,
                 types.FloatType:   gconf.Client.set_float,
                 types.StringType:  gconf.Client.set_string}
        casts[type(value)](self.client,key, value)

    def get_key(self,key):
        try:
            casts = {gconf.VALUE_BOOL:   gconf.Value.get_bool,
                     gconf.VALUE_INT:    gconf.Value.get_int,
                     gconf.VALUE_FLOAT:  gconf.Value.get_float,
                     gconf.VALUE_STRING: gconf.Value.get_string}
            value = self.client.get(key)
            return casts[value.type](value)
        except AttributeError:
            raise ValueError
 
        
class Vacia:
    def __init__(self):
        pass


def main():

    v = Validator()
    v.checkFolders()
    

if __name__ == '__main__':
    main()

