import os
import sys
import unittest
from decimal import Decimal

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import StrategyBase


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


if __name__ == '__main__':
    unittest.main()
