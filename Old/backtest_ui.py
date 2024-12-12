# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backtest.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QDialog,
    QGridLayout, QHeaderView, QScrollArea, QSizePolicy,
    QTableView, QTableWidget, QTableWidgetItem, QWidget)

class Ui_Backtest(object):
    def setupUi(self, Backtest):
        if not Backtest.objectName():
            Backtest.setObjectName(u"Backtest")
        Backtest.resize(1069, 659)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Backtest.sizePolicy().hasHeightForWidth())
        Backtest.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(Backtest)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(Backtest)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1035, 1012))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.backtestPlot = QWidget(self.scrollAreaWidgetContents)
        self.backtestPlot.setObjectName(u"backtestPlot")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.backtestPlot.sizePolicy().hasHeightForWidth())
        self.backtestPlot.setSizePolicy(sizePolicy1)
        self.backtestPlot.setMinimumSize(QSize(800, 600))

        self.gridLayout_5.addWidget(self.backtestPlot, 2, 0, 1, 1)

        self.backtestTable = QTableWidget(self.scrollAreaWidgetContents)
        self.backtestTable.setObjectName(u"backtestTable")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.backtestTable.sizePolicy().hasHeightForWidth())
        self.backtestTable.setSizePolicy(sizePolicy2)
        self.backtestTable.setMinimumSize(QSize(0, 300))
        self.backtestTable.setMaximumSize(QSize(16777215, 500))
        self.backtestTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.backtestTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.backtestTable.setAlternatingRowColors(True)

        self.gridLayout_5.addWidget(self.backtestTable, 0, 0, 1, 1)

        self.resultsTable = QTableView(self.scrollAreaWidgetContents)
        self.resultsTable.setObjectName(u"resultsTable")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.resultsTable.sizePolicy().hasHeightForWidth())
        self.resultsTable.setSizePolicy(sizePolicy3)
        self.resultsTable.setMinimumSize(QSize(0, 80))
        self.resultsTable.setBaseSize(QSize(200, 80))
        self.resultsTable.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.resultsTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.gridLayout_5.addWidget(self.resultsTable, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_5, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(Backtest)

        QMetaObject.connectSlotsByName(Backtest)
    # setupUi

    def retranslateUi(self, Backtest):
        Backtest.setWindowTitle(QCoreApplication.translate("Backtest", u"Dialog", None))
    # retranslateUi

