import os

##################
# KEYS / SECRETS #
##################

TWEETS_FILE = 'tweets.data'
LOG_FILE = '../tweets.log'

##################
# KEYS / SECRETS #
##################

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

#########################
# TWITTER API ENDPOINTS #
#########################

API_BASE = 'https://api.twitter.com'
STREAM_BASE = 'https://stream.twitter.com'
STREAM_VERSION = '1.1'

API_URLS = {
    'stream_filter': '{host}/{version}/statuses/filter.json'.format(host=STREAM_BASE, version=STREAM_VERSION),
    'stream_sample': '{host}/{version}/statuses/sample.json'.format(host=STREAM_BASE, version=STREAM_VERSION),
    'oauth': '{host}/oauth2/token'.format(host=API_BASE)
}
