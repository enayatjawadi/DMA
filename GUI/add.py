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
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import re, string
#import pyttsx3
from gtts import gTTS
from playsound import playsound
import sqlite3

class Ui_MainWindow(QMainWindow):

    def createMainTable(self):
        conn = sqlite3.connect("DMA.db")
        cur = conn.cursor()
        #cur.execute('DROP TABLE IF EXISTS mainTable')
        cur.execute("""CREATE TABLE IF NOT EXISTS mainTable(     
        question TEXT PRIMARY KEY,
        answer TEXT,
        picture_only INTEGER,
        level INTEGER,
        deck INTEGER,
        pic_front TEXT,
        pic_back TEXT,
        group_name TEXT,
        subGroup TEXT,
        package TEXT);""")
        conn.commit()
        conn.close()

    def createThesaurusTable(self):
        conn = sqlite3.connect("DMA.db")
        cur = conn.cursor()
        #cur.execute('DROP TABLE IF EXISTS thesaurus')
        cur.execute("""CREATE TABLE IF NOT EXISTS thesaurus(
        group_name TEXT PRIMARY KEY,
        subGroups TEXT);""")
        conn.commit()
        conn.close()

    def createPackageTable(self):
        conn = sqlite3.connect("DMA.db")
        cur = conn.cursor()
        #cur.execute('DROP TABLE IF EXISTS packages')
        cur.execute("""CREATE TABLE IF NOT EXISTS packages(
        package TEXT PRIMARY KEY);""")

        conn.commit()
        conn.close()

    def insertCard(self):
        conn = sqlite3.connect("DMA.db")
        cur = conn.cursor()

        if self.pictureCard:
            pic = 1;
        else:
            pic = 0
        
        questionField = self.questionField
        answerField = self.answerField
        level = self.level
        deck = self.deck
        qPicName = self.qPicName        
        aPicName = self.aPicName
        questionGroup = self.questionGroup
        questionSubGroup = self.questionSubGroup
        questionPackage = self.questionPackage
    

        cur.execute(f'INSERT INTO mainTable VALUES("{questionField}", "{answerField}", {pic}, {level}, {deck}, "{qPicName}", "{aPicName}", "{questionGroup}", "{questionSubGroup}", "{questionPackage}");')
        
        conn.commit()
        
        # TODO Insert data into thesaurus and packages tables too AFTER clicking the add button

        conn.close()

    def dbInit(self):
        self.createMainTable()
        self.createThesaurusTable()
        self.createPackageTable()

    def qName(self, txt):
        pattern = re.compile('[^a-zA-Z0-9]')
        print(pattern.sub('', txt))
        return pattern.sub('',txt)

    def findOrientation(self, image):
        if "exif" in image.info:
            exif_dict = piexif.load(image.info["exif"])
            if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                print("Orientation: "+str(orientation))
                return orientation

    def clearForm(self):
        print("Clear clicked")
        self.thesaurus.currentIndexChanged.connect(self.thesaurusSelected)
        self.packages.currentIndexChanged.connect(self.packageSelected)
        self.thesaurusInit()
        self.packageInit()        
        self.questionText.setText("")
        self.answerText.setText("")
        self.qPicture_2.setPixmap(self.pixmap)
        self.aPicture_2.setPixmap(self.pixmap2)
        if(self.pictureCard):
            self.question = ""+str(randint(10000, 1000000))

    def thesaurusInit(self):
        print("Thesaurus init")
        self.thesaurus.clear()
        self.groupData.clear()
        self.groupData.append("Choose a group")
        self.groupData.append("homonyms")
        self.thesaurus.addItems(self.groupData)
