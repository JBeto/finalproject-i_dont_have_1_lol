from tweets.listener import FileStream
from tweets.streams import FilterStream, map_urls
import tweets.oauth as oauth
import tweets.config as config
import logging


# Configure project logger
def configure_logger():
    # create logger
    logger = logging.getLogger('tweets')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.FileHandler(filename=config.LOG_FILE)
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)


configure_logger()
_logger = logging.getLogger(__name__)


CHUNKS = 10
MAX_TWEETS = 325000

# Credit: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/

def chunkify(tweets, num_chunks):
    for i in range(0, len(tweets), num_chunks):
        yield tweets[i:i+num_chunks]


def main():
    try:
        auth = oauth.authenticate(consumer_key=config.CONSUMER_KEY,
                                  consumer_secret=config.CONSUMER_SECRET,
                                  access_token=config.ACCESS_TOKEN,
                                  access_secret=config.ACCESS_SECRET)

        data_stream = FileStream(config.TWEETS_FILE)
        stream = FilterStream(auth=auth, stream_listener=data_stream)
        stream.stream_async_geo_data()

        # Wait until size is > 1 GB determined by ls -l or until we reach > 325,000 tweets
        user = ''
        while user != 'quit' and data_stream.tweets_gathered < MAX_TWEETS:
            user = input('Type \'quit\' to exit out, type anything else to get a status update: ')
            print('Tweets gathered: {}'.format(data_stream.tweets_gathered))
        stream.close_stream()

        # Add the url title to the raw json as a field
        fs = FileStream(config.URL_TITLE_FILE)
        fs.on_open()
        with open(config.TWEETS_FILE, 'r') as f:
            tweets = f.read().splitlines()
            # write chunks to file
            for chunk in chunkify(tweets, CHUNKS):
                map_urls(chunk, fs, 16)
        fs.on_close()

    except Exception as e:
        print('Fatal Error!')
        _logger.exception('Fatal error: {}'.format(str(e)))


if __name__ == '__main__':
    main()
