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

import sqlite3, os, os.path

from members import Members
from pathtools import PathTools
from sqlite import sqlite

class DBUtils:
    ''' Clase para el manejo de utilidades de base de datos. '''
    
    def __init__(self):
        self.__PT = PathTools()
        self.__new_campos = ['title','language','contens','tags','description',
        'creation','starred','reference','modified','uploader']
        self.__old_campos = ['title','language','contens','tags',
            'comments','date','starred','reference']
        
###############
# METODOS GET #
###############

    def agregarBDADefault(self, pathBD):
        ''' Copia el archivo recibido a la carpeta establecida por defecto
        para los catalogos del programa.'''
        import shutil
        
        shutil.copy(pathBD, self.__PT.getPathDatabasesDir())
        
    def actualizarEstructuraBD(self, pathBD):
        ''' Reconfigura la estructura de la bd antigua a la version actual.'''
        
        import os
        
        bd = sqlite(pathBD)
        
        # obtiene todos los snippets de la bd
        todo = bd.getDatosTabla('snippet','title,language,contens,tags,comments,date,starred,reference')
                
        # elimina el actual archivo de la bd        
        os.remove(pathBD)
        # creamos una nueva bd 
        self.newDataBase(pathBD)
        
        bd = sqlite(pathBD)

        orden_campos = {
        'title':0,
        'language':1,
        'contens':2,
        'tags':3,
        'description':4,
        'creation':5,
        'starred':6,
        'reference':7
        }
        # agrega nuevamente los snippets a la bd
        bd.realizarAltas('snippet', orden_campos, todo)
        
        print 'Estructura de la bd actualizada.'
        
    def getBDsInDatabasesDir(self):
        ''' Obtiene los path's de las bases de datos ubicadas en el directorio databases.'''
        
        # obtiene una lista con los archivos que estan en el directorio databases
        archivos_dbs = os.listdir(self.__PT.getPathDatabasesDir())
        bds = []
        # filtra los archivos devueltos por la extencion .db
        for archivo in archivos_dbs:
            # si es un archivo que es alguna de las extenciones permitidas
            if os.path.splitext(archivo)[1] == Members.DB_EXTENCIONS:
                bds.append(self.__PT.getPathDatabasesDir()+archivo)
        return bds

    def getBDsNamesDatabasesDir(self):
        ''' Obtiene una lista con los nombres de los archivos bds,
        del directorio databases.  '''
        
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

    def __getColumnasTabla(self, nombreTabla) :
        """ Obtiene los nombres de las columnas de la tabla. """
        columnas = []
        self.__cursor.execute('PRAGMA table_info(' + nombreTabla +')')
        infotable = self.__cursor.fetchall()
        #print infotable
        for row in infotable:
            #print row
            columnas.append(row[1])
        return columnas
    
    #~ def isBDActual(self, pathBD):
        #~ ''' Devuelve TRUE en caso de que sea una base de datos
        #~ Fragmentos con la estructura 'title','language','contens','tags',
        #~ 'description','creation','starred','reference','modified','uploader'.'''
        #~ 
        #~ # pregunta si es la bd con estructura nueva
        #~ if self.validarBD(pathBD) :
            #~ return True
        #~ elif self.validarBD(pathBD):
            #~ return False
        
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
            return True
        else:
            print 'Ya existe una base de datos con el mismo nombre...'
            return False

    def validarBD(self, pathBD):
        ''' Verifica que la estructura de la bd sea una bd tipo Fragmentos.'''

        valido = False
        # crea la conexion para el path asignado
        connection = sqlite3.connect(pathBD)
        cursor = connection.cursor()
        
        # consulta para obtener las tablas de la bd
        try:
            cursor.execute('Select tbl_name From MAIN.[sqlite_master] where type = "table"')
        except :
            return False
        # recorre las tablas devueltas para verificar que exista la tabla 'snippet'
        for fila in cursor:
            if fila[0] == 'snippet':
                # recupera las 
                columnas = []
                cursor.execute('PRAGMA table_info(snippet)')
                infotable = cursor.fetchall()
                for row in infotable:
                    columnas.append(row[1])
                
                if columnas == self.__new_campos :
                    valido = True
                elif columnas == self.__old_campos :
                    self.actualizarEstructuraBD(pathBD)
                    valido = True
                else: valido = False

        return valido

if __name__ == '__main__':
#~ 
    hola = DBUtils()
    act = 'ms.db'
    old = 'HolaMundo.db'
    prueba = old
    #~ rutas = hola.getBDsNames()
    #~ print hola.isBDACtual(prueba)
    #~ 
    #~ if not hola.isBDACtual(prueba):
        #~ print 'estoy por actualizar la estructura'
        #~ print hola.validarBD(prueba)
        #~ hola.actualizarEstructuraBD(prueba)
        
    #~ hola.actualizarEstructuraBD(prueba)    
