#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from gui import TrayIcon

app = QtGui.QApplication(sys.argv)

w = QtGui.QWidget()
trayIcon = TrayIcon.SystemTrayIcon(QtGui.QIcon("gui/star.png"), w)

trayIcon.show()
sys.exit(app.exec_())

