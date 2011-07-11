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

import sqlite3,os
from members import Members
from sys import argv

class DBUtils:

    def __init__(self):
        pass
        
###############
# METODOS GET #
###############

    def getBDsInDatabasesDir(self):
        ''' Obtiene los path's de las bases de datos ubicadas en el directorio databases.'''
        archivos_dbs = os.listdir(self.getPathDatabasesDir())
        bds = []
        #filtro los archivos devueltos por la extencion .db
        for archivo in archivos_dbs:
            if archivo[-3:] == Members.DB_EXTENCIONS:
                bds.append(self.getPathDatabasesDir()+archivo)
        return bds

    def getBDsNames(self):
        ''' Obtiene una lista con los nombres de los archivos bds. '''
        bd_rutas = self.getBDsInDatabasesDir()
        bd_names = []
        for ruta in bd_rutas:
            nombre_bd = os.path.splitext(os.path.basename(ruta))
            bd_names.append(nombre_bd[0])
        return bd_names

    def getDBNumberInDatabasesDir(self):
        ''' Obtiene la cantidad de archivos de bd en el dir databases '''
        bds = self.getBDsInDatabasesDir()
        return len(bds)

    def getPathDatabasesDir(self):
        ''' Obtiene la ruta del directorio databases segun el so. '''
        program_folder = self.convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
        bd_folder = self.convertPath(os.path.dirname(program_folder[:-1])+'/'+Members.DATABASES_DIR +'/')
        return bd_folder

    def getPathProgramFolder(self):
        ''' Obtiene la ruta de la carpeta del programa. '''
        import os
        from sys import argv
        program_folder = self.convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")
        return program_folder

    def newDataBase(self,pathNewBD):
        ''' Crea una nueva base de datos Fragmentos. '''
        if not os.path.exists(pathNewBD):
            connection = sqlite3.connect(pathNewBD)
            cursor = connection.cursor()
            cursor.execute(Consts.SCRIPTSQL_BD_SNIPPET)
            connection.commit()
            print 'BD creada con exito...'
        else:
            print 'Ya existe una base de datos con el mismo nombre...'

    def validarBD(self,pathBD = None):
        ''' Verifica que la estructura de la bd sea una bd tipo Fragmentos.'''

        if pathBD is None:
            pathBD = self.__pathBD
        connection = sqlite3.connect(pathBD)
        cursor = connection.cursor()
        cursor.execute('Select tbl_name From MAIN.[sqlite_master] where type = "table"')
        existe = False
        for fila in cursor:
            if fila[0] == 'snippet':
                existe = True
        return existe

    def convertPath(self,path):
        """Convierte el path a el específico de la plataforma (separador)"""
        import os
        if os.name == 'posix':
            return "/"+apply( os.path.join, tuple(path.split('/')))
        elif os.name == 'nt':
            return apply( os.path.join, tuple(path.split('/')))


if __name__ == '__main__':

    hola = DBUtils()
    rutas = hola.getBDsNames()
    print rutas
