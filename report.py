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

# Average mentions per user
path ="{}/images/avg_mentions.png".format(current_path)
graph = Graph(path)
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






