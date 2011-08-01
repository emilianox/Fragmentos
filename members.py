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

class Members:
    
        ''' Clase que contiene todos los miembros constantes 
        usados en el programa. '''
        
        CFG_FILE = 'settings.cfg'
        DATABASES_DIR = 'databases'
        HISTORY_DIR = 'data'
        HISTORY_FILE = 'history.fht'
        TABLENAME_SNIPPET = 'snippet'
        CONFIG_DIR = 'data'
        SCRIPTSQL_BD_SNIPPET = ''' CREATE TABLE [snippet] (
                                    [title] TEXT  NOT NULL,
                                    [language] TEXT  NOT NULL,
                                    [contens] TEXT  NOT NULL,
                                    [tags] TEXT  NULL,
                                    [description] TEXT  NULL,
                                    [creation] TEXT  NOT NULL,
                                    [starred] TEXT  NULL,
                                    [reference] TEXT  NULL,
                                    [modified] TEXT  NULL,
                                    [uploader] TEXT  NULL,
                                    PRIMARY KEY ([title],[language])
                                    );'''
        #Extenciones soportadas para las bases de datos
        DB_EXTENCIONS = '.db'
