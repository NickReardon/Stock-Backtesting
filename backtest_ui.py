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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHeaderView,
    QSizePolicy, QSpacerItem, QTableView, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_Backtest(object):
    def setupUi(self, Backtest):
        if not Backtest.objectName():
            Backtest.setObjectName(u"Backtest")
        Backtest.resize(1183, 624)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Backtest.sizePolicy().hasHeightForWidth())
        Backtest.setSizePolicy(sizePolicy)
        self.gridLayoutWidget = QWidget(Backtest)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 0, 1151, 621))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.backtestPlot = QWidget(self.gridLayoutWidget)
        self.backtestPlot.setObjectName(u"backtestPlot")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.backtestPlot.sizePolicy().hasHeightForWidth())
        self.backtestPlot.setSizePolicy(sizePolicy1)
        self.backtestPlot.setMinimumSize(QSize(500, 500))

        self.gridLayout_3.addWidget(self.backtestPlot, 0, 1, 1, 1)

        self.backtestTable = QTableWidget(self.gridLayoutWidget)
        self.backtestTable.setObjectName(u"backtestTable")
        sizePolicy1.setHeightForWidth(self.backtestTable.sizePolicy().hasHeightForWidth())
        self.backtestTable.setSizePolicy(sizePolicy1)

        self.gridLayout_3.addWidget(self.backtestTable, 0, 0, 4, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)

        self.gridLayout_3.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.resultsTable = QTableView(self.gridLayoutWidget)
        self.resultsTable.setObjectName(u"resultsTable")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.resultsTable.sizePolicy().hasHeightForWidth())
        self.resultsTable.setSizePolicy(sizePolicy2)
        self.resultsTable.setMinimumSize(QSize(0, 20))
        self.resultsTable.setMaximumSize(QSize(577, 80))
        self.resultsTable.setBaseSize(QSize(200, 40))

        self.gridLayout_3.addWidget(self.resultsTable, 3, 1, 1, 1)


        self.retranslateUi(Backtest)

        QMetaObject.connectSlotsByName(Backtest)
    # setupUi

    def retranslateUi(self, Backtest):
        Backtest.setWindowTitle(QCoreApplication.translate("Backtest", u"Dialog", None))
    # retranslateUi

