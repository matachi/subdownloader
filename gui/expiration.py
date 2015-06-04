from builtins import str
#!/usr/bin/env python
# Copyright (c) 2010 SubDownloader Developers - See COPYING - GPLv3

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, SIGNAL, QObject, QCoreApplication, \
                         QSettings, QVariant, QSize, QEventLoop, QString, \
                         QBuffer, QIODevice, QModelIndex,QDir
from PyQt4.QtGui import QPixmap, QErrorMessage, QLineEdit, \
                        QMessageBox, QFileDialog, QIcon, QDialog, QInputDialog,QDirModel, QItemSelectionModel
from PyQt4.Qt import qDebug, qFatal, qWarning, qCritical

from gui.expiration_ui import Ui_ExpirationDialog
import logging
import webbrowser
from modules import APP_TITLE, APP_VERSION
log = logging.getLogger("subdownloader.gui.expiration")

from datetime import date , timedelta
import time

DAYS_TRIAL = 30
def GetFirstRunTime():
    settings = QSettings()
    firstRunTime = settings.value("mainwindow/size2", QVariant())
    if firstRunTime != QVariant():
        return firstRunTime.toDouble()[0]
    else:
            now = time.time()
            settings.setValue("mainwindow/size2", QVariant(now))
            return now

def calculateDaysLeft(server_time):
        log.debug('Calculating the days left for expiration')
        server_date = date.fromtimestamp(server_time)
        first_run_time = GetFirstRunTime()

        first_run_date = date.fromtimestamp(first_run_time)
        #first_run_date  -= timedelta(days=21)
        daysLeft =  first_run_date + timedelta(days=DAYS_TRIAL) - server_date

        #print "Days Left = %d" % daysLeft.days
        if daysLeft.days <= 0:
            return 0
        return daysLeft.days

class expirationDialog(QtGui.QDialog):
    def __init__(self, parent, daysLeft):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ExpirationDialog()
        self.ui.setupUi(self)
        self._main  = parent
        self.daysLeft = daysLeft
        settings = QSettings()
        QObject.connect(self.ui.buttonCancel, SIGNAL("clicked(bool)"), self.onButtonCancel)
        QObject.connect(self.ui.buttonRegister, SIGNAL("clicked(bool)"), self.onButtonRegister)
        QObject.connect(self.ui.buttonActivate, SIGNAL("clicked(bool)"), self.onButtonActivate)
        QObject.connect(self.ui.activation_email, SIGNAL("textChanged()"), self.onFieldsChanged)
        QObject.connect(self.ui.activation_fullname, SIGNAL("textChanged()"), self.onFieldsChanged)
        QObject.connect(self.ui.activation_licensekey, SIGNAL("textChanged()"), self.onFieldsChanged)

        if daysLeft:
            self.ui.label_expiration.setText(_('The program will expire in %d days.') % daysLeft)
            self.setWindowTitle(_('Activate Program'))
        else:
            self.ui.label_expiration.setText(_('The program has expired after %d days of usage.') % DAYS_TRIAL)
            self.ui.buttonCancel.hide()

    def onButtonCancel(self):
        self.reject()

    def onButtonRegister(self):
        webbrowser.open( "http://www.subdownloader.net/buylicense.html", new=2, autoraise=1)

    def onFieldsChanged(self):
        if len(self.ui.activation_email.text()) and len(self.ui.activation_fullname.text()) and len(self.ui.activation_licensekey.text()):
            self.ui.buttonActivate.setEnabled(True)
        else:
            self.ui.buttonActivate.setEnabled(False)

    def onButtonActivate(self):
        email = str(self.ui.activation_email.text())
        fullname = str(self.ui.activation_fullname.text())
        licensekey  = str(self.ui.activation_licensekey.text())
        if not email or not fullname or not licensekey:
            QMessageBox.about(self,_("Error"),_("Some fields are empty.. please fill them."))
            return
        self.setCursor(Qt.BusyCursor)
        result = self._main.SDDBServer.xmlrpc_server.CheckSoftwareLicense(APP_VERSION, email, fullname, licensekey, True)
        self.setCursor(Qt.ArrowCursor)
        if result == "REGISTERED":
            settings = QSettings()
            settings.setValue('activation/email', QVariant(email))
            settings.setValue('activation/licensekey', QVariant(licensekey))
            settings.setValue('activation/fullname', QVariant(fullname))
            QMessageBox.about(self,_("Info"),"Program Registered Successfully. Thank you")
            self._main.setTitleBarText(_('Program Registered'))
            self._main.menu_Help.removeAction(self._main.action_ActivateProgram)
            self.accept()
        elif result == "DISABLED_TOO_MANY":
            QMessageBox.about(self,_("Error"),"This license has been disabled because of too many suspicious registrations in a short period of time.\nIf you think this is a mistake contact us at licenses@subdownloader.net")
        else:
            QMessageBox.about(self,_("Error"),"Invalid Registration.\nIf you have paid for the license, you should receive soon an email from licenses@subdownloader.net with your License Key")

