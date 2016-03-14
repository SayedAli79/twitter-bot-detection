import tweepy
import json
import unicodedata
import sqlite3

import app_config
import definitions

API_launch()

followers_list(followers_name[1])

create_db()

create_table()

tweet_info(followers_name[1],tweets_number=100)
