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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox, QComboBox, QDateEdit,
    QDialog, QGridLayout, QLabel, QMainWindow, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem, QTableView, QTableWidget, QTableWidgetItem, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.startDateEdit = QDateEdit(self.centralwidget)
        self.startDateEdit.setObjectName(u"startDateEdit")

        self.gridLayout.addWidget(self.startDateEdit, 1, 3, 1, 1)

        self.endDateEdit = QDateEdit(self.centralwidget)
        self.endDateEdit.setObjectName(u"endDateEdit")

        self.gridLayout.addWidget(self.endDateEdit, 1, 4, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.endDateLabel = QLabel(self.centralwidget)
        self.endDateLabel.setObjectName(u"endDateLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endDateLabel.sizePolicy().hasHeightForWidth())
        self.endDateLabel.setSizePolicy(sizePolicy)
        self.endDateLabel.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.endDateLabel, 0, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(30, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.symbolLabel = QLabel(self.centralwidget)
        self.symbolLabel.setObjectName(u"symbolLabel")
        sizePolicy.setHeightForWidth(self.symbolLabel.sizePolicy().hasHeightForWidth())
        self.symbolLabel.setSizePolicy(sizePolicy)
        self.symbolLabel.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.symbolLabel, 0, 1, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_4, 5, 8, 1, 1)

        self.startDateLabel = QLabel(self.centralwidget)
        self.startDateLabel.setObjectName(u"startDateLabel")
        sizePolicy.setHeightForWidth(self.startDateLabel.sizePolicy().hasHeightForWidth())
        self.startDateLabel.setSizePolicy(sizePolicy)
        self.startDateLabel.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addWidget(self.startDateLabel, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.downloadButton = QPushButton(self.centralwidget)
        self.downloadButton.setObjectName(u"downloadButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.downloadButton.sizePolicy().hasHeightForWidth())
        self.downloadButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.downloadButton, 1, 6, 1, 1)

        self.ETF_Dropdown = QComboBox(self.centralwidget)
        self.ETF_Dropdown.addItem("")
        self.ETF_Dropdown.addItem("")
        self.ETF_Dropdown.setObjectName(u"ETF_Dropdown")

        self.gridLayout.addWidget(self.ETF_Dropdown, 1, 1, 1, 1)

        self.yAxisCheckbox = QCheckBox(self.centralwidget)
        self.yAxisCheckbox.setObjectName(u"yAxisCheckbox")
        self.yAxisCheckbox.setAutoFillBackground(True)
        self.yAxisCheckbox.setChecked(True)

        self.gridLayout.addWidget(self.yAxisCheckbox, 5, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(80, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 1, 5, 1, 1)

        self.backtestButton = QPushButton(self.centralwidget)
        self.backtestButton.setObjectName(u"backtestButton")

        self.gridLayout.addWidget(self.backtestButton, 5, 7, 1, 1)

        self.strategyComboBox = QComboBox(self.centralwidget)
        self.strategyComboBox.setObjectName(u"strategyComboBox")

        self.gridLayout.addWidget(self.strategyComboBox, 5, 6, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 5, 2, 1, 4)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_5, 0, 0, 1, 1)

        self.plotWidget = QWidget(self.centralwidget)
        self.plotWidget.setObjectName(u"plotWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.plotWidget, 2, 0, 2, 9)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy3)
        self.progressBar.setMinimumSize(QSize(0, 0))
        self.progressBar.setAutoFillBackground(True)
        self.progressBar.setValue(24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.progressBar, 1, 7, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 8, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 8, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 0, 7, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(80, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 0, 5, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 0, 6, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.endDateLabel.setText(QCoreApplication.translate("MainWindow", u"End Date", None))
        self.symbolLabel.setText(QCoreApplication.translate("MainWindow", u"Symbol", None))
        self.startDateLabel.setText(QCoreApplication.translate("MainWindow", u"Start Date", None))
        self.downloadButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.ETF_Dropdown.setItemText(0, QCoreApplication.translate("MainWindow", u"FNGU", None))
        self.ETF_Dropdown.setItemText(1, QCoreApplication.translate("MainWindow", u"FNGD", None))

        self.yAxisCheckbox.setText(QCoreApplication.translate("MainWindow", u"Maintain Y-axis", None))
        self.backtestButton.setText(QCoreApplication.translate("MainWindow", u"Backtest", None))
    # retranslateUi




# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'backtest.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


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

