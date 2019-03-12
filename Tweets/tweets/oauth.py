from requests_oauthlib import OAuth1


def authenticate(consumer_key, consumer_secret, access_token, access_secret):
    return OAuth1(client_key=consumer_key,
                  client_secret=consumer_secret,
                  resource_owner_key=access_token,
                  resource_owner_secret=access_secret,
                  decoding=None)
