# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.review = QtWidgets.QPushButton(self.centralwidget)
        self.review.setGeometry(QtCore.QRect(290, 190, 211, 181))
        self.review.setObjectName("review")
        self.newCard = QtWidgets.QPushButton(self.centralwidget)
        self.newCard.setGeometry(QtCore.QRect(580, 40, 121, 111))
        self.newCard.setObjectName("newCard")
        self.thesaurus = QtWidgets.QPushButton(self.centralwidget)
        self.thesaurus.setGeometry(QtCore.QRect(90, 40, 121, 111))
        self.thesaurus.setObjectName("thesaurus")
        self.packages = QtWidgets.QPushButton(self.centralwidget)
        self.packages.setGeometry(QtCore.QRect(90, 410, 121, 111))
        self.packages.setObjectName("packages")
        self.viewBox = QtWidgets.QPushButton(self.centralwidget)
        self.viewBox.setGeometry(QtCore.QRect(580, 410, 121, 111))
        self.viewBox.setObjectName("viewBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.review.setText(_translate("MainWindow", "Review"))
        self.newCard.setText(_translate("MainWindow", "New card"))
        self.thesaurus.setText(_translate("MainWindow", "thesaurus"))
        self.packages.setText(_translate("MainWindow", "packages"))
        self.viewBox.setText(_translate("MainWindow", "View Box"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
