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

import sqlite3


class Snippet (object):

    def __init__(self,datosSnippet=None,dbReference=None):
        u""" Constructor de la clase. donde:
        datosSnippet, es un objeto de tipo diccionario.
        dbReference, referencia a la instancia actual de la base de datos. """

        if datosSnippet is not None:
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
        if dbReference is not None:
            self.__DB = dbReference
    
#################
## Metodos Get ##
#################

    def __getTitulo(self):
        return self.__titulo

    def __getLenguaje(self):
        return self.__lenguaje

    def __getCodigo(self):
        return self.__codigo

    def __getTags(self):
        return self.__tags

    def __getDescripcion(self):
        return self.__descripcion

    def __getFechaCreacion(self):
        return self.__fecha_creacion

    def __getReferencias(self):
        return self.__referencias

    def __getFavorito(self):
        return self.__favorito

    def __getFechaModificacion(self):
        return self.__fecha_modificacion
    def __getUploader(self):
        return self.__uploader
        
#################
## Metodos Set ##
#################

    def __setTitulo(self,titulo):
        print 'entrando a actualiuzar titulo...'
        self.__actualizarCampo('title',titulo)


    def __setLenguaje(self,lenguaje):
        self.__actualizarCampo('language',lenguaje)

    def __setCodigo(self,codigo):
        self.__actualizarCampo('contens',codigo)

    def __setTags(self,tags):
        self.__actualizarCampo('tags',tags)

    def __setDescripcion(self,descripcion):
        self.__actualizarCampo('descripction',descripcion)

    def __setFechaCreacion(self,fcreacion):
        self.__actualizarCampo('creation',fcreacion)

    def __setReferencias(self,referencias):
        self.__actualizarCampo('reference',referencias)

    def __setFavorito(self,favorito):
        self.__actualizarCampo('starred',favorito)

    def __setFechaModificacion(self,fmodificacion):
        self.__actualizarCampo('modified',fmodificacion)

    def __setUploader(self,uploader):
        self.__actualizarCampo('uploader',uploader)

    def setDB(self,dbReference):
        self.__DB = dbReference

    def __actualizarCampo(self,campo,valorNuevo):
        ''' Recibe el campo y valor nuevo y edita ese campo en la
        base de datos, correspondiente a este Snippet. '''
        
        sql_update = "UPDATE snippet SET %s = ? WHERE title = ? AND language = ?"
        try:
            connection = sqlite3.connect(self.__DB.getPathBD())
            cursor = connection.cursor()
            cursor.execute(sql_update % (campo),(valorNuevo,self.titulo,self.lenguaje))
            connection.commit()
        except Exception, msg:
            print 'actualizarCampo: ',str(msg)


################
## Properties ##
################

    titulo = property(__getTitulo,__setTitulo)
    lenguaje = property(__getLenguaje,__setLenguaje)
    codigo = property(__getCodigo,__setCodigo)
    tags = property(__getTags,__setTags)
    descripcion = property(__getDescripcion,__setDescripcion)
    fechaCreacion = property(__getFechaCreacion,__setFechaCreacion)
    fechaModificacion = property(__getFechaModificacion,__setFechaModificacion)
    referencias = property(__getReferencias,__setReferencias)
    favorito = property(__getFavorito,__setFavorito)
    uploader = property(__getUploader,__setUploader)
