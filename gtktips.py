#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       gtktips.py
#
#       Copyright 2010-2011 Emiliano Fernandez <emilianohfernandez@gmail.com>
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
import gtk
import time
import gtksourceview2
class GtkTips:
    """Tips que facilitan el uso de herramientas GTK"""
################# LISTAS #######################################################
    def __init__(self):
        self.datos="" #obtener los datos que estan actualmente en la lista
        self.listaColumnas=""
        self.cellrender=""

    def crearLista(self,treeview, listaColumnas,CellRender=gtk.CellRendererText()):
        """Recibe un treview y crea un listore con las columnas de la tabla."""
        viejas_columnas = treeview.get_columns()
        for basura in viejas_columnas :###crear columnas
            treeview.remove_column(basura)
        self.listaColumnas=listaColumnas
        liststore = self.crearListview(listaColumnas)
        treeview.set_model(liststore)
        i = 0
        for columna in listaColumnas :###crear columnas
            column = gtk.TreeViewColumn(columna,CellRender, text=i)
            column.set_resizable(True)
            treeview.append_column(column)
            i += 1
        #~ treeview.set_enable_search(True)
        #~ treeview.set_search_column(0)### make treeview searchable
        #~ treeview.set_reorderable(True)### podes arrastrar columnas
        treeview.set_rules_hint(True) # colores alternados
        #returns
        return liststore

    def crearListview(self,numColumnas):#dependencia del anterior
        """A partir de una lista de columnas crea el liststore."""
        __temp = []
        for elemento in numColumnas:
            __temp.append(str)
        __arg = tuple(__temp)
        return gtk.ListStore(*__arg)

    def rellenarLista(self,lista,datos):
        """Rellena una liststore con una lista de filas de datos."""
        print "Comienza el relleno de listas"
        lista.clear()
        self.datos=datos
        #~ i=1
        for row in datos:
            #~ i+=1
            #~ print i," filas cargadas."
            lista.append(row)
        return lista

    def crearListaTF(self,treeview, listaColumnas):
        """Recibe un treview y crea un listore con las columnas de la tabla."""
        from herramientas import whois
        self.w =whois()
        viejas_columnas = treeview.get_columns()
        for basura in viejas_columnas :###crear columnas
            treeview.remove_column(basura)
        self.listaColumnas=listaColumnas
        liststore = self.crearListviewTF(listaColumnas)
        treeview.set_model(liststore)
        i = 0
        fg = len(listaColumnas)
        for columna in listaColumnas :###crear columnas
        #0000#
            cell = gtk.CellRendererText()
            #~ cell.set_property('background-set' , True)
            cell.set_property('foreground-set' , True)
            column = gtk.TreeViewColumn(columna,cell, text=i,\
            foreground=fg)
        #0000#
            #~ column = gtk.TreeViewColumn(columna,CellRender, text=i)
            column.set_resizable(True)
            treeview.append_column(column)
            i += 1
        #~ treeview.set_enable_search(True)
        #~ treeview.set_search_column(0)### make treeview searchable
        #~ treeview.set_reorderable(True)### podes arrastrar columnas
        treeview.set_rules_hint(True) # colores alternados
        #returns
        return liststore

    def crearListviewTF(self,numColumnas):#dependencia del anterior
        """A partir de una lista de columnas crea el liststore."""
        __temp = []
        for elemento in numColumnas:
            __temp.append(str)
        #000#
        __temp.append(str)
        #0000#
        __arg = tuple(__temp)

        return gtk.ListStore(*__arg)

    def rellenarListaTF(self,lista,datos):
        """Rellena una liststore con una lista de filas de datos."""
        print "Comienza el relleno de listas"
        lista.clear()
        self.datos=datos
        #~ i=1
        for row in datos:
        #~ #0000#
            row = list(row)
            if self.w.esta_libre(row[0],row[1]):
                row.append(u"#155415")
            else:
                row.append(u"#8C1B10")
        #0000#
            #~ i+=1
            #~ print i," filas cargadas."
            lista.append(tuple(row))
        return lista

    def cargarEnLista(self,lista,listaaagregar):
        self.datos=self.datos+listaaagregar
        #~ i=1
        for row in listaaagregar:
            #~ i+=1
            #~ print i," filas cargadas."
            lista.append(row)
        return lista

    def create_cell_render(self):
        import pango
        self.cellrender = gtk.CellRendererText()
        font = pango.FontDescription('default 13')
        self.cellrender.set_property('font-desc', font)
        return self.cellrender

    def change_font_size(self,num):
        import pango
        viejafont = self.cellrender.get_property('font-desc')
        fontnew =font = pango.FontDescription("default "+str(int(str(viejafont)[-2:])+num))
        print fontnew
        self.cellrender.set_property('font-desc', fontnew)
        pass
