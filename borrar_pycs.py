#!/usr/bin/env python
# -*- coding: utf-8 -*-

#

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

EXTENCION = '*.pyc'
import os
from sys import argv
import glob

def convertpath(path):
	"""Convierte el path a el específico de la plataforma (separador)"""
	if os.name == 'posix':
		return "/"+apply( os.path.join, tuple(path.split('/')))
	elif os.name == 'nt':
		return apply( os.path.join, tuple(path.split('/')))
		
def borrarArchivosPorExtencion(archivos):
	''' Borra los archivos pasados en la lista 
	que recibe por parámetro'''
	for archivo in archivos:
		os.remove(archivo)
	print str(len(archivos)) + ' archivo(s) eliminados...'
	raw_input()

def getProgramFolder():
	''' Obtiene la ruta del programa actualmente ejecutandoce'''
	def convertpath(path):
		"""Convierte el path a el específico de la plataforma (separador)"""		
		if os.name == 'posix':
			return "/"+apply( os.path.join, tuple(path.split('/')))
		elif os.name == 'nt':
			return apply( os.path.join, tuple(path.split('/')))
	program_folder = convertpath(os.path.abspath(os.path.dirname(argv[0])) + "/")
	return program_folder

#obtiene los archivos del directorio, filtardo por la extencion que deseo
ficheros = glob.glob(getProgramFolder()+EXTENCION)
#borra los archivos
borrarArchivosPorExtencion(ficheros)
