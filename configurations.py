#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Informática MEG <contacto@informaticameg.com>
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


import ConfigParser
import os
from pathtools import PathTools

        
class Configurations (object) : 

    def __init__(self):
        
        PT = PathTools()
        # ubicacion del archivo de configuracion
        self.cfgFile = PT.getPathCFGFile()
        
        # instancia de configparser
       
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.cfgFile)
        
        self.__searchPresitionTags = None
        self.__windowStateStartup = None
        self.__userUploader = None
        self.__expandTree = None
        self.__defaultBdName = None
        self.__referencesToBds = None
        
        # valores dentro de la seccion configurations
        configurations_values = {
        "searchpresitiontags" : 0,
        "windowstatestartup" : 0,
        "useruploader" : '',
        "expandtree" : 0
        }
        
        # valores dentro de la seccion database
        database_values = {
        "defaultbdName" : '',
        "referencestobds" : ''
        }
        
        # diccionario con las secciones
        self.__sections = {
        'configurations' : configurations_values,
        'database' : database_values }

    def __getValue(self, attribute):
        """ Recupera del archivo de configuracion el  
        valor del atributo indicado. """
        
        section = ''
        # recorre el diccionario buscando la seccion a la que 
        # pertenece el atributo
        for elemento in self.__sections : 
            if attribute in self.__sections[elemento].keys():
                section = elemento
        try:
            # obtiene el valor desde el cfg
            return self.config.get(section, attribute)            
        except ConfigParser.NoSectionError, msg:
            print 'No existe la seccion <',section,'>'
            return None
    
    def __setValue(self, attribute, value):
        """ Establece en el archivo de configuracion el  
        valor del atributo indicado. """
        
        section = ''
        # recorre el diccionario buscando la seccion a la que 
        # pertenece el atributo
        for elemento in self.__sections : 
            if attribute in self.__sections[elemento].keys():
                section = elemento
        try:
            # establece el valor en el cfg
            self.config.set(section, attribute, value)
            
            self.config.write(open(self.cfgFile,'w'))
        except ConfigParser.NoSectionError:
            print 'No existe la seccion <',section,'>'
            
    def __get_search_presition_tags(self):
        return self.__getValue('searchpresitiontags')


    def __get_window_state_startup(self):
        return self.__getValue('windowstatestartup')


    def __get_user_uploader(self):
        return self.__getValue('useruploader')


    def __get_expand_tree(self):        
        return self.__getValue('expandtree')


    def __get_default_bd_name(self):
        return self.__getValue('defaultbdname')


    def __get_references_to_bds(self):
        return self.__getValue('referencestobds')


    def __set_search_presition_tags(self, value):
        self.__setValue('searchpresitiontags',value)


    def __set_window_state_startup(self, value):
        self.__setValue('windowstatestartup',value)


    def __set_user_uploader(self, value):
        self.__setValue('useruploader',value)


    def __set_expand_tree(self, value):
        self.__setValue('expandtree', value)


    def __set_default_bd_name(self, value):
        self.__setValue('defaultbdName',value)


    def __set_references_to_bds(self, value):
        self.__setValue('referencestobds',value)


######################
## Metodos PROPERTY ##
######################
    
    searchPresitionTags = property(__get_search_presition_tags, __set_search_presition_tags, None, None)
    windowStateStartup = property(__get_window_state_startup, __set_window_state_startup, None, None)
    userUploader = property(__get_user_uploader, __set_user_uploader, None, None)
    expandTree = property(__get_expand_tree, __set_expand_tree, None, None)
    defaultBdName = property(__get_default_bd_name, __set_default_bd_name, None, None)
    referencesToBds = property(__get_references_to_bds, __set_references_to_bds, None, None)

#########################
## Metodos de la clase ##
#########################

    def regenerateNewCFG(self) : 
        """ Regenera el archivo cfg. """            
        
        # lee el archivo cfg
        self.config.read(self.cfgFile)
        
        # agrega las secciones
        for section in self.__sections :
            # crea la seccion
            self.config.add_section(section)
            for atributo in self.__sections[section]:
                # agrega el atributo para la seccion actual
                self.config.set(section, atributo,self.__sections[section][atributo])
            
        self.config.write(open(self.cfgFile, 'w'))
        print 'CFG regenerado con exito!!!'
        
    def getDBsInCFGReferences(self):
        ''' Obtiene los path's de las bases de datos ubicadas 
        en el archivo de configuracion.'''
        if self.referencesToBds != None :
            paths_cfg = self.referencesToBds.strip()
            if paths_cfg :
                #~ separa las rutas obtenidas
                a_comprobar = paths_cfg.split(',')
    
                #~ comprueba que existan estos archivos, retornando
                #~ solo aquellas rutas que sean validas
                rutas_validas = filter(os.path.exists,a_comprobar)
                return rutas_validas
        else:
            return []
            
        
    def getDBsNamesCFGReferences(self):
        '''Obtiene una lista con los nombres de los archivos bds en el CFG.'''
        
        rutas = self.getDBsInCFGReferences()
        bd_names = []
        if rutas : 
            for ruta in rutas:
                # recupera el nombre del archivo
                nombre_bd = os.path.splitext(os.path.basename(ruta))
                # lo agrega a la lista
                bd_names.append(nombre_bd[0])
        return bd_names
        
    def quitarDBInCFGReference(self, path_reference):
        rutas = self.getDBsInCFGReferences()
        if path_reference in rutas :
            rutas.remove( path_reference )
            self.referencesToBds = ','.join( rutas )
        
def main():
    pass
    

if __name__ == '__main__':
    main()
