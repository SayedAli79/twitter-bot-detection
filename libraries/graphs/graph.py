import pylab as pl
import numpy as np
import matplotlib.pyplot as plt

class Graph(object):
    def __init__(self, output_path):
        self.output_path = output_path

    def avg_tweets(self, avg_mention_users, avg_mention_bots, path):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.yaxis.grid(True)
        ax.set_ylabel("avg mentions per tweet")

        ax.boxplot([ avg_mention_users, avg_mention_bots ], vert=True, patch_artist=True)

        pl.setp(ax, xticks=[1, 2], xticklabels=[ "Humans", "Bots"])
        pl.savefig(path)

