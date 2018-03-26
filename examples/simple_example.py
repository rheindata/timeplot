"""
This example demonstrates how to plot a single line using the default settings.
"""

from datetime import datetime, timedelta
import numpy as np

from timeplot import timeplot


class MyTimeSeries:
    """ A very simple time series.
     Calling get_tick() returns a single (time, value) tuple. """
    def __init__(self):
        self.t = datetime.fromtimestamp(1521482712)
        self.i = 0

    def get_tick(self):
        self.t += timedelta(seconds=1)
        self.i += 1 / 10
        return self.t, np.sin(self.i)


ts = MyTimeSeries()
timeplot.timeplot(ts.get_tick, interval=40, update_style='cont')
# timeplot.timeplot(ts.get_tick, interval=40, update_style='jump')
