import os
from libraries.models import Tweet, User
from config import app_config as cfg
from libraries.graphs.graph import Graph
from libraries.classification import Entropy

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

# Metrics
#  Account reputation
Accountrep_human = User.followers_friends_per_users(human_users)
Accountrep_bot = User.followers_friends_per_users(bot_users)
#  Tweeting density
tweetdens_human, mean_count_user, median_count_user = Tweet.tweet_density(human_tweets)
tweetdens_bot, mean_count_bot, median_count_bot = Tweet.tweet_density(bot_tweets)
#  tweets per week days
weekday_human = Tweet.tweet_weekday(human_tweets)
weekday_bot = Tweet.tweet_weekday(bot_tweets)
#  avg_mentions_per_user
mentions_human = Tweet.avg_mentions_per_user(human_tweets).values()
mentions_bot = Tweet.avg_mentions_per_user(bot_tweets).values()
#  Vocabulary size per users
voc_human = Tweet.vocabulary_size(human_tweets).values()
voc_bot = Tweet.vocabulary_size(bot_tweets).values()
#  Follower / Following ratio
ratio_human = User.ratio_followers_following_per_users(human_users)
ratio_bot = User.ratio_followers_following_per_users(bot_users)



### Average mentions per user
#path ="{}/images/avg_mentions.png".format(current_path)
#graph.avg_tweets(
#    mentions_human,
#    mentions_bot,
#    path
#)

### Vocabulary size per users
#path ="{}/images/vocabulary.png".format(current_path)
#graph.vocabulary(
#    voc_human,
#    voc_bot,
#    path
#)

### ratio followers/following
#path ="{}/images/followers_following.png".format(current_path)
#graph.ratio_followers_following(
#    ratio_human,
#    ratio_bot,
#    path
#)

### number of tweets during active days
#path ="{}/images/density.png".format(current_path)
#graph.hist_density(
#    tweetdens_human,
#    tweetdens_bot,
#    mean_count_user,
#    median_count_user,
#    mean_count_bot,
#    median_count_bot,
#    path
#)

### number of tweets per week days
#path ="{}/images/weekdays.png".format(current_path)
#graph.hist_weekday(
#    weekday_human,
#    weekday_bot,
#    path
#)

## Nb followers/following
#path ="{}/images/followers_following.png".format(current_path)
#graph.Nb_followers_following(
#    Accountrep_human,
#    Accountrep_bot,
#    path
#)

## Entropy depending on Human or bot
information_gains = Entropy().information_gains(Accountrep_human,Accountrep_bot,tweetdens_human,tweetdens_bot
             ,weekday_human,weekday_bot,mentions_human,mentions_bot
             ,voc_human,voc_bot,ratio_human,ratio_bot)

print(information_gains)



