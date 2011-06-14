class Busqueda :
    '''(NULL)'''
    def generarConsulta (self, labusqueda) :
        """ recibe la busqueda completa y genera un sql para realizar la busqueda """
        listadecriterios = self.__separarPorCampos(labusqueda)
        sql = self.__generarSQL(listadecriterios)
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
                listadecriterios.append(labusqueda)
            else:
            #caso en que tengas todo ej: t=hola,l=python
                listadecriterios = labusqueda.split(',')
        return listadecriterios

    def __generarConsultaSimple (self, campo) :
        """ devuelve el sql del campo simple buscado """
        #esto es para __generarSQL
        #preconsulta = 'SELECT language,title FROM snippet ORDER BY language,title where '
        #~ print 'generando consulta simple... ',campo

        diccampos = {'t=' : 'title', 'l=':'language', 'g=':'tags', 'c=':'contents',
        'd=':'description','r=':'references','n=':'creation','m=':'modified',
        'u=':'uploader', 's=': 'starred'}

        #~ campo = 'g=agua'
        if campo[:2] == 'g=':#%,atr,%-%,atr-atr,%-atr
            sql = "((" + diccampos[campo[:2]] + " LIKE '%,"+campo[2:]+",%')"+\
            " or (" + diccampos[campo[:2]] + " LIKE '%,"+campo[2:]+"%')"+\
            " or (" + diccampos[campo[:2]] + " LIKE '%"+campo[2:]+",%')"+\
            " or (" + diccampos[campo[:2]] + " ='"+campo[2:]+"'))"
        elif campo[:2] == 'l=':#atr%
            sql = "(" + diccampos[campo[:2]] + " LIKE '"+campo[2:]+"%')"
        elif campo[:2] == 's=':#atr
            sql = "(" + diccampos[campo[:2]] + " LIKE '"+campo[2:]+"')"
        elif diccampos.has_key(campo[:2]):#%atr%
            sql = "(" + diccampos[campo[:2]] + " LIKE '%"+campo[2:]+"%')"
        else:#no deberia pasar
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

    def __generarSQL (self, listadecampos) :
        """ recibe una lista de campos y genera un sql para realizar la busqueda """
        
        consulta_sql = "SELECT language,title \nFROM snippet \nWHERE "
        for campo in listadecampos:
                if (campo.find(' and ') == -1) and (campo.find('or') == -1):
                    consulta_sql += self.__generarConsultaSimple(campo)
                else:
                    consulta_sql += self.__generarConsultaCompleja(campo)
                consulta_sql += " \nAND "
        consulta_sql = consulta_sql[:-4] + "ORDER BY language,title"
        return consulta_sql

if __name__ == '__main__':
    b = Busqueda()
    print b.generarConsulta('t=gtk and button,l=python')
