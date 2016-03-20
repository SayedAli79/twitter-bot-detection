import pylab as pl
import numpy as np
from matplotlib.lines import Line2D


class Graph(object):
    def __init__(self, output_path):
        self.output_path = output_path

    def avg_tweets(self, avg_mention_per_user):
        path = "{}/avg_tweets.png".format(self.output_path)

        ax = pl.axes(frameon=False)         # Remove frame
        ax.get_yaxis().set_visible(False)   # Remove y axis
        ax.get_xaxis().tick_bottom()        # Remove top ticks

        values = avg_mention_per_user.values()
        ax.plot(values, np.zeros_like(values), 'o')

        # Draw xaxis
        xmin, xmax = ax.get_xaxis().get_view_interval()
        ymin, ymax = ax.get_yaxis().get_view_interval()
        ax.add_artist(Line2D((xmin, xmax), (ymin, ymin), color='black', linewidth=2))

        pl.savefig(path)

