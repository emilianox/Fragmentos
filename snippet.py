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

class Snippet :

    def __init__(self,datosSnippet=None,dbReference=None):
        """ Constructor de la clase. donde:
        datosSnippet, es un objeto de tipo diccionario.
        dbReference, referencia a la instancia actual de la base de datos. """
        
        if datosSnippet != None:
            self.__titulo = datosSnippet['title']
            self.__lenguaje = datosSnippet['language']
            self.__codigo = datosSnippet['contens']
            self.__tags = datosSnippet['tags']
            self.__descripcion = datosSnippet['description']
            self.__fecha_creacion = datosSnippet['creation']
            self.__favorito = datosSnippet['starred']
            self.__referencias = datosSnippet['reference']
            self.__fecha_modificacion = datosSnippet['modified']
            self.__uploader = datosSnippet['uploader']
        if dbReference != None:
            self.__DB = dbReference           

#################
## Metodos Get ##
#################

    def getTitulo(self):
        return self.__titulo

    def getLenguaje(self):
        return self.__lenguaje

    def getCodigo(self):
        return self.__codigo

    def getTags(self):
        return self.__tags

    def getDescripcion(self):
        return self.__descripcion

    def getFechaCreacion(self):
        return self.__fecha_creacion

    def getReferencias(self):
        return self.__referencias

    def getFavorito(self):
        return self.__favorito

    def getFechaModificacion(self):
        return self.__fecha_modificacion

#################
## Metodos Set ##
#################

    def setTitulo(self,titulo):
       self.__actualizarCampo('title',titulo) 
       
        
    def setLenguaje(self,lenguaje):
        self.__actualizarCampo('language',lenguaje)

    def setCodigo(self,codigo):
        self.__actualizarCampo('contens',codigo)
        
    def setTags(self,tags):
        self.__actualizarCampo('tags',tags)
        
    def setDescripcion(self,descripcion):
        self.__actualizarCampo('descripction',descripcion)
        
    def setFechaCreacion(self,fcreacion):
        self.__actualizarCampo('creation',fcreacion)

    def setReferencias(self,referencias):
        self.__actualizarCampo('reference',referencias)

    def setFavorito(self,favorito):
        self.__actualizarCampo('starred',favorito) 
                      
    def setFechaModificacion(self,fmodificacion):
        self.__actualizarCampo('modified',fmodificacion)   
        
    def setUploader(self,uploader):
        self.__actualizarCampo('uploader',uploader)
        
    def setDB(self,dbReference):
        self.__DB = dbReference
                                   
    def __actualizarCampo(self,campo,valorNuevo):
        ''' Recibe el campo y valor nuevo y edita ese campo en la 
        base de datos, correspondiente a este Snippet. '''
        
        sql_update = 'UPDATE snippet SET ' + campo + ' = ' + valorNuevo + ' \
        WHERE title = ' + self.titulo + ' AND language = ' + self.lenguaje
        try:
            connection = sqlite3.connect(self.__DB.getPathBD())
            cursor = connection.cursor(sql_update)
            cursor.execute()
            connection.commit()
        except sqlite3.OperationalException, msg:
            print 'actualizarCampo: ',msg
