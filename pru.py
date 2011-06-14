#!/usr/bin/env python
# -*- coding: utf-8 -*-

#probando agregar un snippet a la bd

#~ from snippetmanager import SnippetManager
#~ from datetime import *
#~ 
#~ agregar = SnippetManager()
#~ raw_input()
#~ print 'instancia de sm iniciada... '
#~ 
#~ agregar.agregarSnippet('probando agregar algo',
                        #~ 'probando',
                        #~ 'mike',
                        #~ 'print "esto es una prueba"',
                        #~ str(datetime.today()),
                        #~ '','')
#~ print 'se inserto el snippet.... '

from utils import Utils 

hola = Utils()
rutas = hola.getBDsInDatabasesDir()
print rutas
