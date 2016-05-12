import pylab as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

        pl.setp(ax, xticks=[1, 2], xticklabels=["Humans", "Bots"])
        pl.savefig(path)

    def hist_density(self, tweet_density_per_user, tweet_density_per_bot, mean_count_user, median_count_user,
                      mean_count_bot, median_count_bot, path):
        gaussian_kernel_density = []
        gaussian_kernel_density[:] = [x - 0.5 for x in tweet_density_per_user]

        fig = plt.figure()
        fig.subplots_adjust(hspace=.5)
        ax1 = plt.subplot(211)
        labels = ['', '1', '2', '3', '4', '5', '6+']
        ax1.set_xticklabels(labels)

        ax1.axis([0, 7, 0, 1])
        ax1.yaxis.set_label_coords(-0.1, 0)

        sns.distplot(gaussian_kernel_density, kde=False, bins=np.arange(1, 8) - 0.5, norm_hist=True)
        sns.distplot(tweet_density_per_user, kde=True, bins=np.arange(0, 8), hist=False)

        line_mean, = plt.plot((mean_count_user, mean_count_user), (0, 1), 'green')
        line_median, = plt.plot((median_count_user, median_count_user), (0, 1), 'red')

        plt.legend([line_mean, line_median], ['mean', 'median'])

        sns.plt.title('number of tweets per active tweeting day for USERS')
        sns.plt.xlabel('number of tweets')
        sns.plt.ylabel('fraction of active tweeting days (0 to 1)')

        gaussian_kernel_density = []
        gaussian_kernel_density[:] = [x - 0.5 for x in tweet_density_per_bot]

        ax2 = plt.subplot(212)
        ax2.axis([0, 7, 0, 1])
        labels = ['', '1', '2', '3', '4', '5', '6+']
        ax2.set_xticklabels(labels)

        sns.distplot(gaussian_kernel_density, kde=False, bins=np.arange(1, 8) - 0.5, norm_hist=True)
        sns.distplot(tweet_density_per_bot, kde=True, bins=np.arange(0, 8), hist=False)

        line_mean, = plt.plot((mean_count_bot, mean_count_bot), (0, 1), 'green')
        line_median, = plt.plot((median_count_bot, median_count_bot), (0, 1), 'red')

        plt.legend([line_mean, line_median], ['mean', 'median'])

        sns.plt.title('number of tweets per active tweeting day for BOTS')
        sns.plt.xlabel('number of tweets')

        pl.savefig(path)

    def hist_weekday(self, tweet_weekday_user, tweet_weekday_bot, path):
	fig = plt.figure()
	ax = plt.subplot(111)

	opacity = 0.4
        labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	bar_width = 0.3
	x = range(len(tweet_weekday_user["prop"]))
	#plt.xticks(x + bar_width)
        #ax.set_xticklabels(labels)
	plt.xticks([0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3], labels)
	ax.bar(x, tweet_weekday_user["prop"],bar_width,color='b',alpha=opacity,label='Users', yerr=tweet_weekday_user["std"])
	ax.bar([0.3, 1.3, 2.3, 3.3, 4.3, 5.3, 6.3], tweet_weekday_bot["prop"],bar_width,color='g',alpha=opacity,label='Bots', yerr=tweet_weekday_bot["std"])

	ax.set_xlabel('Week days')
	ax.set_ylabel('Tweets proportion per day (0 to 1)')
        sns.plt.title('Proportion of tweets for each week day')
	ax.legend()
        pl.savefig(path)
	

