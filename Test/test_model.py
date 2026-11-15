import os
import sys
import unittest
from decimal import Decimal
from unittest import mock

import numpy as np

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import StrategyBase
from matplotlib.figure import Figure
import strategies.sma_crossover_strategy as sma


class _Strategy(StrategyBase):
    def execute_strategy(self, *args):
        pass

    def plot_strategy(self, *args):
        pass


class TestGainLoss(unittest.TestCase):
    def test_sell_gain_loss_is_against_entry_price(self):
        data = pd.DataFrame({'Close': [10.0, 12.0, 15.0]},
                            index=pd.date_range('2024-01-01', periods=3))
        s = _Strategy()
        log, tx = [], []
        balance, shares = s.buy(data, 0, 'X', Decimal(100), Decimal(0), log, tx)
        balance, shares = s.sell(data, 2, 'X', balance, shares, log, tx)
        # 10 shares bought at 10, sold at 15 -> +50 (not +30 vs previous close)
        self.assertEqual(log[-1]['Gain/Loss'], '50.00')
        self.assertEqual(balance, Decimal(150))


class TestStrategyInMemory(unittest.TestCase):
    def test_sma_returns_result_without_writing_files(self):
        steps = np.arange(300)
        close = 100 + 10 * np.sin(steps / 15)
        data = pd.DataFrame({'Close': close}, index=pd.bdate_range('2021-01-01', periods=300, name='Date'))
        before = set(os.listdir('.'))

        with mock.patch.object(sma.SMACrossoverStrategy, 'read_and_prepare_data', return_value=data):
            result = sma.execute_strategy('X')
        sma.plot_strategy(Figure(), data, result, 'X')

        self.assertGreater(len(result.trade_log), 0)
        self.assertEqual(list(result.transactions['Action'].unique()), ['Buy', 'Sell'])
        self.assertEqual(list(result.indicators.columns), ['Short_MA', 'Long_MA'])
        self.assertEqual(f"{result.summary['Balance']:.2f}", result.trade_log['Balance'].iloc[-1])
        self.assertEqual(set(os.listdir('.')) - before, set())


if __name__ == '__main__':
    unittest.main()
