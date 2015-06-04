# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'imdb.ui'
#
# Created: Fri Mar 13 21:04:58 2010
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IMDBSearchDialog(object):
    def setupUi(self, IMDBSearchDialog):
        IMDBSearchDialog.setObjectName("IMDBSearchDialog")
        IMDBSearchDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        IMDBSearchDialog.resize(522, 406)
        IMDBSearchDialog.setModal(True)
        self.vboxlayout = QtGui.QVBoxLayout(IMDBSearchDialog)

        self.label = QtGui.QLabel(IMDBSearchDialog)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.hboxlayout = QtGui.QHBoxLayout()

        self.movieSearch = QtGui.QLineEdit(IMDBSearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movieSearch.sizePolicy().hasHeightForWidth())
        self.movieSearch.setSizePolicy(sizePolicy)
        self.movieSearch.setObjectName("movieSearch")
        self.hboxlayout.addWidget(self.movieSearch)
        self.searchMovieButton = QtGui.QPushButton(IMDBSearchDialog)
        self.searchMovieButton.setObjectName("searchMovieButton")
        self.hboxlayout.addWidget(self.searchMovieButton)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.searchResultsView = ImdbListView(IMDBSearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchResultsView.sizePolicy().hasHeightForWidth())
        self.searchResultsView.setSizePolicy(sizePolicy)
        self.searchResultsView.setAcceptDrops(True)
        self.searchResultsView.setDragEnabled(True)
        self.searchResultsView.setDragDropMode(QtGui.QAbstractItemView.DropOnly)
        self.searchResultsView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.searchResultsView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.searchResultsView.setGridStyle(QtCore.Qt.DotLine)
        self.searchResultsView.setObjectName("searchResultsView")
        self.vboxlayout.addWidget(self.searchResultsView)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.movieInfoButton = QtGui.QPushButton(IMDBSearchDialog)
        self.movieInfoButton.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.movieInfoButton.setIcon(icon)
        self.movieInfoButton.setIconSize(QtCore.QSize(32, 16))
        self.movieInfoButton.setObjectName("movieInfoButton")
        self.hboxlayout1.addWidget(self.movieInfoButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(IMDBSearchDialog)
        self.okButton.setEnabled(False)
        self.okButton.setObjectName("okButton")
        self.hboxlayout1.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(IMDBSearchDialog)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout1.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(IMDBSearchDialog)
        QtCore.QMetaObject.connectSlotsByName(IMDBSearchDialog)

    def retranslateUi(self, IMDBSearchDialog):
        IMDBSearchDialog.setWindowTitle(_("IMDB search dialog:"))
        self.label.setText(_("Enter the Movie Title or IMDB id:"))
        self.searchMovieButton.setText(_("Search Movie"))
        self.movieInfoButton.setText(_("Movie Info"))
        self.okButton.setText(_("OK"))
        self.cancelButton.setText(_("Cancel"))

from imdblistview import ImdbListView
import images_rc

