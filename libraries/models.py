from peewee import *
from config import app_config as cfg
from collections import defaultdict
import numpy as np

db = SqliteDatabase(cfg.database["name"])

def create_database():
    db.connect()
    db.drop_tables([Tweet])
    db.create_tables([Tweet])

class BaseModel(Model):
    class Meta:
        database = db

class Tweet(BaseModel):
    name = CharField()
    is_bot = BooleanField()
    text = CharField()
    date = CharField()
    mentions = CharField()

    @classmethod
    def avg_mentions_per_user(cls, is_bot=False):
        tweets = Tweet.select().where(Tweet.is_bot == is_bot)

        mentions_per_user = defaultdict(lambda: [])
        for tweet in tweets:
            count = 0
            if len(tweet.mentions) > 0:
                count = len(tweet.mentions.split(","))
            mentions_per_user[tweet.name].append(count)

        avg_per_user = {user: np.mean(mentions) for (user, mentions) in mentions_per_user.iteritems()}

        return avg_per_user

    @classmethod
    def vocabulary_size(cls, is_bot=False, min_tweets=200):
        selected_users = Tweet.select(Tweet.name).group_by(Tweet.name).having(fn.Count() >= min_tweets)
        tweets = (Tweet.select()
            .where(
                (Tweet.is_bot == is_bot) &
                (Tweet.name << selected_users )
            ))


        words_per_user = defaultdict(lambda: set())
        for tweet in tweets:
            for word in tweet.text.split(" "):
                words_per_user[tweet.name].add(word)

        return {name: len(words) for (name, words) in words_per_user.iteritems()}