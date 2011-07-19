#!/usr/bin/env python
# -*- coding: utf-8 -*-



def normalizarTitulo(titulo):
    
    #quita mas de un espacio entre palabras
    while titulo.find("  ") != -1:
            titulo = titulo.replace("  "," ")
    #quita espacios al comienzo y final
    titulo = titulo.strip()
    #pone la primer letra a Mayuscula
    titulo = titulo.capitalize()
    
    return titulo
    

titulo = "      probando  norm tags     "

h = normalizarTitulo(titulo)
print h+"-"
