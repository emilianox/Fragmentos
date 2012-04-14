#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
#
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

import dbus

bus = dbus.SessionBus()

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        if sys.argv[1] == '-add':
            try:
                mi_service = bus.get_object('ar.fragmentos.service', '/ar/fragmentos/service')
                metodo = mi_service.get_dbus_method('showAgregarSnippet', 'ar.fragmentos.service')
                print metodo()
            except dbus.exceptions.DBusException,argument:
                print('No esta abierto fragmentos')
        if sys.argv[1] == '-search':
            try:
                mi_service = bus.get_object('ar.fragmentos.service', '/ar/fragmentos/service')
                metodo = mi_service.get_dbus_method('showBuscarSnippet', 'ar.fragmentos.service')
                print metodo()
            except dbus.exceptions.DBusException,argument:
                print('No esta abierto fragmentos')             
    else:
        print "Este programa necesita un parámetro"
    



