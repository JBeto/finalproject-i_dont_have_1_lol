from tweets.listener import FileStream, ListStream
from tweets.streams import FilterStream, map_urls
import tweets.oauth as oauth
import tweets.config as config
import logging
import time


# Configure root logger
logging.basicConfig(filename=config.LOG_FILE,
                    level=logging.DEBUG)

_logger = logging.getLogger(__name__)


GIGABYTE = 1073741824


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
        start_time = time.time()
        while data_stream.byte_size() < GIGABYTE:
            elapsed = time.time() - start_time
            # every 5 minutes print out status report
            if elapsed > 5 * 60.0:
                start_time = time.time()
                print('Size of tweets: {} Bytes'.format(data_stream.byte_size()))

        stream.close_stream()
        file_stream = FileStream(config.TWEETS_FILE)
        map_urls(data_stream.data, file_stream, 16)

    except Exception as e:
        print('Fatal Error!')
        _logger.exception('Fatal error: {}'.format(str(e)))


if __name__ == '__main__':
    main()
