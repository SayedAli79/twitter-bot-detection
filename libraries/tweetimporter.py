import unicodedata
from models import Tweet

class TweetImporter(object):
    def __init__(self, twitter_client):
        self.twitter_client = twitter_client

    def fromUser(self, user, tweets_number=10, is_bot=False):
        tweets = self.twitter_client.user_timeline(screen_name=user, count=tweets_number)
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
                    name = user,
                    is_bot = is_bot,
                    text = text_string,
                    date = date_string,
                    mentions = name_mentions_string
            )

    def fromFollowers(self, user, tweets_number=10):
        followers = self.twitter_client.followers_list(screen_name=user, count=200)

        for j, follower in enumerate(followers):
            self.fromUser(follower, tweets_number)

