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

class Snippet:

    # Variables miembro de la clase
    def __init__(self,datosSnippet):
        #recibe un diccionario
        self.__titulo = datosSnippet['title']
        self.__lenguaje = datosSnippet['language']
        self.__codigo = datosSnippet['contens']
        self.__tags = datosSnippet['tags']
        self.__descripcion = datosSnippet['description']
        self.__fechaCreacion = datosSnippet['creation']
        self.__favorito = datosSnippet['starred']
        self.__referencias = datosSnippet['reference']
        self.__fechaModificacion = datosSnippet['modified']
        self.__uploader = datosSnippet['uploader']

    def getTitulo(self):
        return self.__titulo

    def getTags(self):
        return self.__tags

    def getLenguaje(self):
        return self.__lenguaje

    def getDescripcion(self):
        return self.__descripcion

    def getFecha(self):
        return self.__fecha

    def getReferencias(self):
        return self.__referencias

    def getCodigo(self):
        return self.__codigo

    def getFavorito(self):
        return self.__favorito

    def getFechaModificacion(self):
        return self.__fechaModificacion

    def getUploader(self):
        return self.__uploader