################ Combobox ####################################
    def setCombobox (self,cb, items):
        """Setup a ComboBox or ComboBoxEntry based on a list of strings."""
        """Written by Thomas Hinkle(thanks for all)."""
        modelo = gtk.ListStore(str)
        for i in items:
            modelo.append([i])
        cb.set_model(modelo)
        if type(cb) == gtk.ComboBoxEntry:
            cb.set_text_column(0)
        elif type(cb) == gtk.ComboBox:
            cell = gtk.CellRendererText()
            cb.pack_start(cell, True)
            cb.add_attribute(cell, 'text', 0)
        cb.set_active(0)

    def valor_combobox(self,combobox):
        """ Función que obtiene el texto de la opción seleccionada en un ComboBox"""
        self.model = combobox.get_model()
        self.activo = combobox.get_active()
        if self.activo < 0:
            return None
        return self.model[self.activo][0]

################ Label ####################################
    def listtolabel(self, lista, label):
        """Recibe una lista y un label
        y devuelve el label con los valores de la lista
        en formato horizontal"""
        temp = ""
        for item in lista:
            temp =temp + str(item)+"\n"
        #print temp
        label.set_label(temp.upper())

##############GtkSourceView#################################
    def crear_source_text_box(self,box,nombre_style,path_style):
        import pango
        font_desc = pango.FontDescription("Monospace 9")
        style=gtksourceview2.StyleSchemeManager()
        style.append_search_path(path_style)
        myestilo = style.get_scheme(nombre_style)
        text_buffer = gtksourceview2.Buffer()
        text_buffer.set_style_scheme(myestilo)
        text_buffer.set_highlight_syntax(True)
        text = gtksourceview2.View(text_buffer)
        text.set_show_line_numbers(True)
        text.set_tab_width(4)
        text.set_auto_indent(True)
        #~ text.set_smart_home_end(True) #sirve para que fin sea findelinea

        text.set_insert_spaces_instead_of_tabs(True)
        #~ text.set_show_right_margin(True)
        #~ text.set_right_margin_position(80)
        text.set_smart_home_end(True)
        text.modify_font(font_desc)
        box.add(text)
        text.show_all()
        #~ text.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FCF2E4"))

        return text

    def cambiar_lenguaje_source(self,sourceview,languaje):
        """Cambia el lenguaje de un gtksourceview."""
        lang_manager = gtksourceview2.LanguageManager()
        lang_latex = lang_manager.get_language(languaje)
        sourceview.get_buffer().set_language(lang_latex)

    def lista_ordenada_lenguajes(self):
        """genera una lista ordenada de lenguajes de gtksourceview."""
        lang_manager = gtksourceview2.LanguageManager()
        listalenguaje = lang_manager.get_language_ids()
        listalenguaje.sort()
        return listalenguaje

###############################entry##################################
    def change_color_entry(self,entry,lista):
        """Permite cambiar el color si no hay resultados."""
        if len(lista) == 0 :
            entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FF6666"))
            entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
        else:
            entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
            entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#000000"))



#####################Date##########################################
class DateChoose():
    """Permite generar un dialog para elegir un dia."""
    def __init__(self):
        self.__dia=""

    def dialog (self,title):
        """Metodo principal.
        Permite generar un dialog para elegir un dia."""
        dia = gtk.Dialog('Window Title',
                        None,  #the toplevel wgt of your app
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,  #binary flags or'ed together
                        ( gtk.STOCK_CANCEL, gtk.RESPONSE_CLOSE,gtk.STOCK_SAVE,77))
        label=gtk.Label(title)
        dia.vbox.pack_start(label, False, False, 0)
        calendar = self.crear_calendar()
        dia.vbox.pack_end(calendar, True, True, 0)
        label.show()
        calendar.show()
        result = dia.run()
        fecha=""
        if result == 77:
            fecha = self.getDia()
        print "Cerrando dialogo..."
        dia.destroy()
        return fecha

    def crear_calendar(self):
        """Crea el objeto calendar y enlaza sus eventos"""
        self.calendar = gtk.Calendar()
        self.calendar.connect("day_selected", self.calendar_day_selected)
        return self.calendar

    def calendar_day_selected(self, widget):
        """Evento que registra el cambio de fecha."""
        self.__dia = self.calendar_date_to_string()
        print self.__dia

    def calendar_date_to_string(self):
        """Conviente la fecha del calendar a un string con el formato DD/MM/YYYY"""
        year, month, day = self.calendar.get_date()
        mytime = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        return time.strftime("%d/%m/%Y", time.localtime(mytime))


    def getDia(self):
        return self.__dia
#################################other#########################################
class Multiplataforma():

    def convertpath(self,path):
        """Convierte el path a el específico de la plataforma (separador)"""
        import os
        if os.name == 'posix':
            return "/"+apply( os.path.join, tuple(path.split('/')))
        elif os.name == 'nt':
            return apply( os.path.join, tuple(path.split('/')))

