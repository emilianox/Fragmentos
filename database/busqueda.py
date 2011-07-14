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

class Busqueda :
    '''(NULL)'''

    def __init__(self):
        self.diccampos = {
        't=' : 'title',
        'l=':'language',
        'g=':'tags',
        'c=':'contents',
        'd=':'description',
        'r=':'references',
        'n=':'creation',
        'm=':'modified',
        'u=':'uploader',
        's=':'starred'
        }
        
    def generarConsulta (self, labusqueda, enfavoritos) :
        """ recibe la busqueda completa y genera un sql para realizar la busqueda """
        listadecriteriosseparados = self.__separarPorCampos(labusqueda)
        if listadecriteriosseparados:
            sql = self.__generarSQL(listadecriteriosseparados, enfavoritos)
            #~ print 'hice una consulta: ',len(sql)
        else :
            sql = ' '
        return sql

    def __separarPorCampos (self, labusqueda) :
        """ separa la busqueda en una lista donde cada elemento es el criterio a buscar por campo """
        #CAUTION!!! Magic. Do not touch
        #~ labusqueda = 'f=sadsdas,t=dadfd and gernedsa,g=dsfbusdfud'
        #~ print 'separando por comas...'
        listadecriterios = []
        if labusqueda.find('=') == -1:
            #caso en que solo escribas titulo(o sea nada)
            listadecriterios.append('t='+labusqueda)
        else:
            if labusqueda.find(',') == -1:
                #caso en que escribas un solo campo para buscar ej: t=hola
                if len(labusqueda) > 2 :
                    listadecriterios.append(labusqueda)
                else:
                    listadecriterios = False
            else:
            #caso en que tengas todo ej: t=hola,l=python
                listadecriterios = labusqueda.split(',')
                #~ print 'el num es: ',len(listadecriterios[-1])
                #~ print 'nuevo antes:',listadecriterios[:-1]
                if len(listadecriterios[-1]) < 3 :
                    #~ listadecriterios = listadecriterios[:-1]
                    listadecriterios = False

        return listadecriterios

    def __generarConsultaSimple (self, campo) :
        """ devuelve el sql del campo simple buscado """
        #esto es para __generarSQL
        #preconsulta = 'SELECT language,title FROM snippet ORDER BY language,title where '
        #~ print 'generando consulta simple... ',campo

        #~ campo = 'g=agua'
        if campo[:2] == 'g=':#%,atr,%-%,atr-atr,%-atr
            sql = "((" + self.diccampos[campo[:2]] + " LIKE '%,"+campo[2:]+",%')"+\
            " or (" + self.diccampos[campo[:2]] + " LIKE '%,"+campo[2:]+"%')"+\
            " or (" + self.diccampos[campo[:2]] + " LIKE '%"+campo[2:]+",%')"+\
            " or (" + self.diccampos[campo[:2]] + " ='"+campo[2:]+"'))"
        elif campo[:2] == 'l=':#atr%
            sql = "(" + self.diccampos[campo[:2]] + " LIKE '"+campo[2:]+"%')"
        elif campo[:2] == 's=':#atr
            sql = "(" + self.diccampos[campo[:2]] + " LIKE '"+campo[2:]+"')"
        elif self.diccampos.has_key(campo[:2]):#%atr%
            sql = "(" + self.diccampos[campo[:2]] + " LIKE '%"+campo[2:]+"%')"
        else:#no deberia pasar
            print 'error: '
            sql = False

        return sql

    def __generarConsultaCompleja (self, campocomplejo) :
        """ Devuelve el sql del campo complejo buscado """
        #~ print 'generando consulta compleja... ',campocomplejo
        #solo soportado para operadores del mismo tipo,
        #ej: aaa and bbb; cc or ddd or fff
        criterios = []

        if campocomplejo.find(' and ') != -1:
            operador = ' AND ' #en caso de una busqueda con and's
        else: operador = ' OR ' #en caso de una busqueda con or's

        criterios = campocomplejo[2:].split(operador.lower())
        sql = '('
        for criterio in criterios:
            sql += self.__generarConsultaSimple(campocomplejo[:2]+criterio) + operador
        return sql[:-len(operador)] + ')'

    def __generarSQL (self, listadecampos, favorito) :
        """ recibe una lista de campos y genera un sql para realizar la busqueda 
        Si favorito = 1, busca en los favoritos."""

        consulta_sql = "SELECT language,title \nFROM snippet \nWHERE "
        for campo in listadecampos:
                if (campo.find(' and ') == -1) and (campo.find(' or ') == -1):
                    consulta_sql += self.__generarConsultaSimple(campo)
                else:
                    consulta_sql += self.__generarConsultaCompleja(campo)
                consulta_sql += " \nAND "
        if favorito == 1:
            consulta_sql = consulta_sql[:-4] + "AND starred = '1' \nORDER BY language,title"
        else:
            consulta_sql = consulta_sql[:-4] + "ORDER BY language,title"
        return consulta_sql

if __name__ == '__main__':
    b = Busqueda()
    print b.generarConsulta('t=gtk and button,l=python', 0)
