from peewee import *
from config import app_config as cfg
from collections import defaultdict
import numpy as np
from pandas import DataFrame
from dateutil import parser
from itertools import product

db = SqliteDatabase(cfg.database["name"])


def create_database():
    db.connect()
    db.drop_tables([User, Tweet], True)
    db.create_tables([User, Tweet], True)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    screen_name = CharField()
    is_bot = BooleanField()
    followers = IntegerField()
    following = IntegerField()

    def ratio_followers_following(self):
        if self.following == 0:
            return 0

        return self.followers / float(self.following)

    @classmethod
    def ratio_followers_following_per_users(self, is_bot=False):
        users = User.select().where(User.is_bot == is_bot)

        return [user.ratio_followers_following() for user in users]


class Tweet(BaseModel):
    user = ForeignKeyField(User, related_name='tweets')
    text = CharField()
    date = CharField()
    mentions = CharField()

    @classmethod
    def avg_mentions_per_user(cls, is_bot=False):
        tweets = Tweet.select(Tweet).join(User).where(User.is_bot == is_bot)

        mentions_per_user = defaultdict(lambda: [])
        for tweet in tweets:
            count = 0
            if len(tweet.mentions) > 0:
                count = len(tweet.mentions.split(","))
            mentions_per_user[tweet.user_id].append(count)

        avg_per_user = {user: np.mean(mentions) for (user, mentions) in mentions_per_user.iteritems()}

        return avg_per_user

    @classmethod
    def vocabulary_size(cls, is_bot=False, min_tweets=200):
        selected_users = Tweet.select(Tweet.user) \
            .group_by(Tweet.user) \
            .having(fn.Count() >= min_tweets)

        tweets = (Tweet.select(Tweet).join(User)
            .where(
            (User.is_bot == is_bot) &
            (User.id << selected_users)
        ))

        words_per_user = defaultdict(lambda: set())
        for tweet in tweets:
            for word in tweet.text.split(" "):
                words_per_user[tweet.user_id].add(word)

        return {name: len(words) for (name, words) in words_per_user.iteritems()}

    @classmethod
    def tweet_density(cls, is_bot=False, min_tweets=200):
        selected_users = Tweet.select(Tweet.user) \
            .group_by(Tweet.user) \
            .having(fn.Count() >= min_tweets)

        tweets = (Tweet.select(Tweet).join(User)
            .where(
            (User.is_bot == is_bot) &
            (User.id << selected_users)
        ))

        parsed_date = []
        tweet_user = []

        for i, tweet in enumerate(tweets):
            tweet_user.append(tweet.user_id)
            parsed_date.append(parser.parse(tweet.date))

        year_date = DataFrame(columns=["year", "month", "day"], index=range(len(parsed_date)))

        for i, date in enumerate(parsed_date):
            year_date["year"][i] = date.year
            year_date["month"][i] = date.month
            year_date["day"][i] = date.day

        year_date["user_id"] = tweet_user

        count_list_by_user = []
        total_count_list = []
        unique_users = list(set(year_date["user_id"]))
        for user in unique_users:
            year_date_by_user = year_date[year_date["user_id"] == user]
            year = range(year_date_by_user["year"].min(), year_date_by_user["year"].max() + 1)
            month = range(1, 13)
            for y, m in product(year, month):
                count = year_date_by_user["day"][year_date_by_user["year"] == y][
                    year_date_by_user["month"] == m].value_counts()
                for i in list(count):
                    if i < 6:
                        count_list_by_user.append(i)
                    else:
                        count_list_by_user.append(6)

        mean_count = np.mean(count_list_by_user)
        median_count = np.median(count_list_by_user)

        return count_list_by_user, mean_count, median_count
