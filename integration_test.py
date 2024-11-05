import sys
import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QDate, QEventLoop, QTimer
from mainwindow import MainWindow

class TestIntegration(unittest.TestCase):
    def setUp(self):
        if QApplication.instance() is None:
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        self.window = MainWindow()
        self.window.show()
        self.window.initialize_ui()

    def tearDown(self):
        self.window.close()
        self.app.quit()
        self.app = None

    def test_select_etf_from_combobox(self):
        # Simulate opening the comboBox
        QTest.mouseClick(self.window.ui.ETF_Dropdown, Qt.LeftButton)
        print("ComboBox opened")

        QTest.qWait(1000)  # Wait for the comboBox to open

        # Simulate selecting an item from the comboBox
        QTest.keyClick(self.window.ui.ETF_Dropdown, Qt.Key_Down)

        QTest.qWait(1000)  # Wait for the comboBox to select the item

        QTest.keyClick(self.window.ui.ETF_Dropdown, Qt.Key_Enter)
        print("ComboBox item selected")

        QTest.qWait(1000)  # Wait for the comboBox to close

        # Explicitly close the comboBox
        self.window.ui.ETF_Dropdown.hidePopup()
        print("ComboBox closed")

        QTest.qWait(1000)  # Wait for the comboBox to close

        # Verify the selected item
        selected_index = self.window.ui.ETF_Dropdown.currentIndex()
        self.assertNotEqual(selected_index, -1, "No item selected in the comboBox")
        print(f"Selected index: {selected_index}")

    def test_download_button(self):
        # Simulate selecting a date range
        self.window.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.window.ui.endDateEdit.setDate(QDate.currentDate())
                                           
        # Simulate selecting a symbol from the dropdown
        self.window.ui.ETF_Dropdown.setCurrentIndex(0)  # Assuming the first item is valid

        # Add debug print to check if the button is being clicked
        print("Clicking the download button")
        
        # Simulate clicking the download button
        QTest.mouseClick(self.window.ui.downloadButton, Qt.LeftButton)
        print("Download button clicked")

        # Create an event loop to wait for the thread to finish
        loop = QEventLoop()
        self.window.download_thread.finished.connect(loop.quit)

        # Wait for the download thread to finish
        loop.exec_()

        # Polling loop to check for download completion
        timeout = 1500  # 5 seconds
        interval = 100  # 100 milliseconds
        elapsed = 0

        while elapsed < timeout:
            if self.window.ui.progressBar.maximum() == 100:
                break
            QTest.qWait(interval)
            elapsed += interval
            print("Elapsed time:", elapsed)

        print("_+____Elapsed time:", elapsed)

        # Check if the progress bar is set to "Complete"
        self.assertEqual(self.window.ui.progressBar.maximum(), 1, "Download did not complete within the timeout period")

    def test_backtest(self):

        self.window.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.window.ui.endDateEdit.setDate(QDate.currentDate())

        # Simulate selecting a symbol from the dropdown
        self.window.ui.ETF_Dropdown.setCurrentIndex(0)  # Assuming the first item is valid

        QTest.qWait(1000)  # Wait for the comboBox to update

        # Simulate selecting a strategy from the strategyComboBox
        self.window.ui.strategyComboBox.setCurrentIndex(0)  # Assuming the first item is valid

        QTest.qWait(1000)  # Wait for the comboBox to update

        # Add debug print to check if the button is being clicked
        print("Clicking the backtest button")
        
        # Simulate clicking the backtest button
        QTest.mouseClick(self.window.ui.backtestButton, Qt.LeftButton)
        print("Backtest button clicked")

        QTest.qWait(2000)  # Wait for the backtest window to open

        # Verify that the backtest window is opened
        self.assertIsNotNone(self.window.backtest_window, "Backtest window was not opened")
        self.assertTrue(self.window.backtest_window.isVisible(), "Backtest window is not visible")

        # Verify that the backtest results are displayed
        # (You can add more specific checks here based on your application's behavior)

    def test_download_and_update_plot(self):
        # Simulate selecting a date range
        self.window.ui.startDateEdit.setDate(QDate(2021, 1, 1))
        self.window.ui.endDateEdit.setDate(QDate.currentDate())

        # Simulate selecting a symbol from the dropdown
        self.window.ui.ETF_Dropdown.setCurrentIndex(0)  # Assuming the first item is valid

        # Add debug print to check if the button is being clicked
        print("Clicking the download button")
        
        # Simulate clicking the download button
        QTest.mouseClick(self.window.ui.downloadButton, Qt.LeftButton)
        print("Download button clicked")

        # Create an event loop to wait for the thread to finish
        loop = QEventLoop()
        self.window.download_thread.finished.connect(loop.quit)

        # Wait for the download thread to finish
        loop.exec_()

        # Polling loop to check for download completion
        timeout = 1500  # 5 seconds
        interval = 100  # 100 milliseconds
        elapsed = 0

        while elapsed < timeout:
            if self.window.ui.progressBar.maximum() == 100:
                break
            QTest.qWait(interval)
            elapsed += interval
            print("Elapsed time:", elapsed)

        print("_+____Elapsed time:", elapsed)

        # Check if the progress bar is set to "Complete"
        self.assertEqual(self.window.ui.progressBar.maximum(), 1, "Download did not complete within the timeout period")

        # Simulate selecting a different symbol from the dropdown
        self.window.ui.ETF_Dropdown.setCurrentIndex(1)  # Assuming the second item is valid
        QTest.qWait(1000)  # Wait for the comboBox to update

        # Simulate selecting a different date range
        self.window.ui.startDateEdit.setDate(QDate(2022, 1, 1))
        self.window.ui.endDateEdit.setDate(QDate(2022, 12, 31))
        QTest.qWait(1000)  # Wait for the date range to update

        # Verify that the plot is updated
        # (You can add more specific checks here based on your application's behavior)

if __name__ == '__main__':
    # Create a TestLoader instance
    loader = unittest.TestLoader()

    # Create a test suite and add tests in the desired order
    suite = unittest.TestSuite()
    suite.addTest(TestIntegration('test_select_etf_from_combobox'))
    suite.addTest(TestIntegration('test_download_button'))
    suite.addTest(TestIntegration('test_backtest'))
    suite.addTest(TestIntegration('test_download_and_update_plot'))

    # Run the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
