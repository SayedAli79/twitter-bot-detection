import os
from config import app_config as cfg

from libraries.database_init import DataBase
from libraries.graphs.graph import Graph

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]



# Start
current_path = os.path.dirname(os.path.abspath(__file__))
database = DataBase(cfg.database["name"], cfg.database["tweet_table"])

# Average mentions per user
path ="{}/images/avg_tweets.png".format(current_path)
graph = Graph(path)
avg_mentions_per_user = database.avg_mentions_per_user().values()
avg_mentions_per_bot = database.avg_mentions_per_user(True).values()
graph.avg_tweets(avg_mentions_per_user, avg_mentions_per_bot, path)
