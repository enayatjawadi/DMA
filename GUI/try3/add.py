# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QCheckBox
from shutil import copyfile
from random import seed
from random import randint
import os.path

class Ui_MainWindow(QMainWindow):

    def clearForm(self):
        print("Clear clicked")
        self.questionText.setText("")
        self.answerText.setText("")
        self.qPicture_2.setPixmap(self.pixmap)
        self.aPicture_2.setPixmap(self.pixmap2)
        self.thesaurusInit()
        self.packageInit()
        if(self.pictureCard):
            self.question = ""+str(randint(10000, 1000000))

    def thesaurusInit(self):
        self.thesaurus.addItem("Choose a group")
        self.thesaurus.addItem("homonyms")
        self.thesaurus.setCurrentIndex(0)

    def packageInit(self):
        self.packages.addItem("Default package")
        self.packages.addItem("English")
        self.packages.addItem("French")
        self.packages.setCurrentIndex(0)


    def pickQuestionImage(self, other):
        if(self.pictureCard == False):
            self.question = self.questionText.toPlainText()
        dst = "Images/"+self.question+"_front.jpg"
        dst2 = "Images/"+self.question+"_back.jpg"
        if(len(self.questionText.toPlainText()) == 0 and self.pictureCard == False):
            err = QMessageBox()
            err.setText("Enter the question first!")
            err.setWindowTitle("No question yet")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()

        elif (os.path.exists(dst) and self.pictureCard == False):
            """ Tell the suer the word already exists in the database """
            err = QMessageBox()
            err.setText("You already have this question, try another one")
            err.setWindowTitle("Duplicate question")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()
        elif ((os.path.exists(dst) or os.path.exists(dst2)) and self.pictureCard == True and aPictureSet == False):
            print("Original: "+dst+"  "+dst2)
            self.question = ""+str(randint(10000, 100000000))
            dst = "Images/"+self.question+"_front.jpg"
            print( '2 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if filename[0]:
                copyfile(filename[0], dst)
                pixmp = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True
        
        elif ((os.path.exists(dst) or os.path.exists(dst2)) and self.pictureCard == True and aPictureSet == True):
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if(filename[0]):
                copyfile(filename[0], dst)
                pixmp = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True

        elif (os.path.exists(dst) == False and self.pictureCard == False):
            print('3 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if filename[0]:
                copyfile(filename[0], dst)
                pixmp = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True
        elif (os.path.exists(dst) == False and os.path.exists(dst2) == False and self.pictureCard == True):
            print('4 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if(filename[0]):
                copyfile(filename[0], dst)
                pixmp = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True


    def pickAnswerImage(self, other):
        if(self.pictureCard == False):
            self.question = self.questionText.toPlainText()
        dst = "Images/"+self.question+"_back.jpg"
        dst2 = "Images/"+self.question+"_front.jpg"

        if (len(self.questionText.toPlainText()) == 0 and self.pictureCard == False):
            err = QMessageBox()
            err.setText("Enter the question first!")
            err.setWindowTitle("No question yet")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()

        elif (os.path.exists(dst) and self.pictureCard == False):
            """ tell the user to change the word """
            err = QMessageBox()
            err.setText("You already have this question, try another one")
            err.setWindowTitle("Duplicate question")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()
        elif (os.path.exists(dst) == False and self.pictureCard == False):
            print('2')
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.jpg)")
            if filename[0]:
                copyfile(filename[0], dst)
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True
        elif ((os.path.exists(dst) or os.path.exists(dst2)) and self.pictureCard == True and self.qPictureSet == False):
            print('3 '+dst)
 #           seed(2)
            self.question = ""+str(randint(10000, 1000000))+str(self.qPictureSet)
            dst = "Images/"+self.question+"_back.jpg"
            print("After modification: "+self.question)
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if(filename[0]):
                copyfile(filename[0], dst)
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True
        
        elif ((os.path.exists(dst) or os.path.exists(dst2)) and self.pictureCard == True and self.qPictureSet == True):
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if(filename[0]):
                copyfile(filename[0], dst)
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True

        elif (os.path.exists(dst) == False and os.path.exists(dst2) == False and self.pictureCard == True):
            print('4 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Image files (*.jpg *.png)")
            if(filename[0]):
                copyfile(filename[0], dst)
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True

    def enter_data(self):
        # TODO should rename the pictures if the question text or pictureCard flag has been changed (compare the file names and rename the pictures if necessary
        pass

    def pictureCardCheck(self):
        if(self.justPicture.isChecked()):
            self.questionText.setReadOnly(True)
            self.answerText.setReadOnly(True)
            self.pictureCard = True
#            seed(1)
            self.question = ""+str(randint(10000, 100000000000))
            print(self.question)
        else:
            self.questionText.setReadOnly(False)
            self.answerText.setReadOnly(False)
            self.pictureCard = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Digital Memory Assistant")
        MainWindow.resize(800, 600)
        self.question = '321657484984968'
        self.pictureCard = False
        self.qPictureSet = False
        self.aPictureSet = False
        self.qwidget = self
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 2396, 1615))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_3.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_3.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.qestionLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qestionLabel.sizePolicy().hasHeightForWidth())
        self.qestionLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.qestionLabel.setFont(font)
        self.qestionLabel.setObjectName("qestionLabel")
        self.horizontalLayout.addWidget(self.qestionLabel)
        
        self.justPicture = QCheckBox("Picture-only card")
        self.justPicture.setSizePolicy(sizePolicy)
        self.justPicture.setFont(font)
        self.justPicture.stateChanged.connect(self.pictureCardCheck)
        self.horizontalLayout.addWidget(self.justPicture)

        self.AnswerLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AnswerLabel.sizePolicy().hasHeightForWidth())
        self.AnswerLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.AnswerLabel.setFont(font)
        self.AnswerLabel.setObjectName("AnswerLabel")
        self.horizontalLayout.addWidget(self.AnswerLabel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.questionText = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_3)
        self.questionText.setObjectName("questionText")
        self.horizontalLayout_2.addWidget(self.questionText)
        self.answerText = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_3)
        self.answerText.setObjectName("answerText")
        self.horizontalLayout_2.addWidget(self.answerText)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.qPicture_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qPicture_2.sizePolicy().hasHeightForWidth())
        self.qPicture_2.setSizePolicy(sizePolicy)
        self.qPicture_2.setText("")
        self.pixmap = QtGui.QPixmap("Images/olaf1.jpg").scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.qPicture_2.setPixmap(self.pixmap)
        self.qPicture_2.setAlignment(QtCore.Qt.AlignCenter)
        self.qPicture_2.setObjectName("qPicture_2")

        self.qPicture_2.mouseReleaseEvent = self.pickQuestionImage

        self.horizontalLayout_3.addWidget(self.qPicture_2)
        self.aPicture_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aPicture_2.sizePolicy().hasHeightForWidth())
        self.aPicture_2.setSizePolicy(sizePolicy)
        self.aPicture_2.setText("")
        self.pixmap2 = QtGui.QPixmap("Images/olaf2.jpg").scaled(311, 201, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.aPicture_2.setPixmap(self.pixmap2)
        self.aPicture_2.setAlignment(QtCore.Qt.AlignCenter)
        self.aPicture_2.setObjectName("aPicture_2")
        
        self.aPicture_2.mouseReleaseEvent = self.pickAnswerImage
        
        self.horizontalLayout_3.addWidget(self.aPicture_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.thesaurus = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.thesaurus.sizePolicy().hasHeightForWidth())
        self.thesaurus.setSizePolicy(sizePolicy)
        self.thesaurus.setObjectName("thesaurus")
        self.horizontalLayout_6.addWidget(self.thesaurus)
        self.newGroup = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newGroup.sizePolicy().hasHeightForWidth())
        self.newGroup.setSizePolicy(sizePolicy)
        self.newGroup.setObjectName("newGroup")
        self.horizontalLayout_6.addWidget(self.newGroup)
        self.packages = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.packages.sizePolicy().hasHeightForWidth())
        self.packages.setSizePolicy(sizePolicy)
        self.packages.setObjectName("packages")
        self.horizontalLayout_6.addWidget(self.packages)
        self.newPackage = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newPackage.sizePolicy().hasHeightForWidth())
        self.newPackage.setSizePolicy(sizePolicy)
        self.newPackage.setObjectName("newPackage")
        self.horizontalLayout_6.addWidget(self.newPackage)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.enter_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.enter_2.sizePolicy().hasHeightForWidth())
        self.enter_2.setSizePolicy(sizePolicy)
        self.enter_2.setObjectName("enter_2")
        self.horizontalLayout_7.addWidget(self.enter_2)
        self.clear = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear.sizePolicy().hasHeightForWidth())
        self.clear.setSizePolicy(sizePolicy)
        self.clear.setObjectName("clear")
        self.clear.clicked.connect(self.clearForm)
        self.horizontalLayout_7.addWidget(self.clear)
        self.cancel = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancel.sizePolicy().hasHeightForWidth())
        self.cancel.setSizePolicy(sizePolicy)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout_7.addWidget(self.cancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.thesaurusInit()
        self.packageInit()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digital Memory Assistant"))
        self.qestionLabel.setText(_translate("MainWindow", "Question"))
        self.AnswerLabel.setText(_translate("MainWindow", "Answer"))
        self.label_6.setText(_translate("MainWindow", "Thesaurus"))
        self.label_8.setText(_translate("MainWindow", "Package"))
        self.newGroup.setText(_translate("MainWindow", "New Group"))
        self.newPackage.setText(_translate("MainWindow", "New Package"))
        self.enter_2.setText(_translate("MainWindow", "Enter"))
        self.clear.setText(_translate("MainWindow", "Clear"))
        self.cancel.setText(_translate("MainWindow", "cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())