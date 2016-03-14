import app_config
from libraries.twitterclient import TwitterClient


# Twitter API configuration
consumer_key = app_config.twitter["consumer_key"]
consumer_secret = app_config.twitter["consumer_secret"]

access_token = app_config.twitter["access_token"]
access_token_secret = app_config.twitter["access_token_secret"]

api = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)





