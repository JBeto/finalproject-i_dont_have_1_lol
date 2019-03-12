from .listener import URLTitleListener
from .streams import FilterStream
import tweets.oauth as oauth
import tweets.config as config
import logging


# Configure root logger
logging.basicConfig(filename=config.LOG_FILE,
                    level=logging.INFO)

_logger = logging.getLogger(__name__)


def main():
    try:
        auth = oauth.authenticate(consumer_key=config.CONSUMER_KEY,
                                  consumer_secret=config.CONSUMER_SECRET,
                                  access_token=config.ACCESS_TOKEN,
                                  access_secret=config.ACCESS_SECRET)

        stream_listener = URLTitleListener(config.TWEETS_FILE)
        stream = FilterStream(auth=auth, stream_listener=stream_listener)
        stream.stream_async_geo_data()

        # Wait until user decides to exit the stream
        while True:
            stream.close_stream()
    except Exception as e:
        _logger.exception('Fatal error: {}'.format(str(e)))
