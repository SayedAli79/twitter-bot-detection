import tweepy
import app_config

# Twitter API configuration
consumer_key = app_config.twitter["consumer_key"]
consumer_secret = app_config.twitter["consumer_secret"]

access_token = app_config.twitter["access_token"]
access_token_secret = app_config.twitter["access_token_secret"]

# Start
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

followers = api.followers(count=200)
for follower in followers:
    print follower.screen_name