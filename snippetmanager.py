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
from utils import Utils
from snippet import Snippet

class SnippetManager:
    ''' Clase que hace de wrapper entre las clases
    de la logica del programa, con la clase GUI'''

    def __init__(self,pathBD):
        self.BD = BD(pathBD)
        self.Utils = Utils()
        self.pathsBDS = []
        self.todos_los_snippets = {}

##########################
## Metodos de instancia ##
##########################

    def agregarSnippet(self,titulo,tags,lenguaje,contenido,fecha,detalles,referencias):
        ''' Recibe los datos desde los widgets de la GUI,
        y carga los datos en una lista para agregarlos a la BD.'''
        datosSnippet = []
        datosSnippet.append(titulo)
        datosSnippet.append(tags)
        datosSnippet.append(lenguaje)
        datosSnippet.append(contenido)
        datosSnippet.append(detalles)
        datosSnippet.append(fecha)
        datosSnippet.append(referencias)
        self.BD.agregarSnippet(datosSnippet)


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
        #TODO: agregar la implementacion de esto
        pass

    def getAllSnippetsFromBD(self):
        ''' Obtiene los snippets desde la bd y carga en un diccionario
        los snippets en formato objeto Snippet().'''
        clave = ()
        #orden en que vienen los campos
        #1-title,2-language,3-tags,4-comments,5-description
        #6-references,7-creation,8-modified,9-uploader,10-starred
        all_snippets = self.BD.getAllSnippets()
        #itera convirtiendo el resultado de la bd, en una
        #coleccion de instancias de Snippet()
        #~ snippet = None
        for actual in all_snippets:
            #obtengo la clave del snippet
            clave = (actual[1],actual[0])#snippet[0] = title, snippet[1] = language
            #se crea una instancia de snippet con los datos actuales
            snippet = Snippet({'title':actual[0],'language':actual[1],
            'tags':actual[2],'contens':actual[3],'description':actual[4],
            'reference':actual[5],'creation':actual[6],'modified':actual[7],
            'uploader':actual[8],'starred':actual[9]})
            #diccionario auxiliar
            elemento_diccionario = {clave:snippet}
            #carga este snippet en el diccionario
            self.todos_los_snippets.update(elemento_diccionario)

        return self.todos_los_snippets

    def getLengsAndTitlesFromBD(self,consulta=None):
        ''' Obtiene los snippets por lenguajes desde la bd.'''
        #sin args devuelve la lista completa si no devuleve filtrado
        if consulta != None:
            from bd import busqueda
            b = busqueda.Busqueda()
            sql =  b.generarConsulta(consulta)
            #~ print sql
        else:
            sql = None
        return self.BD.getLengAndTitles(sql)

    def getPathsBDs(indice = None):
        ''' Devuleve la/s ruta/s de las bds cargadas en self.pathsBDS'''
        if indice is None:
            pass
        else:
            pass

    def getSnippetFromBD(self,lenguaje,titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        from snippet import Snippet
        miSnippet = Snippet(self.BD.getSnippet(lenguaje,titulo))
        return miSnippet

    def getSnippetsCountFromBD(self):
        ''' Devuelve un entero con la cantidad de snippets cargados en la BD.'''
        return self.BD.getSnippetsCount()

    def buscarSnippets (self, argumentos) :
        """ recibe un argumento y devuelve una consulta en sql """
        #controlo que no tenga =
            #si hay = busco por titulo

        #sino controlo que no haya ,
            #si hay , divido y hago busqueda avanzada
            #si no hay hago busqueda avanzada

        # returns
        pass

#################
## Metodos Set ##
#################

    def setPathsBDs():
        ''' Carga en una lista, las rutas de las bds existentes en el dir
        databases y el cfg '''
        pass

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

#~ U = Utils()
#~ pathbd_volador = U.getPathDatabasesDir()+'SourceCode.db'
#~ f = SnippetManager(pathbd_volador)
#~ print f.getSnippetFromBD('VB','Solo numeros')
