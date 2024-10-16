# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ETF_Dropdown = QComboBox(self.centralwidget)
        self.ETF_Dropdown.addItem("")
        self.ETF_Dropdown.addItem("")
        self.ETF_Dropdown.setObjectName(u"ETF_Dropdown")

        self.gridLayout.addWidget(self.ETF_Dropdown, 0, 0, 1, 1)

        self.startDateEdit = QDateEdit(self.centralwidget)
        self.startDateEdit.setObjectName(u"startDateEdit")

        self.gridLayout.addWidget(self.startDateEdit, 0, 1, 1, 1)

        self.endDateEdit = QDateEdit(self.centralwidget)
        self.endDateEdit.setObjectName(u"endDateEdit")

        self.gridLayout.addWidget(self.endDateEdit, 0, 2, 1, 1)

        self.downloadButton = QPushButton(self.centralwidget)
        self.downloadButton.setObjectName(u"downloadButton")

        self.gridLayout.addWidget(self.downloadButton, 0, 3, 1, 1)

        self.plotWidget = QWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.gridLayout.addWidget(self.plotWidget, 1, 0, 1, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ETF_Dropdown.setItemText(0, QCoreApplication.translate("MainWindow", u"FNGU", None))
        self.ETF_Dropdown.setItemText(1, QCoreApplication.translate("MainWindow", u"FNGD", None))

        self.downloadButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
    # retranslateUi

