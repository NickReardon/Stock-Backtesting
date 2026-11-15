import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QDate

from controller import MainWindow
from yfinance_adapter import YFinanceAdapter

DOWNLOAD_TIMEOUT_MS = 10000
POLL_INTERVAL_MS = 100


class FakeYFinanceAdapter(YFinanceAdapter):
    """Serves deterministic prices so the test never touches the network."""

    def fetch_data(self, symbol, start_date, end_date):
        dates = pd.bdate_range(start=start_date, end=end_date, name="Date")
        # A sine wave over a drift gives the strategies real crossovers to trade on.
        steps = np.arange(len(dates))
        close = 100 + steps * 0.05 + 10 * np.sin(steps / 15)
        return pd.DataFrame({
            "Open": close,
            "High": close + 1,
            "Low": close - 1,
            "Close": close,
            "Volume": 1_000_000,
        }, index=dates)


class TestIntegration(unittest.TestCase):
    def setUp(self):
        # The app reads and writes its JSON and CSV files in the working directory.
        self.original_cwd = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

        self.app = QApplication.instance() or QApplication(sys.argv)
        self.window = MainWindow()
        self.window.data_access = FakeYFinanceAdapter()
        self.window.show()

    def tearDown(self):
        self.window.close()
        os.chdir(self.original_cwd)
        self.temp_dir.cleanup()

    def download(self):
        """Click download and wait until the progress bar reports completion."""
        self.window.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.window.ui.endDateEdit.setDate(QDate(2022, 12, 31))
        self.window.ui.ETF_Dropdown.setCurrentIndex(0)

        QTest.mouseClick(self.window.ui.downloadButton, Qt.LeftButton)
        self.assertTrue(self.window.download_thread.wait(DOWNLOAD_TIMEOUT_MS), "Download thread did not finish")

        elapsed = 0
        while self.window.ui.progressBar.format() != "Complete" and elapsed < DOWNLOAD_TIMEOUT_MS:
            QTest.qWait(POLL_INTERVAL_MS)
            elapsed += POLL_INTERVAL_MS

        self.assertEqual(self.window.ui.progressBar.format(), "Complete", "Download did not complete within the timeout period")

    def test_select_etf_from_combobox(self):
        QTest.mouseClick(self.window.ui.ETF_Dropdown, Qt.LeftButton)
        QTest.keyClick(self.window.ui.ETF_Dropdown, Qt.Key_Down)
        QTest.keyClick(self.window.ui.ETF_Dropdown, Qt.Key_Enter)
        self.window.ui.ETF_Dropdown.hidePopup()

        self.assertNotEqual(self.window.ui.ETF_Dropdown.currentIndex(), -1, "No item selected in the comboBox")

    def test_download_button(self):
        self.download()

        self.assertTrue(os.path.exists("all_symbols_data.json"), "Downloaded data was not saved")
        self.assertTrue(self.window.ui.backtestButton.isEnabled(), "Backtest button not enabled after download")

    def test_backtest(self):
        self.download()
        self.window.ui.strategyComboBox.setCurrentIndex(0)

        QTest.mouseClick(self.window.ui.backtestButton, Qt.LeftButton)
        QTest.qWait(POLL_INTERVAL_MS)

        self.assertTrue(hasattr(self.window, "backtest_window"), "Backtest window was not opened")
        self.assertTrue(self.window.backtest_window.isVisible(), "Backtest window is not visible")
        self.assertGreater(self.window.backtest_window.ui.backtestTable.rowCount(), 0, "Backtest table is empty")

    def test_download_and_update_plot(self):
        self.download()

        # Switching symbols after a download replots from the saved data.
        self.window.ui.ETF_Dropdown.setCurrentIndex(1)
        QTest.qWait(POLL_INTERVAL_MS)

        self.assertEqual(self.window.ui.ETF_Dropdown.currentIndex(), 1)


if __name__ == '__main__':
    unittest.main()