#        self.thesaurus.model().item(0).setEnabled(False)
        self.thesaurus.setCurrentIndex(0)

    def thesaurusSelected(self, indx):
        print("Thesaurus index: "+str(indx))
        if(indx == 0):
            self.questionGroup = "none"
        else:
            self.questionGroup = self.groupData[indx]
        #self.questionSubGroup = self.subGroupData(indx) 
        print(self.questionGroup)

    def packageSelected(self, indx):
        print("Package index: "+str(indx))
        if(indx == 0):
            self.questionPackage = "none"
        else:
            self.questionPackage = self.packageData[indx]

    def packageInit(self):
        self.packages.clear()
        self.packageData.clear()
        self.packageData.append("Default package")
        self.packageData.append("General")
        self.packageData.append("English")
        self.packageData.append("French")
        self.packages.addItems(self.packageData)
        self.packages.model().item(0).setEnabled(False)
        self.packages.setCurrentIndex(0)

    def boxPartInit(self):
        self.boxPart.clear()
        self.partData = []
        self.boxPart.addItem("Level")
        for i in range (1, 6):
            self.partData.append(str(i))
        
        self.boxPart.addItems(self.partData)

        self.boxPart.setCurrentIndex(0)
        self.boxPart.model().item(0).setEnabled(False)

    def partSectionInit(self):
        self.partSection.clear()
        self.partSection.addItem("Deck")
        self.partSection.setCurrentIndex(0)
        self.partSection.model().item(0).setEnabled(False)

    def sectionSet(self, section):
        self.deck = section

    def sectionUpdate(self, part):
        self.sectionData = []
        self.partSection.clear()
        self.level = part
        self.partSection.addItem("Deck")
        if part == 1:
            self.sectionData.append("1")
        
        elif part == 2:
            self.sectionData.append("1")
            self.sectionData.append("2")
        
        elif part == 3:
            for i in range(1, 5):
                self.sectionData.append(str(i))
                
        elif part == 4:
            for i in range(1, 9):
                self.sectionData.append(str(i))

        elif part == 5:
            for i in range (1, 17):
                self.sectionData.append(str(i))

        self.partSection.addItems(self.sectionData)
        self.partSection.setCurrentIndex(0)
        self.partSection.model().item(0).setEnabled(False)


    def pickQuestionImage(self, other):
        if(self.pictureCard == False):
            self.question = self.qName(self.questionText.toPlainText())
        dst = "Images/"+self.question+"_front.jpg"
        dst2 = "Images/"+self.question+"_back.jpg"
        if(len(self.questionText.toPlainText()) == 0 and self.pictureCard == False):
            err = QMessageBox()
            err.setText("Enter the question first!")
            err.setWindowTitle("No question yet")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()

        elif (os.path.exists(dst) and self.pictureCard == False and self.qPictureSet == False):
            """ Tell the suer the word already exists in the database """
            err = QMessageBox()
            err.setText("You already have this question, try another one")
            err.setWindowTitle("Duplicate question")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()
        elif (os.path.exists(dst) and self.qPictureSet == True):
            #remove the previous photo from Images directory, then copy the new one
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if(filename[0]):
                self.qSrc = filename[0]
                os.remove(dst)
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(-90))
                picname = os.path.basename(filename[0])
                self.qPicName = os.path.basename(dst)
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath

                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True

        elif ((os.path.exists(dst) or os.path.exists(dst2)) and self.pictureCard == True and self.aPictureSet == False):
            print("Original: "+dst+"  "+dst2)
            self.question = ""+str(randint(10000, 100000000))
            dst = "Images/"+self.question+"_front.jpg"
            print( '2 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if filename[0]:
                self.qSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(-90))

                picname = os.path.basename(filename[0])
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath

                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True
        
        elif (os.path.exists(dst2) and self.aPictureSet == True and self.qPictureSet == False):
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if(filename[0]):
                self.qSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(-90))

                picname = os.path.basename(filename[0])
                picpath = filename[0].replace(picname, "")
                self.qPicName = os.path.basename(dst)
                self.picPath = picpath
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True

        elif (os.path.exists(dst) == False and self.pictureCard == False):
            print('3 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if filename[0]:
                self.qSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(-90))


                picname = os.path.basename(filename[0])
                picpath = filename[0].replace(picname, "")
                self.qPicName = os.path.basename(dst)
                self.picPath = picpath
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True
        elif (os.path.exists(dst) == False and os.path.exists(dst2) == False and self.pictureCard == True):
            print('4 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if(filename[0]):
                self.qSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp = pixmp.transformed(QtGui.QTransform().rotate(-90))
                picname = os.path.basename(filename[0])
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath
               
                self.qPicture_2.setPixmap(pixmp)
                self.qPictureSet = True
    

    def pickAnswerImage(self, other):
        if(self.pictureCard == False):
            self.question = self.qName(self.questionText.toPlainText())
        dst = "Images/"+self.question+"_back.jpg"
        dst2 = "Images/"+self.question+"_front.jpg"

        if (len(self.questionText.toPlainText()) == 0 and self.pictureCard == False):
            err = QMessageBox()
            err.setText("Enter the question first!")
            err.setWindowTitle("No question yet")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()

        elif (os.path.exists(dst) and self.pictureCard == False and self.aPictureSet == False):
            """ tell the user to change the word """
            err = QMessageBox()
            err.setText("You already have this question, try another one")
            err.setWindowTitle("Duplicate question")
            err.setStandardButtons(QMessageBox.Ok)
            err.exec_()
        elif (os.path.exists(dst) and self.aPictureSet == True):
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if filename[0]:
                self.aSrc = filename[0]
                os.remove(dst)
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(-90))

                picname = os.path.basename(filename[0])
                self.aPicName = os.path.basename(dst)
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath
                self.aPicPath = dst
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True

        elif (os.path.exists(dst) == False and self.pictureCard == False):
            print('2')
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if filename[0]:
                self.aSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(-90))

                picname = os.path.basename(filename[0])
                picpath = filename[0].replace(picname, "")
                self.aPicName = os.path.basename(dst)
                self.picPath = picpath
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True
        elif ((os.path.exists(dst) or os.path.exists(dst2)) and self.pictureCard == True and self.qPictureSet == False and self.aPictureSet == False):
            print('3 '+dst)
            self.question = ""+str(randint(10000, 1000000))
            dst = "Images/"+self.question+"_back.jpg"
            print("After modification: "+self.question)
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if(filename[0]):
                self.aSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(-90))

                picname = os.path.basename(filename[0])
                
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True
        
        elif (os.path.exists(dst2) and self.pictureCard == True and self.qPictureSet == True and self.aPictureSet == False):
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if(filename[0]):
                self.aSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])

                pixmp2 = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(-90))
                picname = os.path.basename(filename[0])
                
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath

                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True

        elif (os.path.exists(dst) == False and os.path.exists(dst2) == False and self.pictureCard == True):
            print('4 '+dst)
            filename = QFileDialog.getOpenFileName(self, 'Open file', self.picPath, "Image files (*.jpg *.png)")
            if(filename[0]):
                self.aSrc = filename[0]
                copyfile(filename[0], dst)
                image = Image.open(filename[0])
                pixmp2 = QtGui.QPixmap(dst).scaled(311, 901, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
                if self.findOrientation(image) == 6:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(90))
                elif self.findOrientation(image) == 8:
                    pixmp2 = pixmp2.transformed(QtGui.QTransform().rotate(-90))
                picname = os.path.basename(filename[0])
                picpath = filename[0].replace(picname, "")
                self.picPath = picpath
                self.aPicture_2.setPixmap(pixmp2)
                self.aPictureSet = True

    def readQuestion(self, other):
        """
        converter = pyttsx3.init()
        converter.setProperty('rate', 150)
        converter.setProperty('volume', 1)

        converter.say(self.questionText.toPlainText())
        converter.runAndWait()
        """
        ################################
        """
        name = self.qName(self.questionText.toPlainText())
        tts = gTTS(self.questionText.toPlainText(), lang='fr')
        if os.path.exists(name+".mp3") == False:
            tts.save(name+".mp3")
        playsound(name+".mp3")
        """

    def enterData(self):
        """ TODO should rename the pictures if the question text or pictureCard flag has been changed (compare the file names and rename the pictures if necessary"""
        
        self.question = self.qName(self.questionText.toPlainText())
        if (self.pictureCard == False and self.question+"_front.jpg" != self.qPicName and self.qPictureSet):
            print(self.question+"_front.jpg")
            if(os.path.exists("Images/"+self.question+"_front.jpg")):
                print("exists")
                #can't add
                err = QMessageBox()
                err.setText("You already have this question, try another one!")
                err.setWindowTitle("Duplicate question")
                err.setStandardButtons(QMessageBox.Ok)
                err.exec_()
            elif os.path.exists("Images/"+self.qPicName):
                print("Rename")
                os.rename("Images/"+self.qPicName, "Images/"+self.question+"_front.jpg")
                self.qPicName = self.question+"_front.jpg"
            elif (os.path.exists("Images/"+self.qPicName) == False):
                print("qPicName doesn't exists")
                copyfile(self.qSrc, "Images/"+self.question+"_front.jpg")
                self.qPicName = self.question+"_front.jpg"

        if (self.pictureCard == False and self.question+"_back.jpg" != self.aPicName and self.aPictureSet):
            if(os.path.exists("Images/"+self.question+"_back.jpg")):
                #can't add
                err = QMessageBox()
                err.setText("You already have this question, try another one!")
                err.setWindowTitle("Duplicate question")
                err.setStandardButtons(QMessageBox.Ok)
                err.exec_()
            elif (os.path.exists("Images/"+self.aPicName)):
                os.rename("Images/"+self.qPicName, "Images/"+self.question+"_back.jpg")
                self.aPicName = self.question+"_back.jpg"
            elif (os.path.exists("Images/"+self.aPicName) == False):
                copyfile(self.aSrc, "Images/"+self.question+"_back.jpg")
                self.aPicName = self.question+"_back.jpg"
                
                # TODO if the boxPart and partSection comboBoxes are not selected (0, 0) => the card should go to the first level first deck
        if (self.boxPart.currentIndex() == 0):
            self.level = 1
        else:
            self.level = self.boxPart.currentIndex()

        if(self.partSection.currentIndex() == 0):
            self.deck = 1
        else:
            self.deck = self.partSection.currentIndex()
        
        # TODO replace nonalphanumeric characters from strings to save to the database
        if(self.pictureCard == False):
            tmp = self.questionText.toPlainText().replace("'", "''")
            self.questionField = tmp.replace('"', '""')

            tmp = self.answerText.toPlainText().replace("'", "''")
            self.answerField = tmp.replace('"', '""')

        self.insertCard()
        # TODO insert new row into the database
        
    
    def pictureCardCheck(self):
        if(self.justPicture.isChecked()):
            self.questionText.setReadOnly(True)
            self.answerText.setReadOnly(True)
            self.pictureCard = True
            self.questionText.setVisible(False)
            self.answerText.setVisible(False)
            self.question = ""+str(randint(10000, 100000000000))
            print(self.question)
            self.questionField = self.question
            self.answerField = self.question
        else:
            self.questionText.setReadOnly(False)
            self.answerText.setReadOnly(False)
            self.answerText.setVisible(True)
            self.questionText.setVisible(True)
            self.pictureCard = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Digital Memory Assistant")
        MainWindow.resize(800, 600)
        self.question = '321657484984968'
        self.questionField = ""
        self.answerField = ""
        self.pictureCard = False
        self.qPictureSet = False
        self.qSrc = ""
        self.qPicName = "none"
        self.aPicName = "none"
        self.aSrc = ""
        self.aPictureSet = False
        self.qwidget = self
        self.picPath = '/home'
        self.level = 1
        self.deck = 1
        self.questionGroup = "none"
        self.questionSubGroup = "none"
        self.questionPackage = "none"
        self.groupData = []
        self.packageData = []

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

        self.horizontalLayout_0 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_0.setObjectName("TopHorizontal")

        self.justPicture = QCheckBox("Picture-only card")
        self.justPicture.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.justPicture.setFont(font)
        self.justPicture.stateChanged.connect(self.pictureCardCheck)
        self.horizontalLayout_0.addWidget(self.justPicture)

        self.boxPart = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.boxPart.sizePolicy().hasHeightForWidth())
        self.boxPart.setSizePolicy(sizePolicy)
        self.boxPart.setObjectName("BoxPart")
        self.boxPart.currentIndexChanged.connect(self.sectionUpdate)
        self.horizontalLayout_0.addWidget(self.boxPart)

        self.partSection = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partSection.sizePolicy().hasHeightForWidth())
        self.partSection.setSizePolicy(sizePolicy)
        self.partSection.setObjectName("BoxPart")
        self.partSection.currentIndexChanged.connect(self.sectionSet)
        self.horizontalLayout_0.addWidget(self.partSection)


        self.verticalLayout_3.addLayout(self.horizontalLayout_0)

        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.qestionLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qestionLabel.sizePolicy().hasHeightForWidth())
        self.qestionLabel.setSizePolicy(sizePolicy)
        self.qestionLabel.setFont(font)
        self.qestionLabel.setObjectName("qestionLabel")
        self.qestionLabel.mouseReleaseEvent = self.readQuestion
        self.horizontalLayout.addWidget(self.qestionLabel)
        

        self.AnswerLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AnswerLabel.sizePolicy().hasHeightForWidth())
        self.AnswerLabel.setSizePolicy(sizePolicy)
        self.AnswerLabel.setMinimumSize(QtCore.QSize(375, 0))
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

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.qPicture_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setWidthForHeight(self.qPicture_2.sizePolicy().hasWidthForHeight())
        self.qPicture_2.setSizePolicy(sizePolicy)
        self.qPicture_2.setText("")
        self.image = Image.open("Images/olaf1.jpg")
        self.pixmap = QtGui.QPixmap("Images/olaf1.jpg").scaled(311, 1011, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        orientation = self.findOrientation(self.image)
        if orientation == 6:
            self.pixmap = self.pixmap.transformed(QtGui.QTransform().rotate(90))
        self.qPicture_2.setPixmap(self.pixmap)
        self.qPicture_2.setAlignment(QtCore.Qt.AlignCenter)
        self.qPicture_2.setObjectName("qPicture_2")
        self.qPicture_2.mouseReleaseEvent = self.pickQuestionImage
        self.horizontalLayout_3.addWidget(self.qPicture_2)


        self.answerText = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_3)
        self.answerText.setObjectName("answerText")
        self.horizontalLayout_2.addWidget(self.answerText)


        self.aPicture_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aPicture_2.sizePolicy().hasHeightForWidth())
        self.aPicture_2.setSizePolicy(sizePolicy)
        self.aPicture_2.setText("")
        self.pixmap2 = QtGui.QPixmap("Images/olaf2.jpg").scaled(311, 1011, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.aPicture_2.setPixmap(self.pixmap2)
        self.aPicture_2.setAlignment(QtCore.Qt.AlignCenter)
        self.aPicture_2.setObjectName("aPicture_2")
        
        self.aPicture_2.mouseReleaseEvent = self.pickAnswerImage
        
        self.horizontalLayout_3.addWidget(self.aPicture_2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
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
        self.enter_2.clicked.connect(self.enterData)
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

        self.thesaurus.currentIndexChanged.connect(self.thesaurusSelected)
        self.packages.currentIndexChanged.connect(self.packageSelected)
        self.thesaurusInit()
        self.packageInit()
        self.boxPartInit()
        self.partSectionInit()
        self.dbInit()

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
