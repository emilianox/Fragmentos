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

import sqlite3
import os
#~ import members
#~
class BD:

    def __init__(self,rutaBD):
        ''' Costructor de la clase. '''
        self.__pathBD = rutaBD
        #conecta a la base de datos
        self.__connection = sqlite3.connect(self.__pathBD)
        #activa el cursor
        self.__cursor = self.__connection.cursor()
        print 'Una instancia de BD fue creada con exito...',rutaBD

###############
# METODOS BD  #
###############

    def getPathBD(self):
        ''' Obtiene la ruta de la base de datos en uso. '''
        return self.__pathBD

    def getLenguajes(self):
        ''' Obtiene los lenguajes para la actual BD. '''

        resultado = self.realizarConsulta('SELECT language FROM snippet ORDER BY language')
        return resultado

    def getLengAndTitles(self,consulta=None):
        ''' Obtiene los snippets por lenguajes de la actual BD.'''
        if not consulta:
            resultado = self.realizarConsulta('SELECT language,title FROM snippet ORDER BY language,title')
        else:
            resultado = self.realizarConsulta(consulta)
        return self.__convertirALista(resultado)

    def getAllSnippets(self):
        ''' Obtiene todos los snippets de la base de datos. '''
        resultado = self.realizarConsulta('SELECT language FROM snippet ORDER BY language')
        return self.__convertirALista(resultado)

    def getSnippet(self,lenguaje,titulo):
        ''' Obtiene un snippet por su lenguaje y titulo correspondiente. '''
        resultado = self.realizarConsulta("SELECT * FROM snippet WHERE language = '"+lenguaje+"' AND title = '"+titulo + "'")
        return self.__convertirALista(resultado)

    def realizarConsulta(self,consulta):
        ''' Realiza una consulta a la base de datos. '''
        #TODO:evitar los self
        #~ print consulta
        cursor_temp = self.__cursor.execute(consulta)
        lista = []
        for fila in cursor_temp:
            lista.append(fila)
        #~ print 'Consulta completa...'
        return lista

################################
# METODOS PARA MANEJAR SNIPPET #
################################

    def agregarSnippet(self,datosSnippet):
        ''' Agrega un nuevo Snippet a la base de datos. '''

        # TODO: agregar los try-catch para contemplar:
        # º snippet repetido
        # º error al agregar un snippet

        listaDatos = map(unicode,datosSnippet)
        self.__cursor.execute('''INSERT INTO snippet (title,tags,language,comments,date,contens)
                                 VALUES (?,?,?,?,?,?)''', datosSnippet)
        self.__connection.commit()


    def editarSnippet(self,datosSnippet):
        ''' '''
        pass

    def modificarSnippet(self,datosSnippetIn,datosSnippetOut):
        ''' '''
        pass

######################
# METODOS AUXILIARES #
######################

    def __convertirALista(self,datos):
        ''' Carga el resultado de una consulta a la BD, en una lista. '''
        lista = []
        for fila in datos:
            lista.append(fila)
        return lista


