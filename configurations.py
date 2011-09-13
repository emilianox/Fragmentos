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


import ConfigParser

import os
from pathtools import PathTools


class MyProperty(object):
    
    def __init__(self, todo, name):
        self.name = name

        self.cfgFile = todo['cfg']
                            
        self.config = todo['config']
        self.config.read(self.cfgFile)
        
        self.__sections = todo['sections']

    def __get__(self, obj, objtype): 
        return self.__getValue(self.name)

    def __set__(self, obj, val):
        self.__setValue(self.name, val)
        
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
        except ConfigParser.NoSectionError:
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
            print section, attribute, value
            self.config.set(section, attribute, value)
            
            self.config.write(open(self.cfgFile,'w'))
        except ConfigParser.NoSectionError:
            print 'No existe la seccion <',section,'>'
        
class Configurations (object) : 

    PT = PathTools()
    # ruta del archivo de configuracion
    cfgFile = PT.getPathCFGFile()
    # 
    config = ConfigParser.ConfigParser()
    
    # valores dentro de la seccion configurations
    configurations_values = {
    "searchPresitionTags" : 0,
    "windowStateStartup" : 0,
    "userUploader" : ''
    }
    
    # valores dentro de la seccion database
    database_values = {
    "defaultBdName" : '',
    "referencesToBds" : ''
    }
    
    # diccionario con las secciones
    sections = {
    'configurations' : configurations_values,
    'database' : database_values 
    }
    
    todo = {'cfg' : cfgFile, 'config' : config, 'sections' : sections}
    
    def __init__(self):
        
        PT = PathTools()
        # ubicacion del archivo de configuracion
        self.cfgFile = PT.getPathCFGFile()
        
        # instancia de configparser
        self.config = ConfigParser.ConfigParser()
        
        # valores dentro de la seccion configurations
        configurations_values = {
        "searchPresitionTags" : 0,
        "windowStateStartup" : 0,
        "userUploader" : ''
        }
        
        # valores dentro de la seccion database
        database_values = {
        "defaultBdName" : '',
        "referencesToBds" : ''
        }
        
        # diccionario con las secciones
        self.sections = {
        'configurations' : configurations_values,
        'database' : database_values 
        }

        
######################
## Metodos PROPERTY ##
######################
    
    defaultBdName = MyProperty(todo, 'defaultBdName')
    searchPresitionTags = MyProperty(todo, 'searchPresitionTags')
    windowStateStartup = MyProperty(todo, 'windowStateStartup')
    referencesToBds = MyProperty(todo, 'referencesToBds')
    userUploader = MyProperty(todo, 'userUploader')
    
#########################
## Metodos de la clase ##
#########################

    def regenerateNewCFG(self) : 
        """ Regenera el archivo cfg. """            
        
        # lee el archivo cfg
        self.config.read(self.cfgFile)
        
        # agrega las secciones
        for section in self.sections :
            #print section
            # crea la seccion
            self.config.add_section(section)
            for atributo in self.sections[section]:
                # agrega el atributo para la seccion actual
                self.config.set(section, atributo,self.sections[section][atributo])
                # print '>',atributo,self.sections[section][atributo]
            
        self.config.write(open(self.cfgFile, 'w'))
        print 'CFG regenerado con exito!!!'
        
    def getDBsInCFGReferences(self):
        ''' Obtiene los path's de las bases de datos ubicadas 
        en el archivo de configuracion.'''
        #~ 
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
        
def main():

    c = Configurations()
    print c.getDBsNamesCFGReferences()
    #~ print c.getDBsInCFGReferences()
    #~ print c.defaulBdName
    #~ c.defaulBdName = "SourceCode"
    #~ c.windowStateStartup = "999"
    #~ print c.windowStateStartup
    
    

if __name__ == '__main__':
    main()
