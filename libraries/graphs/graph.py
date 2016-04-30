import pylab as pl
import matplotlib.pyplot as plt

class Graph(object):
    def __init__(self, output_path):
        self.output_path = output_path

    def avg_tweets(self, values_human, values_bot, path):
        self.boxplot(values_human, values_bot, "Avg mentions per tweet", path)

    def vocabulary(self, values_human, values_bot, path):
        self.boxplot(values_human, values_bot, "Vocabulary size", path)

    def ratio_followers_following(self, values_human, values_bot, path):
        self.boxplot(values_human, values_bot, "Ratio followers/following", path)

    def boxplot(self, values_human, values_bot, title, path):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.yaxis.grid(True)
        ax.set_ylabel(title)

        ax.boxplot([values_human, values_bot], vert=True, patch_artist=True)

        pl.setp(ax, xticks=[1, 2], xticklabels=[ "Humans", "Bots"])
        pl.savefig(path)