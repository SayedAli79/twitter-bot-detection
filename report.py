import os
from libraries.models import Tweet, User
from config import app_config as cfg
from libraries.graphs.graph import Graph

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]


# Start
current_path = os.path.dirname(os.path.abspath(__file__))
graph = Graph()

# Average mentions per user
path ="{}/images/avg_mentions.png".format(current_path)
avg_mentions_per_user = Tweet.avg_mentions_per_user().values()
avg_mentions_per_bot = Tweet.avg_mentions_per_user(True).values()
graph.avg_tweets(avg_mentions_per_user, avg_mentions_per_bot, path)

path ="{}/images/vocabulary.png".format(current_path)
graph.vocabulary(Tweet.vocabulary_size().values(), Tweet.vocabulary_size(True).values(), path)

path ="{}/images/followers_following.png".format(current_path)
graph.ratio_followers_following(
    User.ratio_followers_following_per_users(),
    User.ratio_followers_following_per_users(is_bot=True),
    path
)

## number of tweets during active days
path ="{}/images/density.png".format(current_path)
tweet_density_per_user, mean_count_user, median_count_user = Tweet.tweet_density()
tweet_density_per_bot, mean_count_bot, median_count_bot = Tweet.tweet_density(True)
graph.hist_density(tweet_density_per_user,tweet_density_per_bot,mean_count_user,median_count_user,mean_count_bot,median_count_bot,path)

# number of tweets per week days
tweet_weekday_user = Tweet.tweet_weekday()
tweet_weekday_bot = Tweet.tweet_weekday(True)
path ="{}/images/weekdays.png".format(current_path)
graph.hist_weekday(tweet_weekday_user, tweet_weekday_bot,path)


