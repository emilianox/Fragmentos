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

import sqlite3


class sqlite :
    """ Permite manipular bases de datos SQLite."""

    def __init__(self, pathDB) :
        ''' Constructor de la clase
        Parametros:
        - pathDB : ruta de la base de dato que se desea instanciar
        '''
        # ruta del archivo de base de datos
        self.__pathDB = pathDB
        # conecta a la base de datos
        self.__connection = sqlite3.connect(self.__pathDB)
        # activa el cursor
        self.__cursor = self.__connection.cursor()


    def crearTabla (self, nombreTabla, campos) :
        """ Crea una tabla con los datos indicados.

        Parametros:
        - nombreTabla = nombre que va a tener la tabla
        - campos = diccionario con formato clave='nombreCampo';
        valor='tipo sqlite'

        Ejemplo:
        - crearTabla('mi_tabla',{'id_libro':INTEGER, 'libro':VARCHAR(30)})"""

        SQL_CREATE_TABLE = u'CREATE TABLE %s ( \n' %nombreTabla

        # genera los campos de la tabla
        for campo in campos.keys():
            if campo not in ("PK","FK","RF") :
                tipo_campo = campos[campo]
                SQL_CREATE_TABLE += "[{0}] {1} ,\n".format(campo, tipo_campo)
        # quita la ultima coma agregada
        SQL_CREATE_TABLE = SQL_CREATE_TABLE[:-2]

        # si hay PRIMARY KEY, la agrega
        if "PK" in campos.keys():
            # se supone que viene en formato : campo1,campo2
            SQL_CREATE_TABLE += ",\nPRIMARY KEY (%s) " % campos["PK"]
        # si hay FOREIGN KEY, la agrega
        if "FK" in campos.keys() and "RF" in campos.keys():
            # se supone que viene en formato : campo1,campo2
            SQL_CREATE_TABLE += ",\nFOREIGN KEY ({0}) REFERENCES [{1}]\n ".format(campos["FK"],campos["RF"])

        # agrega el ultimo parentesis
        SQL_CREATE_TABLE += ")"

        #~ print SQL_CREATE_TABLE
        if self.realizarNoConsulta(SQL_CREATE_TABLE):
            print 'Tabla %s creada...' %nombreTabla
            return True
        else:
            print 'Error en crearTabla '
            return False

    def crearVista(self, nombreVista, contenidoVista):
        """ Crea una vista en la bd con el nombre indicado y
        la consulta SQL especificada. """

        SQL_CREATE_VISTA = "CREATE VIEW {0} AS \n {1} ".format(nombreVista,contenidoVista)

        if self.realizarNoConsulta(SQL_CREATE_VISTA):
            print 'Vista %s creada...' %nombreVista
            return True
        else:
            print 'Error en crearVista '
            return False

    def ejecutarVista (self, nombreVista) :
        """ Ejecuta la vista indicada. """
        return self.realizarConsulta("SELECT * FROM %s" %nombreVista)
        
    def existeTabla(self, nombreTabla):
        """ """
        
        existe = False
        self.__cursor.execute('Select tbl_name From MAIN.[sqlite_master] where type = "table"')
        # recorre las tablas devueltas para verificar que exista la tabla 'snippet'
        for fila in self.__cursor:
            #~ print fila
            if fila[0] == nombreTabla :
                existe = True
        return existe
                
    def getCantColumnasTabla(self, tabla):
        """ Obtiena la cantidad de Columnas de la tabla."""
        return len(self.getColumnasTabla(tabla))

    def getCantFilasTabla(self, tabla):
        """ Obtiena la cantidad de FILAS de la tabla."""
        return int(self.realizarConsulta('SELECT COUNT(*) FROM '+tabla)[0][0])

    def getColumnasTabla(self, nombreTabla) :
        """ Obtiene los nombres de las columnas de la tabla. """
        columnas = []
        self.__cursor.execute('PRAGMA table_info(' + nombreTabla +')')
        infotable = self.__cursor.fetchall()
        #print infotable
        for row in infotable:
            #print row
            columnas.append(row[1])
        return columnas

    def getDatosColumna (self, tabla, columna, loquebusco, campos = None) :
        """ Recibe un patron y una columna y devuelve las coincidencias
        de dicho patron en la tabla. """

        if campos :
            cursor = self.realizarConsulta("SELECT " + campos + " FROM " + tabla \
                            +" WHERE " + columna + "=" + loquebusco)
        else :
            cursor = self.realizarConsulta("SELECT * FROM " + tabla \
                            +" WHERE " + columna + "=" + loquebusco)
        return  list(list(cursor)[0])

    def getDatosColumnas(self, tabla, criterios, campos = None) :
        """
        Busca en la tabla, segun los criterios indicados.
        Recibe un diccionio donde clave es la columna y valor es el criterio
        de busqueda.
        """
        condiciones = ''
        for campo in criterios.keys() :
            valor = criterios[campo]
            if campo == 'caracteres' :
                campo = 'nombre'
                valor = '_'*valor
                condiciones += campo + " LIKE '" + valor + "' AND "
            else:
                condiciones += campo + " LIKE '%" + valor + "%' AND "

        condiciones = condiciones[:-4]

        # ejecuta la consulta
        if campos :
            consulta = "SELECT %s FROM %s WHERE %s " % (campos,tabla,condiciones)
            #~ consulta = "SELECT %s FROM %s WHERE %s " % (campos,tabla,condiciones)            
        else:
            consulta = "SELECT * FROM %s WHERE %s" % (tabla,condiciones)  
            #~ consulta = "SELECT * FROM %s WHERE %s " % (tabla,condiciones)  
        
        #~ print consulta
        # se obtienen los datos de la consulta
        datos = self.realizarConsulta(consulta)
        #print "la cantidad que hay es ",cantidad_registros
        #print "lo que se quiere enviar son desde ",a_obtener-longitud_parte,'hasta',len(datos)

        resultado = datos
        return resultado
    
    def getDatosTabla (self, tabla, campos = None) :
        """ Obtiene una lista con todos los datos de la tabla. """
        if campos is None:
            return self.realizarConsulta('SELECT * FROM ' + tabla)
        else:
            return self.realizarConsulta('SELECT ' + campos + ' FROM ' + tabla)

    def getDatosPatronColumna (self, tabla, patron, columna) :
        """ Recibe un patron y una columna y devuelve las
        coincidencias de dicho patron en la tabla. """

        return self.realizarConsulta("SELECT * FROM "+ tabla \
                            +" WHERE "+columna+" LIKE '%"+patron+"%'")

    def getDatosPatronColumnasEspecificas(self, tabla, patron, columna, listacolumnas):
        """Recibe un patron, una columna y una lista de columnas a devolver
        que cumplan con esos requisitos"""

        listamatch, lista,items = self.getDatosPatronColumna(tabla, patron, columna), [],[]
        for registro in listamatch:
            for ncolumna in listacolumnas:
                items.append(registro[ncolumna])
            lista.append(items)
            items = []

        return lista

    def getEstructuraTabla(self, nombreTabla) :
        """ 
        Devuelve un diccionario con la estructura de la tabla, 
        donde clave = nombre del campo, 
        y valor = tipo dato campo.
        """
        self.__cursor.execute('PRAGMA table_info(' + nombreTabla + ')')
        infotable = self.__cursor.fetchall()
        
        estructura = {}
        for row in infotable :
            # row[1] = nombre_campo
            # row[2] = tipo_campo
            estructura[row[1]] = row[2]
        return estructura
        
    def getFilasSegunPatronEnTabla (self, tabla, patron) :
        """ Recibe un patron(string) y devuelve todas las filas
        donde se encuentra dicho patron. """

        return self.realizarConsulta("SELECT * FROM " + tabla + \
                                " WHERE * LIKE '%" + patron + "%'")

    def getTiposCampos(self, nombreTabla):
        """ Obtiene los tipos de los campos de la tabla. """
        lista = []
        self.__cursor.execute('PRAGMA table_info(' + nombreTabla + ')')
        infotable = self.__cursor.fetchall()
        #print infotable
        for row in infotable:
            #print row
            lista.append(row[2])
        return lista

    def getTablas(self):
        """Devuleve una lista con los nombres de las tablas en la bd."""
        lista = []
        self.__cursor.execute('select * from sqlite_master')
        infotable = self.__cursor.fetchall()
        #print infotable
        for row in infotable:
            #print row[2]
            lista.append(row[2])
        return lista
    
    def realizarConsulta (self, consulta) :
        """ Ejecuta la consulta SQL indicada. """
        try:
            cursor_temp = self.__cursor.execute(consulta)
            lista = []
            for fila in cursor_temp:
                lista.append(fila)
            return lista
        except sqlite3.OperationalError, msg:
            print msg
            return None

    def realizarNoConsulta (self, noconsulta, parametros = None) :
        """ Ejecuta la consulta SQL indicada para operaciones que
        no devuelvan valores como resultado.

        Ejemplo: update, drop, insert, alter, etc."""
        try:
            if parametros is None :
                self.__cursor.execute(noconsulta)
            else:
                self.__cursor.execute(noconsulta, parametros)
            self.__connection.commit()
            return True
        except sqlite3.OperationalError, msg:
            print 'realizarNoConsulta error: ',msg
            return False

    def realizarAlta (self, tabla, datos) :
        """ Realiza un INSERT en la tabla y campos indicados.

        Parametros:
        - tabla = tabla donde se insertara el registro
        - datos = diccionario con formato {'nombre_campo':valor_campo}
        """

        # genera los signos de preguntas segun la cantidad de campos recibidos
        questions = str('('+'?,'*len(datos))[:-1] + ')'
        # genera un string con los nombre de los campos
        nombres_campos = '('+','.join(datos.keys())+')'

        # genera el sql con el insert
        SQL_ALTA = u'INSERT INTO {0} {1} VALUES {2}'.format(tabla,nombres_campos,questions)
        #~ print SQL_ALTA
        valores_a_insertar= []
        # lee los valores del diccionario, y los carga en una listas
        for valor in datos.values():
            valores_a_insertar.append(valor)

        if self.realizarNoConsulta(SQL_ALTA, valores_a_insertar):
            print 'Alta realizada con exito en la tabla <%s>...' %tabla
            return True
        else :
            print 'Error en realizarAlta... '
            return False

    def realizarAltas (self, tabla, ordencampos, listadedatos) :
        """ Realiza los N INSERTS segun la cantidad de
        elementos haya en la lista/tupla reciba como parametro.

        Parametros:
        - tabla = nombre tabla donde se insertaran los registros
        - ordencampos = diccionario con formato: {"campo_1": 1,"campo_2": 0},
        donde cada <clave>, es el nombre del campo de la tabla; y donde
        cada <valor>, es el indice del dato que se va a insertar.
        - listadedatos = lista/tupla que contiene los datos a insertarce."""

        # genera los signos de preguntas segun la cantidad de campos recibidos
        questions = str('('+'?,'*len(ordencampos))[:-1] + ')'
        # genera un string con los nombre de los campos
        nombres_campos = '('+','.join(ordencampos.keys())+')'

        # genera el sql con el insert
        SQL_ALTA = u'INSERT INTO {0} {1} VALUES {2}'.format(tabla,nombres_campos,questions)

        nrreg_total = len(listadedatos)
        print SQL_ALTA

        try:
            # recorre, insertando en la bd/tabla los registros
            for nrreg_actual, a_insertar in enumerate(listadedatos):

                valores_a_insertar = []

                # carga en el orden indicado en el diccionario
                # los datos, a la lista que se insertara actualmente
                for valor in ordencampos.keys():
                    indice = ordencampos[valor]
                    valores_a_insertar.append(a_insertar[indice])

                # inserta el registro en la bd
                self.__cursor.execute(SQL_ALTA, valores_a_insertar)

                print 'Alta %d de %d realizada con exito en la tabla <%s>...' % (nrreg_actual+1,nrreg_total,tabla)

            # confirma los cambios en la bd
            self.__connection.commit()
            return True
        except Exception, msg:
            self.__connection.rollback()
            print 'realizarAltas error: ',msg
            return False

    def realizarBaja (self, tabla, condiciones) :
        """ Realiza un DELETE en la tabla dicha, con las condiciones indicadas
        SI RECIBE '*' COMO CONDICION, BORRA TODO EL CONTENIDO DE LA TABLA.

        Parametros :
        - tabla = nombre tabla donde se realizara la baja
        - condiciones = lista o tupla, que contiene las restricciones
        quue deben cumplir los registros.

        Ejemplo: ["id_libro = 21","nombre_libro = 'Sqlite es genial!!!' "]
        """

        SQL_BAJA = u'DELETE FROM %s ' %tabla

        # genera los WHERE a partir de las condiciones
        # NOTA: SOLO FUNCIONA PARA OPERADORES <AND>

        if condiciones != "*" :
            SQL_BAJA += "WHERE "
            for condicion in condiciones:
                SQL_BAJA += condicion + " AND "
            # quita el ultimo and
            SQL_BAJA = SQL_BAJA[:-4]
        #~ print SQL_BAJA
        if self.realizarNoConsulta(SQL_BAJA):
            print 'Baja realizada con exito en la tabla <%s>...' %tabla
            return True
        else:
            print 'Error en realizarBaja '
            return False

    def realizarModificacion (self, tabla, sets, condiciones) :
        """ Realiza un UPDATE en la tabla y campos indicados, que
        cumplan con las condiciones especificadas.

        Parametros:
        - tabla = string,
        - sets = diccionario con formato {'nombre_campo':nuevo_valor}
        - condiciones = lista o tupla con formato
        ['campo > 10',"otro_campo = 'algun_valor' "]"""

        SQL_MODIFICACION = u'UPDATE %s ' %tabla
        SETS, WHERES = 'SET', 'WHERE '

        # genera los SETS a partir de 'sets'
        for campo in sets.keys():
            valor = sets[campo]
            SETS += " {0} = {1} ,".format(campo,valor)
        # quita la ultima coma agregada
        SETS = SETS[:-1]

        # genera los VHERES a partir de 'condiciones'
        for condicion in condiciones:
            WHERES += condicion + " AND "
        WHERES = WHERES[:-4]

        # concatena los resultados
        SQL_MODIFICACION += SETS + WHERES
        print SQL_MODIFICACION
        if self.realizarNoConsulta(SQL_MODIFICACION):
            print 'Modificacion realizada con exito a la tabla <%s>...' %tabla
            return True
        else:
            print 'Error en realizarModificacion '
            return False

