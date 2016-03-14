import tweepy
import json
import unicodedata
import sqlite3

class TwitterClient(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def followers_list(self, number_followers=5):
        followers =  self.api.followers(count=number_followers)

        followers_name = []
        for follower in followers:
            followers_name.append(str(follower.screen_name))
            
        self.followers_name = followers_name 

