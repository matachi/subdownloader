# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'expiration.ui'
#
# Created: Fri Mar 13 21:05:00 2010
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExpirationDialog(object):
    def setupUi(self, ExpirationDialog):
        ExpirationDialog.setObjectName("ExpirationDialog")
        ExpirationDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ExpirationDialog.resize(483, 295)
        ExpirationDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(ExpirationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_expiration = QtGui.QLabel(ExpirationDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_expiration.setFont(font)
        self.label_expiration.setObjectName("label_expiration")
        self.verticalLayout.addWidget(self.label_expiration)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonRegister = QtGui.QPushButton(ExpirationDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.buttonRegister.setFont(font)
        self.buttonRegister.setObjectName("buttonRegister")
        self.horizontalLayout_2.addWidget(self.buttonRegister)
        spacerItem = QtGui.QSpacerItem(188, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_5 = QtGui.QLabel(ExpirationDialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(ExpirationDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.activation_email = QtGui.QLineEdit(ExpirationDialog)
        self.activation_email.setObjectName("activation_email")
        self.gridLayout.addWidget(self.activation_email, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(ExpirationDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.activation_fullname = QtGui.QLineEdit(ExpirationDialog)
        self.activation_fullname.setObjectName("activation_fullname")
        self.gridLayout.addWidget(self.activation_fullname, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(ExpirationDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.activation_licensekey = QtGui.QLineEdit(ExpirationDialog)
        self.activation_licensekey.setObjectName("activation_licensekey")
        self.gridLayout.addWidget(self.activation_licensekey, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtGui.QSpacerItem(238, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonCancel = QtGui.QPushButton(ExpirationDialog)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout.addWidget(self.buttonCancel)
        self.buttonActivate = QtGui.QPushButton(ExpirationDialog)
        self.buttonActivate.setObjectName("buttonActivate")
        self.horizontalLayout.addWidget(self.buttonActivate)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ExpirationDialog)
        QtCore.QMetaObject.connectSlotsByName(ExpirationDialog)

    def retranslateUi(self, ExpirationDialog):
        ExpirationDialog.setWindowTitle(QtGui.QApplication.translate("ExpirationDialog", "Program has expired", None, QtGui.QApplication.UnicodeUTF8))
        self.label_expiration.setText(QtGui.QApplication.translate("ExpirationDialog", "The program has expired after %d days of usage.", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRegister.setText(QtGui.QApplication.translate("ExpirationDialog", "Register Online...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ExpirationDialog", "After registering, you will receive a license key via email.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ExpirationDialog", "Email:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ExpirationDialog", "Full Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ExpirationDialog", "License key:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCancel.setText(QtGui.QApplication.translate("ExpirationDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonActivate.setText(QtGui.QApplication.translate("ExpirationDialog", "Activate", None, QtGui.QApplication.UnicodeUTF8))

