"""
    Twitter API
"""
import tweepy


class TwitterAPI:
    API_KEY = 'EwEg2CK0OgSMBxXL2IH6JT1sp'
    API_SECRET = 'rgVCQa5p5PMgRwEVLKXJfrkZp9f6Rii2i18YLdLjBnBYUmg1GR'
    ACCESS_TOKEN = '1097861108780519424-uifbGPTKHmCNZFl4GndOuedlE8f5iR'
    ACCESS_SECRET = 'rARDVVZDq8izOP35WIAO5ckSEhFQ2Nfx80TY0Df8GShPF'

    def push_update(self, tweet):
        try:
            api = self.get_api({
                "consumer_key": self.API_KEY,
                "consumer_secret": self.API_SECRET,
                "access_token": self.ACCESS_TOKEN,
                "access_token_secret": self.ACCESS_SECRET
            })
            status = api.update_status(status=tweet)
            if status:
                return True
            else:
                return False
        except:
            return False

    def get_api(self, cfg):
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)
