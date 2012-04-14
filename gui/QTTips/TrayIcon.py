import sys
from PyQt4 import QtGui, QtCore

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        """ """
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        menu.addAction("&Ocultar/&Mostrar",self.menuShowHide)
        menu.addSeparator()
        menu.addAction("B&uscar",self.menuSearch)
        menu.addAction("&Agregar Snippet",self.menuAdd)
        menu.addSeparator()
        menu.addAction("&Salir",self.menuExit)
        self.setContextMenu(menu)
        traySignal = "activated(QSystemTrayIcon::ActivationReason)"
        QtCore.QObject.connect(self, QtCore.SIGNAL(traySignal), self.__icon_activated)

        self.__window_parent = parent

    def windowIsShowing(self):
        return self.__window_parent.isVisible ()

    def menuShowHide(self):
        '''menu show'''
        if self.windowIsShowing():
            self.__window_parent.hide()
        else:
            self.__window_parent.show()
            self.__window_parent.eBusqueda.setFocus()

    def menuSearch(self):
        '''menu show'''
        print 'search'
        # establece el foco en la barra de busqueda
        self.__window_parent.eBusqueda.setFocus()
        # si la ventana esta oculta, la muestra
        if not self.windowIsShowing():
            self.__window_parent.show()           

    def menuAdd(self):
        '''menu show'''
        #~ print 'add'
        # abre la ventana de agregar snippet
        self.__window_parent.Padre.showAgregarSnippet()

    def menuExit(self):
        '''menu show'''
        #~ print 'exit'
        sys.exit(0)

    def __icon_activated(self,reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.menuShowHide()
            #print 'Ventana Escondida/mostrada'

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    SystemTrayIcon(QtGui.QIcon("star.png"), w)

#    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
