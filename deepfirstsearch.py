from libraries.tweetimporter import TweetImporter
from libraries.twitterclient import TwitterClient

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
    importer.fromUser(args.specified_user, 200)

    # initial user mark as visited (stack) 
    stack.append(initial_user.screen_name)

    # load the nodes to visit next (followers list)
    nodes = client.followers_ids(args.specified_user)

    new_nodes = []

    for node in nodes:
        if node in stack:
             pass
        else:
            # import tweets from followers of each node
            importer.fromUser(node, 200)
            # mark the node as visited (stack) 
            stack.append(node)
            # new list of followers to investigate
            new_nodes.append(client.followers_ids(args.specified_user)) 

    print(len(new_nodes))





