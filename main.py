import app_config
from libraries.twitterclient import TwitterClient
from libraries.database_init import DataBase

# Twitter API configuration
consumer_key = app_config.twitter["consumer_key"]
consumer_secret = app_config.twitter["consumer_secret"]

access_token = app_config.twitter["access_token"]
access_token_secret = app_config.twitter["access_token_secret"]

db = DataBase()

Tweet_db = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)




