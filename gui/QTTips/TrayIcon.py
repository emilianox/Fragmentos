import sys
from PyQt4 import QtGui, QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        """ """
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        menu.addAction("Hide/&Show",self.menuShowHide)
        menu.addSeparator()
        menu.addAction("S&earch",self.menuSearch)
        menu.addAction("&Add",self.menuAdd)
        menu.addSeparator()
        menu.addAction("&Exit",self.menuExit)
        self.setContextMenu(menu)
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        QtCore.QObject.connect(self, QtCore.SIGNAL(traySignal), self.__icon_activated)

        self.__window_parent = parent
        self.__bandera_show = True


    def menuShowHide(self):
        '''menu show'''
        if self.__bandera_show:
            self.__window_parent.hide()
            self.__bandera_show = False
        else:
            self.__window_parent.show()
            self.__bandera_show = True
        pass

    def menuSearch(self):
        '''menu show'''
        print 'search'
        pass

    def menuAdd(self):
        '''menu show'''
        print 'add'
        pass

    def menuExit(self):
        '''menu show'''
        print 'exit'
        pass

    def __icon_activated(self,reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.menuShowHide()
            print 'Ventana Escondida/mostrada'

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("star.png"), w)

#    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
