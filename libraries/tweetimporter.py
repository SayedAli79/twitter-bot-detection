import unicodedata

class TweetImporter(object):
    def __init__(self, twitter_client, database):
        self.twitter_client = twitter_client
        self.database = database

    def importData(self, user, tweets_number=10):
        followers = self.twitter_client.followers_list(screen_name=user, count=200)

        for j, follower in enumerate(followers):
            tweets = self.twitter_client.user_timeline(screen_name=follower, count=tweets_number)
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

                self.database.feed_table(
                    follower,
                    text_string,
                    date_string,
                    name_mentions_string)
