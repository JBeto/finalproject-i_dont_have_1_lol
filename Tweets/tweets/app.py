from tweets.listener import FileStream, ListStream
from tweets.streams import FilterStream, map_urls
import tweets.oauth as oauth
import tweets.config as config
import logging
import time


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


GIGABYTE = 2500000  # 1073741824


def main():
    try:
        auth = oauth.authenticate(consumer_key=config.CONSUMER_KEY,
                                  consumer_secret=config.CONSUMER_SECRET,
                                  access_token=config.ACCESS_TOKEN,
                                  access_secret=config.ACCESS_SECRET)

        data_stream = ListStream()
        stream = FilterStream(auth=auth, stream_listener=data_stream)
        stream.stream_async_geo_data()

        # Wait until size is > 1 GB
        user = ''
        while user != 'quit':
            user = input('Type \'quit\' to exit out, type anything else to get a status update: ')
            print('Tweets gathered: {}'.format(len(data_stream.data)))

        stream.close_stream()
        file_stream = FileStream(config.TWEETS_FILE)
        map_urls(data_stream.data, file_stream, 16)

    except Exception as e:
        print('Fatal Error!')
        _logger.exception('Fatal error: {}'.format(str(e)))


if __name__ == '__main__':
    main()
