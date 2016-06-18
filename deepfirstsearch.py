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

    # initialize the stack
    stack = []

    client = TwitterClient(consumer_key, consumer_secret, access_token, access_token_secret)
    importer = TweetImporter(client)
    initial_user = importer.createUser(args.specified_user)

    # import tweets from initial user
    importer.fromUser(node, 200)

    # initial user mark as visited (stack) 
    stack.append(initial_user.screen_name)

    # load the nodes to visit next (followers list)
    nodes = client.followers_ids(args.specified_user)


    def follower_crawl(nodes,stack,depth=1):
        # init new nodes to investigate from node
        new_nodes = []
        for node in nodes:
            if node in stack:
                 pass
            else:
                # try/except here to avoid protected followers to breack for loop
                try:
                    # new list of followers to investigate
                    node_followers = client.followers_ids(node)
                except tweepy.TweepError:
                    print("Failed to import followers from that user, Skipping...")
                    node_followers = ['']
                # mark the node as visited (stack) 
                stack.append(node)
                # check weither new followers have already been investigated -> discard followers that are already investigated
                for follower in node_followers:
                    if not follower in (stack, nodes):
                        new_nodes.append(follower) 
                    else:
                        pass
       # condition to end recursive function is depth == 0
       depth = depth - 1
       # check condition to end the recursive function 
       if depth > 0:
           print(depth > 0, "crawling through followers...")
           follower_crawl(new_nodes,stack,depth=depth)
       else: 
           print(depth == 0, "end of crawling procedure")  
        return (stack, new_nodes)

# ______ MAKE NEW FUNCTION __________________
# import tweets from followers of each node
#importer.fromUser(node, 200)

