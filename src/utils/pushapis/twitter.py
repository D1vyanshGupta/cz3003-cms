"""
    Twitter API
"""
import tweepy


class TwitterAPI:
    API_KEY = 'J1zlXWbPXeKR7tjgQnM28Moj6'
    API_SECRET = 'XTXYkDtRTZMpKlUD3SkPtudBl6dH4uQWSA1ClqVQFYd07DkQe1'
    ACCESS_TOKEN = '708263718585372672-DoPcGuN849xdwPmIaYjAknYDsAA3iVF'
    ACCESS_SECRET = 'OtnBKub9qERxOLIfqswkAYSPJ7j2R9V3kLhaUzjSkL7dD'

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
