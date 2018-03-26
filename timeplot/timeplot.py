from collections import deque
from datetime import timedelta

import matplotlib.pyplot as plt
from matplotlib import spines, animation
from matplotlib.dates import num2date, MinuteLocator, DateFormatter, SecondLocator
from matplotlib.ticker import FormatStrFormatter


def timeplot(f, lcolors=None, lstyles=None, lwidths=None, llabels=None,
             title=None, period=300, interval=10, update_style='jump'):
    """
    A realtime plot for time series.

    Args:
        f (:obj:'method'): A function that returns a single tick in the form of a tuple
            (t, y1, ..., yn). Here t is a datetime object and y1, ..., yn
            are numerical values. The number n of lines to plot is determined
            automatically.
        lcolors (:obj:'list' of :obj:'str', optional): List of line colors.
            Must be either unspecified or specify a color for every line that is plotted.
            If unspecified, all line colors default to 'darkblue'.
        lstyles (:obj:'list' of :obj:'str', optional): List of line styles.
            Must be either unspecified or specify a style for every line that is plotted.
            If unspecified, all line styles default to 'solid'.
        lwidths (:obj:'list' of :obj:'str', optional): List of line widths.
            Must be either unspecified or specify a widhts for every line that is plotted.
            If unspecified, all line widths default to '1.0'.
        llabels (:obj:'list' of :obj:'str', optional): List of line labels.
            Must be either unspecified or specify a label for every line that is plotted;
            notice that it is legal to specify emtpy labels ''.
            If unspecified, no legend is created.
        title (str, optional): Plot title, shown in the upper left corner of the plot.
        period (int, optional): The size of the time range shown in the plot (in seconds).
        interval (int, optional): Update frequency for Matplotlib's FuncAnimation function.
            Set this to a small value if you are plotting a realtime data stream.
        update_style (str, optional): Either 'jump' or 'cont'. With 'jump', the time range
            shown is changed once every minute by jumping one minute further.
            With 'cont', the time range is updated every tick.
    Returns:
        None
    """

    def init():
        ax.clear()

        """ Initialize plot window and static plot elements """
        # Configure x-axis and y-axis
        ax.xaxis.set_major_locator(MinuteLocator())
        ax.xaxis.set_major_formatter(DateFormatter(time_format))
        ax.xaxis.set_minor_locator(SecondLocator(bysecond=[15, 30, 45]))
        ax.yaxis.tick_right()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.5f'))

        # Set colors
        fig.set_facecolor(colortheme['bg2'])
        ax.set_facecolor(colortheme['bg1'])
        for child in ax.get_children():
            if isinstance(child, spines.Spine):
                child.set_color(colortheme['fg1'])
        ax.xaxis.grid(color=colortheme['fg2'], linewidth=0.2)
        ax.yaxis.grid(color=colortheme['fg2'], linewidth=0.2)
        ax.tick_params(axis='both', colors=colortheme['fg1'])

        # Put more space below and above plot
        ax.set_ymargin(0.8)

        # Create title
        if title:
            ax.annotate(title, xy=(0.02, 0.945), xycoords='axes fraction',
                        ha='left', color=colortheme['fg1'])

        """ Determine number of plot lines and set default values 
            for line color, style and width """
        # Generate one tick to find out how many lines must be plotted
        tick = f()
        num_lines = len(tick) - 1

        # Set default values for lcolors, lstyles, lwidths and llabels
        lcols = lcolors if lcolors else [colortheme['fg1']] * num_lines
        lstys = lstyles if lstyles else ['-'] * num_lines
        lwids = lwidths if lwidths else [1.0] * num_lines

        # Check that user inputs have correct length
        assert (len(lcols) == num_lines) & \
               (len(lstys) == num_lines) & \
               (len(lwids) == num_lines) & \
               (not llabels or len(llabels) == num_lines), \
            'lcolors, lstyles, lwidths and llabels must either be unspecified' \
            'or their length must equal the number of plot lines'

        """ Initialize interactive plot elements """
        # Initialize x-axis
        ax.set_xlim(tick[0], tick[0] + timedelta(seconds=period + padding))

        # Initialize date textbox below x-axis
        date_text = ax.annotate('', xy=(0.5, -0.11), xycoords='axes fraction',
                                ha='center', color=colortheme['fg1'])
        timeplot.texts.append(date_text)

        # Initialize current tick value on y-axis
        value_text = ax.annotate('', xy=(1, 1), xycoords=ax.get_yaxis_transform(),
                                 xytext=(7, 0), textcoords='offset points',
                                 ha='left', va='center', color=colortheme['fg1'],
                                 bbox=dict(edgecolor=colortheme['fg1'],
                                           facecolor=colortheme['bg1']))
        timeplot.texts.append(value_text)

        # Initialize plot lines
        for i in range(num_lines):
            line = ax.plot([], [], c=lcols[i], ls=lstys[i], lw=lwids[i])[0]
            if llabels:
                line.set_label(llabels[i])
            timeplot.lines.append(line)

        """ Create legend """
        if llabels:
            handles = [line for line, label in zip(timeplot.lines, llabels) if label]
            plt.legend(handles=handles, loc='lower left')

        return animate(tick)

    def animate(tick):
        timeplot.ticks.append(tick)
        # Remove old ticks.
        # This keeps one tick that lies outside the plot range to make sure that
        # the plot always starts at the left border of the plot window.
        if len(timeplot.ticks) > 1:
            while timeplot.ticks[1][0] < (tick[0] - timedelta(seconds=period)):
                timeplot.ticks.popleft()

        # Autoscale axes
        ax.relim()
        ax.autoscale_view()

        # Set range for x-axis.
        xmin, xmax = (num2date(x).replace(tzinfo=None) for x in ax.get_xlim())
        if xmax < tick[0] + timedelta(seconds=padding):
            # Move x-axis to the right
            if update_style == 'jump':
                # Move x-axis by one minute
                ax.set_xlim(xmin + timedelta(minutes=1),
                            xmax + timedelta(minutes=1))
            elif update_style == 'cont':
                # Move x-axis by 'current tick time - previous tick time'
                ax.set_xlim(tick[0] - timedelta(seconds=period),
                            tick[0] + timedelta(seconds=padding))

        # Update lines
        for idx, line in enumerate(timeplot.lines):
            line.set_data([tick[0] for tick in timeplot.ticks],
                          [tick[idx + 1] for tick in timeplot.ticks])

        # Update date below x-axis
        timeplot.texts[0].set_text(tick[0].strftime(date_format))

        # Update tick value on y-axis
        timeplot.texts[1].set_text(round(tick[1], 5))
        timeplot.texts[1].xy = (1, tick[1])

        return timeplot.lines + timeplot.texts

    """ Some additional parameters """
    # Determines the (minimal) distance of the lines to the right border of the plot
    padding = 15
    # The color theme to use.
    # 'fg1' is the default color for most plot elements (lines, axes, labels),
    # 'fg2' is the color of the grid lines,
    # 'bg1' and 'bg2' are background colors.
    colortheme = {'fg1': 'darkblue', 'fg2': 'lightblue',
                  'bg1': 'white', 'bg2': 'white'}
    # Format of the time stamps on the x-axis
    time_format = '%H:%M'
    # Format of the date stamp below the x-axis. You might want to change this to American format '%m/%d/%Y'.
    date_format = '%d.%m.%Y'

    # Internal variables that keep track of plot elements and ticks
    timeplot.lines = []
    timeplot.texts = []
    timeplot.ticks = deque()

    # Start the animation
    fig, ax = plt.subplots()
    anim = animation.FuncAnimation(fig, lambda i: animate(f()),
                                   init_func=init, interval=interval)
    plt.show()
