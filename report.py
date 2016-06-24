import os
from libraries.models import Tweet, User
from config import app_config as cfg
from libraries.graphs.graph import Graph
import csv

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]

# Start
current_path = os.path.dirname(os.path.abspath(__file__))
graph = Graph()

human_tweets = Tweet.get_sample()
bot_tweets = Tweet.get_sample(is_bot=True)
human_users = User.get_sample()
bot_users = User.get_sample(True)

# top sources
if os.path.isfile('reports/top_sources_human.csv') == False or os.path.isfile('reports/top_sources_bot.csv') == False:
    top_sources_human = Tweet.top_sources(human_tweets)
    top_sources_bot = Tweet.top_sources(bot_tweets)
    list_top_sources_human = zip(top_sources_human.keys(),top_sources_human.values)
    list_top_sources_bot = zip(top_sources_bot.keys(),top_sources_bot.values)
    with open('reports/top_sources_human.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in list_top_sources_human:
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                row = tuple(list(('UnicodeEncodeError',row[1])))  
                writer.writerow(row)
    with open('reports/top_sources_bot.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in list_top_sources_bot:
            try:
                writer.writerow(row)
            except UnicodeEncodeError:
                row = tuple(list(('UnicodeEncodeError',row[1])))  
                writer.writerow(row)
    path ="{}/images/top_sources.png".format(current_path)
    graph.top_sources(
        top_sources_human,
        top_sources_bot,
        path
    )


# Average mentions per user
if os.path.isfile('reports/avg_mentions_per_human.csv') == False or os.path.isfile('reports/avg_mentions_per_bot.csv') == False:
    avg_mentions_per_human = list(Tweet.avg_mentions_per_user(human_tweets).values())
    avg_mentions_per_bot = list(Tweet.avg_mentions_per_user(bot_tweets).values())
    with open('reports/avg_mentions_per_human.csv', 'wb') as f:
        writer = csv.writer(f, delimiter = ',')
        for row in avg_mentions_per_human:
            writer.writerow([row])
    with open('reports/avg_mentions_per_bot.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in avg_mentions_per_bot:
            writer.writerow([row])
    path ="{}/images/avg_mentions.png".format(current_path)
    graph.avg_tweets(
        avg_mentions_per_human,
        avg_mentions_per_bot,
        path
    )

## Vocabulary size per users
if os.path.isfile('reports/vocabulary_size_human.csv') == False or os.path.isfile('reports/vocabulary_size_bot.csv') == False:
    vocabulary_size_human = list(Tweet.vocabulary_size(human_tweets).values())
    vocabulary_size_bot = list(Tweet.vocabulary_size(bot_tweets).values())
    with open('reports/vocabulary_size_human.csv', 'wb') as f:
        writer = csv.writer(f, delimiter = ',')
        for row in vocabulary_size_human:
            writer.writerow([row])
    with open('reports/vocabulary_size_bot.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in vocabulary_size_bot:
            writer.writerow([row])
    path ="{}/images/vocabulary.png".format(current_path)
    graph.vocabulary(
        vocabulary_size_human,
        vocabulary_size_bot,
        path
    )

# number of tweets during active days
if os.path.isfile('reports/tweet_density_per_human.csv') == False or os.path.isfile('reports/tweet_density_per_bot.csv') == False:
    tweet_density_per_human, mean_count_user, median_count_user = Tweet.tweet_density(human_tweets)
    tweet_density_per_bot, mean_count_bot, median_count_bot = Tweet.tweet_density(bot_tweets)
    with open('reports/tweet_density_per_human.csv', 'wb') as f:
        writer = csv.writer(f, delimiter = ',')
        for row in tweet_density_per_human:
            writer.writerow([row])
    with open('reports/tweet_density_per_bot.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in tweet_density_per_bot:
            writer.writerow([row])
    path ="{}/images/density.png".format(current_path)
    graph.hist_density(
        tweet_density_per_human,
        tweet_density_per_bot,
        mean_count_user,
        median_count_user,
        mean_count_bot,
        median_count_bot,
        path
    ) 


# number of tweets per week days
if os.path.isfile('reports/tweet_weekday_human.csv') == False or os.path.isfile('reports/tweet_weekday_bot.csv') == False:
    tweet_weekday_human = Tweet.tweet_weekday(human_tweets)
    tweet_weekday_bot = Tweet.tweet_weekday(bot_tweets)
    tweet_weekday_human.to_csv('reports/tweet_weekday_human.csv', sep=',')
    tweet_weekday_bot.to_csv('reports/tweet_weekday_bot.csv', sep=',')
    path ="{}/images/weekdays.png".format(current_path)
    graph.hist_weekday(
        Tweet.tweet_weekday(human_tweets),
        Tweet.tweet_weekday(bot_tweets),
        path
    )

# Nb followers/following
if os.path.isfile('reports/followers_friends_human.csv') == False or os.path.isfile('reports/followers_friends_bot.csv') == False:
    followers_friends_human = User.followers_friends_per_users(human_users)
    followers_friends_bot = User.followers_friends_per_users(bot_users)
    followers_friends_human.to_csv('reports/followers_friends_human.csv', sep=',')
    followers_friends_bot.to_csv('reports/followers_friends_bot.csv', sep=',')
    path ="{}/images/followers_following.png".format(current_path)
    graph.Nb_followers_following(
        followers_friends_human,
        followers_friends_bot,
        path
    )

