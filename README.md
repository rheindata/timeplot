# timeplot

A Python module for fancy realtime plots.
This was built with financial time series in mind, but hopefully also serves other purposes.
Built on Matplotlib's `FuncAnimation`.

## Getting started
The single required argument for `timeplot` is a function `f` that returns a tuple `(t, y1, ..., yn)`.
Here, `t` is a datetime timestamp and `y1` through `yn` are numerical values. 
This is also the place to plug in your own data stream, e.g. by polling ticks from an API.

A very simple example:
```python
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
timeplot(ts.get_tick, interval=40, update_style='cont')
# Also check out:
# timeplot(ts.get_tick, interval=40, update_style='jump')
```
<p align="center">
<a href="url"><img src="https://github.com/rheindata/timeplot/blob/master/examples/simple_example.jpg" width="600" ></a>
</p>

See [`examples/multiple_lines.py`](/examples/multiple_lines.py) for a slightly more sophisticated example.

## Changing the look
There are a few additional parameters that can easily be changed to customize the plot layout; check out the inline information on the variables `padding`, `colortheme`, `time_format` and `date_format` for more information. 
Also feel free to change features of the `fig` and `ax` objects inside the `init()` function.
