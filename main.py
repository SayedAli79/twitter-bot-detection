import os
import argparse

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

parser = argparse.ArgumentParser(description='provide additional information to run the bot detection')
parser.add_argument('specified_user', action="store",help='specify the twitter user to investigate')

arg_results = parser.parse_args()
importer = TweetImporter(client, database)
importer.importData(arg_results.specified_user, 200)

# dir = os.path.dirname(os.path.abspath(__file__))
# out = "{}/images".format(dir)
#
# g = Graph(out)
# g.avg_tweets(database.avg_mentions_per_user())
