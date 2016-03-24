import argparse

from config import app_config as cfg

from libraries.database_init import DataBase
from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]

# Command line options
parser = argparse.ArgumentParser(description='provide additional information to run the bot detection')
parser.add_argument('specified_user', action="store", help='load tweets from the specified user')
parser.add_argument('--followers', action="store_true", help="load tweets from user's followers")

args = parser.parse_args()

# Start
database = DataBase(cfg.database["name"], cfg.database["tweet_table"])
client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)
importer = TweetImporter(client, database)

database.create_table()

importer.fromUser(args.specified_user, 20)
if args.followers:
    importer.fromFollowers(args.specified_user, 20)

