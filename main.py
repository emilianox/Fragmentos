#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Copyright 2011 Emiliano Fernandez <emilianohfernandez@gmail.com>
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
from fragmentos import Fragmentos

class Main :

    def __init__(self) :
        self.Fragmentos = Fragmentos()
        
    def validar (self) :
        # returns
        pass


def main():
    import os
    if os.name == 'posix':
        import fcntl
        pid_file = 'Singleton'
        fp = open(pid_file, 'w')
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            ventana = Main()
            gtk.main()
            exit(0)

        except IOError:
            # another instance is running
            print 'Ya hay otra instancia corriendo. Ciao'
            exit(0)
    elif os.name == 'nt':
        ventana = VentanaPrincipal()
        gtk.main()
        exit(0)

if __name__ == '__main__':
    main()

