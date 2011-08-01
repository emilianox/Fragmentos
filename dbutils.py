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
        
        # obtiene una lista con los archivos que estan en el directorio databases
        archivos_dbs = os.listdir(self.getPathDatabasesDir())
        bds = []
        # filtra los archivos devueltos por la extencion .db
        for archivo in archivos_dbs:
            # si es un archivo que es alguna de las extenciones permitidas
            if archivo[-3:] == Members.DB_EXTENCIONS:
                bds.append(self.getPathDatabasesDir()+archivo)
        return bds

    def getBDsNames(self):
        ''' Obtiene una lista con los nombres de los archivos bds. '''
        
        # obtienes los paths de las bds en /databases
        bd_rutas = self.getBDsInDatabasesDir()
        bd_names = []
        for ruta in bd_rutas:
            # recupera el nombre del archivo
            nombre_bd = os.path.splitext(os.path.basename(ruta))
            # lo agrega a la lista
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

    def newDataBase(self, pathNewBD):
        ''' Crea una nueva base de datos Fragmentos. '''
        
        # se fija que la bd ya no exista anteriormente
        if not os.path.exists(pathNewBD):
            # crea la conexion para el path asignado
            connection = sqlite3.connect(pathNewBD)
            cursor = connection.cursor()
            # ejecuta la consulta para crear la tabla dentro de la bd
            cursor.execute(Members.SCRIPTSQL_BD_SNIPPET)
            # persiste la consulta
            connection.commit()
            print 'BD creada con exito en : ',pathNewBD
        else:
            print 'Ya existe una base de datos con el mismo nombre...'

    def validarBD(self, pathBD):
        ''' Verifica que la estructura de la bd sea una bd tipo Fragmentos.'''

        # crea la conexion para el path asignado
        connection = sqlite3.connect(pathBD)
        cursor = connection.cursor()
        
        # consulta para obtener las tablas de la bd
        cursor.execute('Select tbl_name From MAIN.[sqlite_master] where type = "table"')
        existe = False
        # recorre las tablas devueltas para verificar que exista la tabla 'snippet'
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
