import unicodedata
from models import Tweet, User
import tweepy

class TweetImporter(object):
    def __init__(self, twitter_client):
        self.twitter_client = twitter_client

    def createUser(self, screen_name, is_bot=False):
        api_user = self.twitter_client.user_shows(screen_name=screen_name)

        user = User.create(
            screen_name=screen_name,
            is_bot=is_bot,
            followers=api_user.followers_count,
            following=api_user.friends_count
        )

        return user

    def fromUser(self, screen_name, tweets_number=10, is_bot=False):

            user = self.createUser(screen_name, is_bot)

            tweets = self.twitter_client.user_timeline(screen_name=screen_name, count=tweets_number)
            for i, status in enumerate(tweets):
                tweet = status._json
                text = tweet['text']
                date = tweet['created_at']
                entities = tweet['entities']
                user_mentions = entities['user_mentions']
                mentions_list = []

                if len(user_mentions) > 0:
                    for mention in user_mentions:
                        mentions_list.append(mention['screen_name'])

                text_string = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
                date_string = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
                name_mentions_string = ",".join(mentions_list)

                Tweet.create(
                        user = user,
                        text = text_string,
                        date = date_string,
                        source = status.source,
                        mentions = name_mentions_string
                )


    def fromFollowers(self, user, tweets_number=10):
        followers = self.twitter_client.followers_list(screen_name=user, count=200)

        for j, follower in enumerate(followers):
            self.fromUser(follower, tweets_number)

    def follower_crawl(self,followers_from_crawl,crawled_users,crawl_depth):
        # init new nodes to investigate from node
        new_followers = []
        for follower in followers_from_crawl:
            if follower in crawled_users:
                 pass
            else:
                # try/except here to avoid protected followers to breack for loop
                try:
                    # new list of followers to investigate
                    crawled_followers = self.twitter_client.followers_ids(follower)

                    # mark the node as visited (stack) 
                    crawled_users.append(follower)
                    # check weither new followers have already been investigated -> discard followers that are already investigated
                    for crawled_follower in crawled_followers:
                        if not crawled_follower in (crawled_users, followers_from_crawl):
                            new_followers.append(crawled_follower) 
                        else:
                            pass
                except tweepy.TweepError:
                    print("Failed to import followers from {}, Skipping...").format(crawled_follower)
        # condition to end recursive function is depth == 0
        crawl_depth = crawl_depth - 1
        # check condition to end the recursive function 
        if crawl_depth > 0:
            print(crawl_depth > 0, "crawling through followers...")
            return follower_crawl(new_followers,crawled_users,crawl_depth)
        elif crawl_depth == 0: 
            print(crawl_depth == 0, "end of crawling procedure")  
            total_crawl_list = crawled_users + new_followers
            return (total_crawl_list)
        else:
            print(crawl_depth < 0, "ErrorValue: negative value for crawling depth!")          


# import tweets from followers of each node
    def tweet_crawl(self,total_crawl_list):
        for user in total_crawl_list:
            try:
                self.fromUser(user, 200)
            except tweepy.TweepError:
                print("Failed to import tweets from {}, Skipping...").format(user)
        print("end of tweets importation")

