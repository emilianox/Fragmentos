#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Informática MEG <contacto@informaticameg.com>
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

class method(object):
    """Clase decoradora que falsifica al service de dbus"""
    def __init__(self,a):
        print a

    def __call__(self,*args,**kwargs):
        def deco(classmother):
            return funcion(classmother)
        funcion = args[0]
        return deco


class Vacia:
    """Esqueleto de clases vacias para herencia falsificada"""
    def __init__(self):
        pass



def main():
    pass

if __name__ == '__main__':
    main()
