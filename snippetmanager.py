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
from dbutils import DBUtils
from snippet import Snippet
from configurations import Configurations

class SnippetManager:
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase Fragmentos'''

    def __init__(self,pathBD=False):
        self.__DBUtils = DBUtils()
        self.__AllPathDBs = self.setAllPathDBs()
        if not pathBD :
            pathBD = self.__AllPathDBs[0]
        #~ print pathBD
        self.__BD = Database(pathBD)
        self.__Snippets = self.getAllSnippets()

        self.__SnippetActual = None # Snippet

##########################
## Metodos de instancia ##
##########################

    def agregarSnippet(self,dicdecosas):
        ''' Recibe un diccionario de las cosas que debe guardar
        y carga los datos en una lista para agregarlos a la BD.'''
        #TODO: convertir a diccionario,debe recibir
        #el diccionario('titulo':'un titulo cualquiera', etc)
        #y generar o devolver a algun metodo de bd para que se agrege.
        datosSnippet = []
        datosSnippet.append(titulo)
        datosSnippet.append(tags)
        datosSnippet.append(lenguaje)
        datosSnippet.append(contenido)
        datosSnippet.append(detalles)
        datosSnippet.append(fecha)
        datosSnippet.append(referencias)
        self.__BD.agregarSnippet(datosSnippet)

    def eliminarSnippet(self,unSnippet):
        ''' '''
        self.__BD.eliminarSnippet(unSnippet)

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
        clave = ()
        todos_los_snippets = {}
        #orden en que vienen los campos
        #1-title,2-language,3-tags,4-contens,5-description
        #6-creation,7-reference,8-modified,9-uploader,10-starred
        all_snippets = self.__BD.getAllSnippets()
        #itera convirtiendo el resultado de la bd, en una
        #coleccion de instancias de Snippet()
        for actual in all_snippets:
            #obtengo la clave del snippet
            clave = (actual[1],actual[0])#snippet[0] = title, snippet[1] = language
            #se crea una instancia de snippet con los datos actuales
            snippet = Snippet({
            'title':actual[0],
            'language':actual[1],
            'tags':actual[2],
            'contens':actual[3],
            'description':actual[4],
            'creation':actual[5],
            'reference':actual[6],
            'modified':actual[7],
            'uploader':actual[8],
            'starred':actual[9]},
            self.__BD)
            #diccionario auxiliar
            elemento_diccionario = {clave:snippet}
            #carga este snippet en el diccionario
            todos_los_snippets.update(elemento_diccionario)
        return todos_los_snippets

    def getLengsAndTitles(self,consulta=None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        #~ print self.__BD.getLengAndTitles(consulta)
        #~ return self.__Snippets.keys()
        #TODO: estamos buscando en le BD en vez de en el multiobjeto?? 2011/07/01 11:37:51
        return self.__BD.getLengAndTitles(consulta)

    def getSnippet(self,lenguaje,titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        try:
            '''TODO:parece ser que la busqueda de dic no admite unicode
            soluciones:a-probar el modulo codec , b-eliminar todos los
            acentos de la BD c-hacer un dic para que reemplaze los acentos
            d-convertir la clave en unicode(eliminar la tupla)

            despues de investigar un poco es un hueva la codificacion
             por cosas normales 2011/07/01 12:02:51'''
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
        self.__BD = database(pathBD)

    def setSnippetActual(self,unSnippet):
        ''' Establece los datos del Snippet usado actualmente.'''
        self.__SnippetActual = unSnippet

    def setAllPathDBs(self):
        ''' Obtiene todsa las rutas de las bds incluidas en
        el dir databases y el CFG '''
        databases_dir = self.__DBUtils.getBDsInDatabasesDir()
        #TODO: implementar estooo
        databases_cfg = []
        return databases_dir + databases_cfg


######################
## Metodos Privados ##
######################
    #~ def __convertPath(self,path):
        #~ """Convierte el path a el específico de la plataforma (separador)"""
        #~ #TODO: verificar si este metodo es neccesario
        #~ import os
        #~ if os.name == 'posix':
            #~ return "/"+apply( os.path.join, tuple(path.split('/')))
        #~ elif os.name == 'nt':
            #~ return apply( os.path.join, tuple(path.split('/')))

