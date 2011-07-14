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

from database import Database
from snippet import Snippet

class SnippetManager:
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase Fragmentos'''

    def __init__(self, pathBD = False, DBUtils = None):
        self.__DBUtils = DBUtils
        #lista con las rutas de las base de datos
        self.__AllPathDBs = self.setAllPathDBs()
        if not pathBD:
            pathBD = self.__AllPathDBs[0]
        #~ print pathBD
        self.__BD = Database(pathBD)
        #diccionario con todas las instancia de objeto Snippet
        self.__Snippets = self.getAllSnippets()
        #objeto snippet mostrado actualmente en GUI
        self.__SnippetActual = None # Snippet

##########################
## Metodos de instancia ##
##########################

    def agregarSnippet(self, datosSnippet):
        ''' Recibe un dicionario de los datos de lo que sera un nuevo
        snippet y lo agrega a la BD.'''
        
        resultado, mensaje = self.__BD.agregarSnippet(datosSnippet)
        if resultado:
            #crea una instancia del nuevo snippet
            newSnippet = Snippet(datosSnippet, self.__BD)
            #~ print '\n valores snippet : ',datosSnippet
            #lo agrega a los snippets ya existentes
            self.__addNewSnippetToCollection(newSnippet)
            return True, None
        else:
            return False,mensaje

    def eliminarSnippet(self, unSnippet):
        ''' Manda a eliminarSnippet de la Bd que
        borre el snippet segun su titulo y lenguaje.'''
        if self.__BD.eliminarSnippet(
            unSnippet.titulo, unSnippet.lenguaje):
                #quita del diccionario el snippet
                self.__Snippets.pop((unSnippet.lenguaje,
                                        unSnippet.titulo))
                #establece como actual snippet a None
                self.__SnippetActual = None
                return True
        else:
            return False

    def newSnippet(self,tuplaSnippet):
        ''' Crea una instancia de snippet. '''
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
        clave = (tuplaSnippet[1],tuplaSnippet[0])
        elemento_diccionario = (clave,nuevoSnippet)

        return elemento_diccionario

    def __addNewSnippetToCollection(self,newSnippet):
        ''' Agrega el nuevo snippet creado a la coleccion actual de snippets. '''
        self.__Snippets.update(
            {(newSnippet.lenguaje, newSnippet.titulo):newSnippet})

#################
## Metodos Get ##
#################

    def getAllLenguajes(self):
        ''' Obtiene una lista de los lenguajes desde la bd.'''
        all_lenguajes = self.__BD.getLenguajes()
        lenguajes = []
        for lenguaje in all_lenguajes:
            lenguajes.append(lenguaje[0])
        return lenguajes

    def getBDNames(self):
        ''' Obtiene una lista con los nombres de los archivos bds.'''
        return self.__DBUtils.getBDsNames()

    def getAllSnippets(self):
        ''' Obtiene los snippets desde la bd y carga en un diccionario
        los snippets en formato objeto Snippet().'''
        #orden en que vienen los campos
        #1-title,2-language,3-tags,4-contens,5-description
        #6-creation,7-reference,8-modified,9-uploader,10-starred
        all_snippets = self.__BD.getAllSnippets()
        #devuelve tuplas de: (claveSnippet : instanciaSnippet)
        todos_los_snippets = map(self.newSnippet,all_snippets)
        #dict(), convierte la tupla de tuplas a diccionario
        return dict(todos_los_snippets)

    def getLengsAndTitles(self,consulta=None, favorito = None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        return self.__BD.getLengAndTitles(consulta, favorito)

    def getSnippet(self,lenguaje,titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        try:
            snippet = self.__Snippets[(lenguaje,titulo)]
            self.setSnippetActual(snippet)
        except Exception:
            #si el snippet no esta en el diccionario, devuelve None
            snippet = None
            self.setSnippetActual(snippet)
        return snippet

    def getSnippetsCount(self):
        ''' Devuelve un entero con la cantidad de snippets cargados en la BD.'''
        return self.__BD.getSnippetsCount()

    def getSnippetActual(self):
        ''' Devuelve la instancia actual del objeto Snippet. '''
        return self.__SnippetActual

    def getAllPathDBs(self):
        return self.__AllPathDBs

    def getPathDB(self,index):
        ''' Recupera de la lista de bds la ruta en el indice especificado.'''
        return self.__AllPathDBs[index]

#################
## Metodos Set ##
#################

    def setDB(self,pathBD):
        '''Crea una instancia de BD'''
        self.__BD = Database(pathBD)

    def setSnippetActual(self,unSnippet):
        ''' Establece los datos del Snippet usado actualmente.'''
        self.__SnippetActual = unSnippet

    def setAllPathDBs(self):
        ''' Obtiene todsa las rutas de las bds incluidas en
        el dir databases y el CFG '''
        
        #TODO: llevar estas instrucciones a BDUTILS.
        
        databases_dir = self.__DBUtils.getBDsInDatabasesDir()
        #TODO: implementar estooo
        databases_cfg = []
        return databases_dir + databases_cfg
