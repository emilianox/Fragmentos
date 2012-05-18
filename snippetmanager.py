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

from database import Database
from snippet import Snippet
from pathtools import PathTools


class SnippetManager:
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase Fragmentos'''

    def __init__(self, DBUtils, Configs):
        
        # class instances
        self.__DBUtils = DBUtils
        self.__PT = PathTools()
        self.__Configs = Configs
        
        # private instances
        self.__BD = None
        # diccionario con todas las instancia de objeto Snippet
        self.__Snippets = None
        # objeto snippet mostrado actualmente en GUI
        self.__SnippetActual = None # Snippet
        
        # esta variable, se utilizara para saber si la instancia de 
        # snippetmanager se creo correctamente con una bd determinada
        # o se creo vacia, indicando que no se puede realizar ninguna
        # operacion sobre la aplicacion 
        self.__estado = False
        
        # lista con las rutas de las base de datos
        # tanto las del pathdefault como del cfg file
        self.__AllPathDBs = []
        self.loadAllPathDBs()
        
        # trae si existe, el valor de la bd a cargar por defecto
        defaultBdName = self.__Configs.defaultBdName
        if defaultBdName :          
            # obtiene el indice de la ruta de la bd a cargarce 
            pathBD = self.getPathBD(
                                self.getIndexBdName(defaultBdName))
            # crea la instancia de el catalogo en cuestion 
            self.__BD = Database(pathBD)
            
            # instancia creada correctamente
            self.__estado = True
            
        elif self.__AllPathDBs:
            # sino, se carga la primer bd encontrada en la lista de bds
            self.__BD = Database(
                        self.getPathDB(0))
        
            # diccionario con todas las instancia de objeto Snippet
            self.__Snippets = self.getAllSnippets()
            
            # instancia creada correctamente
            self.__estado = True                    

##########################
## Metodos de instancia ##
##########################

    def agregarSnippet(self, datosSnippet):
        ''' Recibe un dicionario de los datos de lo que sera un nuevo
        snippet y lo agrega a la BD.'''
        
        # llama al metodo de bd para agregar un snippet, devolviendo
        # el resultado de la operacion como boolean y en caso de error, 
        # el mensaje del error.
        resultado, mensaje = self.__BD.agregarSnippet(datosSnippet)
        if resultado:
            # crea una instancia del nuevo snippet
            newSnippet = Snippet(datosSnippet, self.__BD)
            # agrega el nuevo snippet a los ya existentes
            self.__addNewSnippetToCollection(newSnippet)
            # retorna que la operacion fue exitosa, 
            #  y ningun mensaje de error
            return True, None
        else:
            # retorna que la operacion no fue exitosa, y 
            # el mensaje de error devuelto por bd
            return False,mensaje

    def eliminarSnippet(self, unSnippet):
        ''' Manda a eliminarSnippet de la Bd que
        borre el snippet segun su titulo y lenguaje.'''
        
        # llama al metodo de bd para eliminar un snippet
        # y devuelve un booleano con el resultado de la operacion.
        if self.__BD.eliminarSnippet(
            unSnippet.titulo, unSnippet.lenguaje):
                # quita del diccionario el snippet
                self.__Snippets.pop((unSnippet.lenguaje,
                                        unSnippet.titulo))
                # establece como actual snippet a None
                self.__SnippetActual = None
                return True
        else:
            return False

    def modificarSnippet(self, clave_spviejo, snippet_nuevo):
        ''' Actualiza el snippet cargado en memoria'''
        del self.__Snippets[clave_spviejo]
        self.__Snippets[
                (snippet_nuevo.lenguaje,snippet_nuevo.titulo)
                    ] = snippet_nuevo

    def newSnippet(self, tuplaSnippet):
        ''' Crea una instancia de snippet. '''
        
        # a partir de los valores que vienen en la tupla, 
        # se crea una instancia de snippet con dichos valores.
        nuevoSnippet = Snippet({
            'title':tuplaSnippet[0],
            'language':tuplaSnippet[1],
            'tags':tuplaSnippet[2],
            'contens':tuplaSnippet[3],
            'description':tuplaSnippet[4],
            'creation':tuplaSnippet[5],
            'reference':tuplaSnippet[6],
            'modified':tuplaSnippet[7],
            'uploader':tuplaSnippet[8],
            'starred':tuplaSnippet[9]},
            self.__BD)
            
        # tupla que sera de clave en el diccionario de los snippets
        clave = (tuplaSnippet[1],tuplaSnippet[0])
        
        elemento_diccionario = (clave,nuevoSnippet)

        return elemento_diccionario

    def __addNewSnippetToCollection(self, newSnippet):
        ''' Agrega el nuevo snippet creado a la coleccion actual de snippets. '''
        self.__Snippets.update(
            {(newSnippet.lenguaje, newSnippet.titulo):newSnippet})

#################
## Metodos Get ##
#################

    def getAllLenguajes(self):
        ''' Obtiene una lista de los lenguajes desde la bd.'''
        
        # obtiene desde la actual instancia de bd los lenguajes existentes 
        all_lenguajes = self.__BD.getLenguajes()
        lenguajes = []
        # saca de la tupla y carga en la lista los lenguajes obtenidos
        #~ for lenguaje in all_lenguajes:
            #~ lenguajes.append(lenguaje[0])
        map(lambda lenguaje: lenguajes.append(lenguaje[0]), all_lenguajes)
        return lenguajes

    def getBDNames(self):
        ''' Obtiene una lista con los nombres de los archivos bds.'''
        databases_dir = self.__DBUtils.getBDsNamesDatabasesDir()
        cfg_file = self.__Configs.getDBsNamesCFGReferences()
        return databases_dir + cfg_file
        
    def getDB(self):
        return self.__BD
    
    def getAllSnippets(self):
        ''' Obtiene los snippets desde la bd y carga en un diccionario
        los snippets en formato objeto Snippet().'''
        
        # obtiene desde la bd todos los snippets,
        # orden en que vienen los campos
        # 1-title,2-language,3-tags,4-contens,5-description
        # 6-creation,7-reference,8-modified,9-uploader,10-starred
        all_snippets = self.__BD.getAllSnippets()
        
        # se aplica map para crear por cada tupla obtenida desde la bd
        # una tupla de tuplas donde el formato resultante es:
        # (claveSnippet : instanciaSnippet)
        todos_los_snippets = map(self.newSnippet,all_snippets)
        
        # dict(), convierte la tupla de tuplas a diccionario
        return dict(todos_los_snippets)

    def getInstanceState(self):
        ''' '''
        return self.__estado
    
    def getIndexBdName(self, bdName):
        ''' Busca en la lista de bds la ocurrencia de la primer bd que 
        coincida con el nombre del parametro <bdName>, devolviendo la 
        posicion en que se encuentra. 
        Devuelve -1 si no se encuentra. '''
        
        return self.__AllPathDBs.index(bdName)
        
    def getLengsAndTitles(self,consulta=None, favorito = None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        #~ tagsPresicion = bool(self.__DBUtils.configs.searchPresitionTags)
        tagsPresicion = False
        return self.__BD.getLengAndTitles(consulta, favorito, tagsPresicion)

    def getSnippet(self, lenguaje, titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        try:
            # del diccionario donde estan todas las instancias de snippet,
            # a partir de la clave tupla, recupera la instancia
            # con lenguaje y titulo indicado 
            snippet = self.__Snippets[(lenguaje,titulo)]
            
            # establece como instancia actual en uso, la instancia obtenida
            self.setSnippetActual(snippet)
        except Exception, msg:
            # si el snippet no esta en el diccionario, devuelve None
            snippet = None
            self.setSnippetActual(snippet)
            print 'getSnippet Error: ',msg
        return snippet

    def getSnippetsCount(self):
        ''' Devuelve un entero con la cantidad de snippets cargados en la BD.'''
        return self.__BD.getSnippetsCount()

    def getSnippetActual(self):
        ''' Devuelve la instancia actual del objeto Snippet. '''
        return self.__SnippetActual

    def getAllPathDBs(self):
        # devuelve la lista con las rutas de las bd actuales
        return self.__AllPathDBs

    def getPathDB(self, index):
        ''' Recupera de la lista de bds la ruta en el indice especificado.'''
        return self.__AllPathDBs[index]

#################
## Metodos Set ##
#################

    def setDB(self, pathBD):
        '''Crea una instancia de BD'''
        self.__BD = Database(pathBD)
        # se vuelven a reobtener los snippets desde esta nueva bd        
        self.__Snippets = self.getAllSnippets()
        
    def setSnippetActual(self, unSnippet):
        ''' Establece los datos del Snippet usado actualmente.'''
        self.__SnippetActual = unSnippet

    def loadAllPathDBs(self):
        ''' Obtiene todsa las rutas de las bds incluidas en
        el dir databases y el CFG '''        
        
        databases_dir = self.__DBUtils.getBDsInDatabasesDir()
        #TODO: implementar estooo
        databases_cfg = self.__Configs.getDBsInCFGReferences()
        if databases_cfg :
            self.__AllPathDBs = databases_dir + databases_cfg
        else:
            self.__AllPathDBs = databases_dir
