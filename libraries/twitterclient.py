import tweepy
import json
import unicodedata
import sqlite3

class TwitterClient(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def followers_list(self, number_followers=200):
        followers =  self.api.followers(count=number_followers)

        followers_name = []
        for follower in followers:
            followers_name.append(str(follower.screen_name))
            
        self.followers_name = followers_name 


    def feed_table(tweet_id ,followers_name,tweet_date ,tweet_text,tweet_mentions,database_name='bot_detection.db'):

        conn = sqlite3.connect(database_name)
        conn.execute("INSERT INTO TWEETS (ID,NAME,DATE,TEXT,MENTIONS) VALUES (?,?,?,?,?)"
                 ,(tweet_id ,followers_name,tweet_date ,tweet_text,tweet_mentions))

        conn.commit()
        conn.close()

    def tweet_info(follower,tweets_number=100):


        user_info = self.api.user_timeline(screen_name = follower,count = tweets_number)

        tweet = {}
        name_mentions = []

        for i,status in enumerate(user_info):
            tweet = status._json
            text = tweet['text']
            date = tweet['created_at']
            entities = tweet['entities']
            user_mentions = entities['user_mentions']
            for mention in user_mentions:
                dict_mentions = mention
                name_mentions = dict_mentions['screen_name']

        ID_string   = i
        name_string = follower       
        text_string = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        date_string = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
        name_mentions_string = unicodedata.normalize('NFKD', name_mentions).encode('ascii','ignore')

        feed_table(ID_string,
            name_string,
            text_string,
            date_string,
            name_mentions_string)
