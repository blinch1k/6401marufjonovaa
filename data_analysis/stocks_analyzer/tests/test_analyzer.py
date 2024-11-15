'''
Модуль тестирования работы класса Analyzer
'''

import unittest
import math
from datetime import datetime
import pandas as pd

from stocks_analyzer.stocks_analyzer.analyzer import Analyzer 

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        data = {"BTC": [1, -1, 1, 2, 1, 2, 1]}
        
        indexes = [datetime(2024, 10, 15), datetime(2024, 10, 16), datetime(2024, 10, 17),
                    datetime(2024, 10, 18), datetime(2024, 10, 19), datetime(2024, 10, 20),
                    datetime(2024, 10, 21)]
        
        table = pd.DataFrame(data=data, index= indexes)
        self.analyzer = Analyzer(table)

    def test_SMA(self):
        avgs = self.analyzer.SMA(['BTC'], 1)
        self.assertTrue([avgs[0][2], avgs[1][1]] == [0, 2])

    def test_DIF(self):
        diffs = self.analyzer.diff(['BTC'], 0)
        self.assertTrue((math.fabs(diffs[0][1] - -2.31481481e-05) < 1e-4) and (math.fabs(diffs[1][0] - 0) < 1e-4))

    def test_ACF(self):
        acf = self.analyzer.ACF(['BTC'], 0)
        self.assertTrue((math.fabs(acf[0][2] - (-0.25)) < 1e-4) and (math.fabs(acf[1][1] - (-0.06565322)) < 1e-4))
    
    def test_extreme_points(self):
        extremes = self.analyzer.extreme_points(['BTC'], 0)
        self.assertTrue((extremes['max'][0][0] == 3) and (extremes['min'][1][0] == 2))

    def test_max_points(self):
        maxs = self.analyzer.max_points(['BTC'], 0)
        self.assertTrue((maxs[0][0] == 3) and (maxs[1][0] == 4))
        
    
    def test_min_points(self):
        mins = self.analyzer.min_points(['BTC'], 0)
        self.assertTrue((mins[0][0] == 1) and (mins[1][0] == 2))

if __name__ == "__main__":
    unittest.main()