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

import sqlite,os
from Members import Consts

class BdUtils:
	
###############    
# METODOS GET #
###############

    def getRutaBDs(self):
        ''' Obtiene los path's de todas las bases de datos [databases + cfg_file] '''
        pass

    def getBDsInDatabasesDir(self):
        ''' Obtiene los path's de las bases de datos ubicadas en el directorio databases.'''
        pass
        
    def getBDsInCfgReferences(self):
        ''' Obtiene los path's de las bases de datos ubicadas en el directorio databases.'''
        pass
        
	def getNumberInDatabasesDir(self):
		''' '''
		pass
        
	def newDataBase(self,pathNewBD):
		''' Crea una nueva base de datos Fragmentos. '''
		if not os.path.exists(pathNewBD):
			conexion = sqlite3.connect(pathNewBD)
			conexion.execute(Consts.SCRIPTSQL_BD_SNIPPET)
			conexion.commit()
			print 'BD creada con exito...'	
		else:
			print 'Ya existe una base de datos con el mismo nombre...'
			
	def validarBD(self,pathBD):
        ''' Verifica que la estructura de la bd sea una bd tipo Fragmentos.'''
        
        pass
