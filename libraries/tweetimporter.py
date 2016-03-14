import unicodedata

class TweetImporter(object):
    def __init__(self, twitter_client, database):
        self.twitter_client = twitter_client
        self.database = database

    def importData(self, user, tweets_number=100):
        # TODO: move to twitterclient
        user_info = self.twitter_client.api.user_timeline(screen_name = user, count = tweets_number)

        name_mentions = []
        for i, status in enumerate(user_info):
            tweet = status._json
            text = tweet['text']
            date = tweet['created_at']
            entities = tweet['entities']
            user_mentions = entities['user_mentions']
            for mention in user_mentions:
                dict_mentions = mention
                name_mentions = dict_mentions['screen_name']

            id_string   = i
            name_string = user
            text_string = unicodedata.normalize('NFKD', text).encode('ascii','ignore')
            date_string = unicodedata.normalize('NFKD', date).encode('ascii','ignore')
            name_mentions_string = unicodedata.normalize('NFKD', name_mentions).encode('ascii','ignore')

            self.database.feed_table(id_string,
                name_string,
                text_string,
                date_string,
                name_mentions_string)