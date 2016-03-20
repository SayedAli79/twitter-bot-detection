import os

from config import app_config as cfg

from libraries.database_init import DataBase
from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient
from libraries.graphs.graph import Graph

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]

# Start
database = DataBase(cfg.database["name"], cfg.database["tweet_table"])
database.create_table()

client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)

importer = TweetImporter(client, database)
importer.importData("FranckBrignoli", 200)

# dir = os.path.dirname(os.path.abspath(__file__))
# out = "{}/images".format(dir)
#
# g = Graph(out)
# g.avg_tweets(database.avg_mentions_per_user())