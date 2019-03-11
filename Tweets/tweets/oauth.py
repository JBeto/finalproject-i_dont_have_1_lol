from requests_oauthlib import OAuth1
import tweets.config as config


def authenticate():
    return OAuth1(client_key=config.CONSUMER_KEY,
                  client_secret=config.CONSUMER_SECRET,
                  resource_owner_key=config.ACCESS_TOKEN,
                  resource_owner_secret=config.ACCESS_SECRET,
                  decoding=None)
