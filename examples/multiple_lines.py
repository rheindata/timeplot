"""
This example demonstrates how to plot multiple lines and change some of the default settings.
"""

import time
from collections import deque
from datetime import datetime

import numpy as np

from timeplot import timeplot


class SimpleTimeSeries:
    def __init__(self):
        self.t = datetime.now()
        self.y = 0.0
        self.y_hist = deque()
        self.maxlen = 60

    def calculate_indicators(self, t, y):
        """ Calculates 1-minute SMA and Bollinger bands """
        self.y_hist.append(y)
        if len(self.y_hist) < self.maxlen:
            # Do not plot SMA and Bollinger bands in the first minute
            return t, y, np.nan, np.nan, np.nan
        y_sma = np.mean(self.y_hist)
        sd = np.std(self.y_hist)
        y_up = y_sma + 2 * sd
        y_down = y_sma - 2 * sd
        return t, y, y_sma, y_up, y_down

    def get_tick(self):
        """ Very simple function that waits for a random time and generates a random variable.
         Replace this with a call to your favorite API or file to plot something interesting. """
        time.sleep(np.random.rand())
        self.y += np.random.randn()
        return self.calculate_indicators(datetime.now(), self.y)


lcolors = ['darkblue', 'orange', 'lightblue', 'lightblue']
lwidths = [1.0, 0.8, 0.4, 0.4]
llabels = ['SimpleTimeSeries', 'Moving average (1 minute)',
           'Moving average +/- 2 std. dev. (1 minute)', '']
title = 'SimpleTimeSeries'

ts = SimpleTimeSeries()
timeplot.timeplot(ts.get_tick, lcolors=lcolors, lwidths=lwidths, llabels=llabels, title=title)
