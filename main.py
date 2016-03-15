import app_config
from libraries.twitterclient import TwitterClient
from libraries.database_init import DataBase
from libraries.tweetimporter import TweetImporter

# Twitter API configuration
consumer_key = app_config.twitter["consumer_key"]
consumer_secret = app_config.twitter["consumer_secret"]

access_token = app_config.twitter["access_token"]
access_token_secret = app_config.twitter["access_token_secret"]

# Start
database = DataBase("bot_detection.db","TWEETS")

client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)

importer = TweetImporter(client, database)
importer.importData("FranckBrignoli")



