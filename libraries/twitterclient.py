import tweepy
import itertools

class TwitterClient(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def followers_list(self, screen_name, count=5):
        followers =  tweepy.Cursor(self.api.followers, screen_name=screen_name).items()

        return [ follower.screen_name for follower in followers if follower.protected == False]

    def user_timeline(self, screen_name, count=10):
        return self.api.user_timeline(screen_name = screen_name, count=count)

    def user_shows(self, screen_name):
        return self.api.get_user(screen_name)

    # Paginate manually user ids from followers_ids(self,screen_name)
    def paginate(self,iterable, page_size):
        while True:
            i1, i2 = itertools.tee(iterable)
            iterable, page = (itertools.islice(i1, page_size, None),
                    list(itertools.islice(i2, page_size)))
            if len(page) == 0:
                break
            yield page

    # followers_ids returns up to 5000 followers (twitter api limit) ids for the given screen_name (or id, user_id or cursor
    def followers_ids(self,screen_name):
        followers = self.api.followers_ids(screen_name=screen_name)
        follower_list = []
        #lookup_users can handle only 100 user ids at a time (twitter api limit)
        for page in self.paginate(followers, 100):
            results = self.api.lookup_users(user_ids=page)
            for result in results:
                follower_list.append(result.screen_name)
        return follower_list

