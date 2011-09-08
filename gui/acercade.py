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

import os,sys

from PyQt4 import QtGui, uic


class AcercaDe(QtGui.QDialog):
    
    def __init__(self):
        FILENAME = 'wAcercaDe.ui'
        QtGui.QDialog.__init__(self)
    #cargamos la interfaz desde el archivo .ui
        uifile = os.path.join(os.path.abspath(os.path.dirname(__file__)),FILENAME)
        uic.loadUi(uifile, self)
        
        self.lbLogo.setPixmap(QtGui.QPixmap('logo.png'))
        self.lbLogo.setScaledContents(True)

    
def main():
    app = QtGui.QApplication(sys.argv)
    window = AcercaDe()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
