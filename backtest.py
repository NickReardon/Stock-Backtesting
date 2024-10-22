from PySide6.QtWidgets import QDialog
from backtest_ui import Ui_Backtest

class BacktestWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Backtest()
        self.ui.setupUi(self)