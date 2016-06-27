import argparse

from config import app_config as cfg

from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient

from libraries.models import create_database

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]

# Command line options
parser = argparse.ArgumentParser(description='provide additional information to run the bot detection')
parser.add_argument('specified_user', action="store", help='load tweets from the specified user')
parser.add_argument('--followers', action="store_true", help="load tweets from user's followers")
parser.add_argument('--create-db', action="store_true", help='create or drop the database if it already exists')
parser.add_argument('--is-bot', action="store_true", help='the specified user will be flag as bot')
parser.add_argument('--crawl', action="store_true", help="crawl through twitter users (starting by the user's followers) till depth length is reached")
parser.add_argument('--depth', choices=['1','2','3'], default = '1' ,help='choose the depth of crawling')

args = parser.parse_args()

# Start
if args.create_db:
    create_database()

client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)
importer = TweetImporter(client)
importer.fromUser(args.specified_user, 200, args.is_bot)

if args.followers:
    importer.fromFollowers(args.specified_user, 200)

if args.crawl:

    # initialize the list of users crawled
    crawled_users = []

    initial_user = importer.createUser(args.specified_user)

    # initial user mark as scanned 
    crawled_users.append(initial_user.screen_name)

    # load the followers to scan (followers list)
    followers_from_scan = client.followers_ids(args.specified_user)

    total_crawl_list = importer.follower_crawl(followers_from_scan,crawled_users,int(args.depth))

    importer.tweet_crawl(total_crawl_list)

