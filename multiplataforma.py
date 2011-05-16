#!/usr/bin/python
# -*- coding: utf-8 -*-

class Multiplataforma():

    def convertpath(self,path):
        """Convierte el path a el específico de la plataforma (separador)"""
        import os
        if os.name == 'posix':
            return "/"+apply( os.path.join, tuple(path.split('/')))
        elif os.name == 'nt':
            return apply( os.path.join, tuple(path.split('/')))
