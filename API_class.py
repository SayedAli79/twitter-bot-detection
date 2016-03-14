class API_config():
    
    def __init__(self, app_config,tweepy):
        self.app_config = app_config
        self.tweepy = app_config

    def API_launch(self):
        
# Twitter API configuration
        consumer_key = app_config.twitter["consumer_key"]
        consumer_secret = app_config.twitter["consumer_secret"]

        access_token = app_config.twitter["access_token"]
        access_token_secret = app_config.twitter["access_token_secret"]

# Start
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)
        return api

API_test = API_config(app_config,tweepy)
API_start = API_test.API_launch()