def main():

    #~ INSTANCIAR LA CLASE
    p = sqlite('/media/Data/Dropbox/Proyectos/Daila/data/horacio.db')
    #~ p.getDatosColumnas('fruta',{'nombre':'gooble','extencion':'com','otro':'lala'})
    #~ CREAR UNA TABLA
    #~ prueba.crearTabla("alumnos",{
    #~ "id_alumno":"int not null",
    #~ "PK":"id_alumno",
    #~ "nombre_alumno":"varchar(20) not null",
    #~ "ap_alumno":"varchar(20)"})

    #~ INSERTAR UN REGISTRO
    #~ prueba.realizarAlta("alumnos",{"id_alumno":1,"nombre_alumno":"Alberto","ap_alumno":"Ferro"})
    #~ prueba.realizarAlta("alumnos",{"id_alumno":2,"nombre_alumno":"Alvaro","ap_alumno":"Gutierrez"})
    #~ prueba.realizarAlta("alumnos",{"id_alumno":3,"nombre_alumno":"Ayelen","ap_alumno":"Lopez"})

    #~ prueba.realizarModificacion("alumnos",{"id_alumno":4},("id_alumno = 1",))

    #~ prueba.realizarBaja("alumnos",["id_alumno = 1"])

    #~ print prueba.realizarConsulta("select * from alumnos")

    # bd = sqlite('test_prueba.db')
    # bd.crearTabla('prueba', {'campo_a':'text','campo_b':'text','campo_c':'text'})
    # print bd.getEstructuraTabla('prueba')

    #print p.getTablas()
    pass

if __name__ == '__main__':
    main()

