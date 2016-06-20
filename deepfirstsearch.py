from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient

import argparse

from config import app_config as cfg

from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient

from libraries.models import create_database
import tweepy

# Twitter API configuration
consumer_key = cfg.twitter["consumer_key"]
consumer_secret = cfg.twitter["consumer_secret"]

access_token = cfg.twitter["access_token"]
access_token_secret = cfg.twitter["access_token_secret"]

# Command line options
parser = argparse.ArgumentParser(description='provide additional information to run the bot detection')
parser.add_argument('specified_user', action="store", help='load tweets from the specified user')
parser.add_argument('--crawl', action="store_true", help="crawl through twitter users (starting by the user's followers) till a limit is reached")
parser.add_argument('--create-db', action="store_true", help='create or drop the database if it already exists')
parser.add_argument('--is-bot', action="store_true", help='the specified user will be flag as bot')

args = parser.parse_args()

# Start
if args.create_db:
    create_database()

if args.crawl:

    # initialize the list of users crawled
    crawled_users = []

    client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)
    importer = TweetImporter(client)
    initial_user = importer.createUser(args.specified_user)

    # import tweets from initial user
    importer.fromUser(args.specified_user, 200)

    # initial user mark as scanned 
    crawled_users.append(initial_user.screen_name)

    # load the followers to scan (followers list)
    followers_from_scan = client.followers_ids(args.specified_user)


    def follower_crawl(followers_from_crawl,crawled_users,crawl_depth=1):
        # init new nodes to investigate from node
        new_followers = []
        for follower in followers_from_crawl:
            if follower in crawled_users:
                 pass
            else:
                # try/except here to avoid protected followers to breack for loop
                try:
                    # new list of followers to investigate
                    crawl_followers = client.followers_ids(follower)
                except tweepy.TweepError:
                    print("Failed to import followers from that user, Skipping...")
                    crawl_followers = ['']
                # mark the node as visited (stack) 
                crawled_users.append(follower)
                # check weither new followers have already been investigated -> discard followers that are already investigated
                for crawled_follower in crawled_followers:
                    if not crawled_follower in (crawled_users, followers_from_crawl):
                        new_followers.append(crawled_follower) 
                    else:
                        pass
       # condition to end recursive function is depth == 0
       crawl_depth = crawl_depth - 1
       # check condition to end the recursive function 
       if crawl_depth > 0:
           print(crawl_depth > 0, "crawling through followers...")
           return follower_crawl(new_followers,crawled_users,crawl_depth=crawl_depth)
       elif crawl_depth == 0: 
           print(crawl_depth == 0, "end of crawling procedure")  
           total_crawl_list = crawled_users + new_followers
           return (total_crawl_list)
       else:
           print(crawl_depth < 0, "ErrorValue: negative value for crawling depth!")          

# ______ MAKE NEW FUNCTION __________________
# import tweets from followers of each node
    def tweet_crawl(total_crawl_list):
        for user in total_crawl_list:
            importer.fromUser(user, 200)


