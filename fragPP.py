#!/usr/bin/python
# -*- coding: utf-8 -*-
#       PlantillaInicioGlade.py
#
#       Copyright 2009 Emiliano Fernandez <emilianohfernandez@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
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

import gtk, os
from sys import argv, exit
import snippetmanager,gtktips,gui

###
#Bienvenidos a las turbulentas aguas de entender a un "desarrollador"
#la documentacion es tu guia
###


class VentanaPrincipal:
    """Genera una ventana principal"""
    def __init__(self):
        self.SM = snippetmanager.SnippetManager()
        self.GUI = gui.GUI()
    #Imports
        #~ from  import
        #~ import
    #constantes
        nombreglade = "fragPP.gui"
        nombreventana = "wPrincipal"
        tituloventana = "Fragmentos"
        xml_estilo = self.SM.convertPath(self.SM.getPathProgramFolder()+'style/blue_dream.xml')
    #importar glade
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.SM.getPathProgramFolder()+ nombreglade)
    #objetos basicos
        self.window = self.builder.get_object(nombreventana)
        #self.window.set_icon_from_file(self.program_folder+"*****")
    #detalles
        self.window.set_title(tituloventana)
        self.window.show_all()
        self.builder.connect_signals(self)
    #variables de Clase
        self.soy_una_variable = ''
    #Llamadas extras
        self.vbOtros = self.builder.get_object("vbOtros")
        self.mPrincipal = self.builder.get_object("mPrincipal")

    #tree list
        self.caja_lenguajes = self.builder.get_object("tvLenguajes")
        self.caja_lenguajes,self.tree_lenguajes = self.GUI.crearArbol(self.caja_lenguajes,'Lenguajes')
        self.GUI.cargarSnippetsEnArbol(self.tree_lenguajes,self.SM.getLengsAndTitlesFromBD())
#Sourcecode

        self.source_view = gtktips.SourceView()
        scroll = self.builder.get_object("contenedor")
        nstyle,pstyle = 'blue_dream',xml_estilo
        self.txtCodigo = self.source_view.crear_source_text_box(scroll,nstyle,pstyle)

#detalles
        self.eBusqueda = self.builder.get_object("eBusqueda")
        self.eBusqueda.grab_focus()
        self.imgStar = [self.builder.get_object("imgStar"),True]
        self.imgStar[0].set_from_file(self.SM.getPathProgramFolder()+'/art/star-empty.png')
#cargar bds en combo
        self.cbBD = self.builder.get_object('cbBD')
        self.GUI.cargarBDsEnCombo(self.cbBD)
#Info al iniciar

        print "full path =", self.SM.getPathProgramFolder()
############
## Metods ##
############
    def XXX(self):
        """XXXXXXXXX"""
        pass

    def busqueda_inteligente(self,cadena):
        """Permite la busqueda por keys"""
        datos = self.SM.getLengsAndTitlesFromBD(cadena)
        self.GUI.cargarSnippetsEnArbol(self.tree_lenguajes,datos)
        #Magic. Do not touch


    def alPortapapeles(self):
        """Envia el contenido de el codigo al portapapeles"""
        from gtk import Clipboard

        textbuffer = self.txtCodigo.get_buffer()
        iter1, iter2 = textbuffer.get_bounds()

        cb = Clipboard()
        text = textbuffer.get_text(iter1,iter2)
        cb.set_text(text)
        cb.store()
        print "se ha mandado al portapapeles"

############
## Events ##
############
    def on_btStar_clicked(self,widget):
        if self.imgStar[1]:
            self.imgStar[0].set_from_file(self.SM.getPathProgramFolder()+'/art/star-full.png')
            self.imgStar[1] = False
        else:
            self.imgStar[0].set_from_file(self.SM.getPathProgramFolder()+'/art/star-empty.png')
            self.imgStar[1] = True

    def on_tvLenguajes_cursor_changed(self,widget):
        model,row = widget.get_selection().get_selected()
        rownodo = model.iter_parent(row)
        if not (rownodo is None):
            valor_nodo = model.get_value(rownodo,0)
            valor_hijo = model.get_value(row,0)
            Snippet = self.GUI.obtenerSnippet(valor_nodo,valor_hijo)
            self.source_view.cambiar_lenguaje_source(self.txtCodigo,valor_nodo.lower())
            self.txtCodigo.get_buffer().set_text(Snippet.getCodigo())
            #TODO: hacer funcion que contemple la similaridad de lenguajes
            #~ equivalentes={'basic':'vbnet','c#':'c-sharp'}

        #~ print '\n',model.iter_n_children(rows)#devuelve cantidad de hijos

    def on_tbPortapapeles_clicked(self, widget):
        self.alPortapapeles()

    def on_btXXX_clicked (self, widget):
        self.XXX()

    def on_btSalir_clicked(self,widget):
        gtk.main_quit()

    def on_VentanaPrincipal_destroy(self,widget):
        gtk.main_quit()

    def on_tgbtRelacionado_toggled(self,widget):
        #TODO
        pass

    def on_tgbtDetalles_toggled(self,widget):
        if widget.get_active():
            position = 30
            self.tanterior = self.vbOtros.get_size_request()#tamaño anterior
            self.vbOtros.set_size_request(-1, 100)
            self.unlabel = gtk.Label('-hola,vengo a flotar\n y como te llamas? -mi nombre es carlitox')#label de pruebas
            self.vbOtros.pack_start(self.unlabel)
        #TODO:agregar un frame
            self.vbOtros.reorder_child(self.unlabel, 0)
            self.unlabel.show()
        else:
            self.vbOtros.remove(self.unlabel)
            self.vbOtros.set_size_request(self.tanterior[0],self.tanterior[1])

        pass

    def on_eBusqueda_insert_text(self, widget, ingresado, tamano, gpoint):
        textoAnterior = widget.get_text()
        pos = widget.get_position()
        cadena = textoAnterior[:pos]+ingresado+textoAnterior[pos:]
        #TODO
        self.busqueda_inteligente(cadena)
        pass

    def on_eBusqueda_delete_text(self,widget,numAhora,numAntes):
        textoAnterior = widget.get_text()
        cadena = textoAnterior[:numAhora] + textoAnterior[numAntes:]
        self.busqueda_inteligente(cadena)
        #TODO
        pass

    def on_btMenu_clicked(self,widget):
        self.mPrincipal.popup(None, None, None, 10, 0)
        pass

##########
## Menu ##
##########
    def on_imenuXXX_activate(self,widget):
        pass

#######################################################
if __name__ == '__main__':
    ventana= VentanaPrincipal()
    gtk.main()
    exit(0)
