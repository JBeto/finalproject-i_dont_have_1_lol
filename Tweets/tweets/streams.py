from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import tweets.config as config
import multiprocessing as mp
import requests
import logging
import json


_logger = logging.getLogger(__name__)


def _get_url(tweet_dict):
    if 'entities' in tweet_dict and 'urls' in tweet_dict['entities'] and len(tweet_dict['entities']['urls']) > 0:
        return tweet_dict['entities']['urls'][0]['url']
    return None


def add_url_title(tweet):
    # get title information
    tweet_dict = json.loads(tweet)
    url = _get_url(tweet_dict)
    if url is not None:
        try:
            page = requests.get(url, timeout=3)
            soup = BeautifulSoup(page.text, 'html.parser')
            tweet_dict['url_title'] = soup.title.string if soup.title is not None else None
        except requests.RequestException as e:
            _logger.error('Error when parsing tweet url title: {}'.format(type(e)))
            tweet_dict['url_title'] = None
    else:
        tweet_dict['url_title'] = None

    # call listener on the final json
    tweet_json = json.dumps(tweet_dict)
    return tweet_json


def map_urls(tweets, listener, max_workers=8):
    p = mp.Pool(max_workers)
    listener.on_open()
    for item in p.map(add_url_title, tweets):
        listener.read_data(item)
    listener.on_close()


class FilterStream:
    _closed = mp.Event()
    _is_running = mp.Event()

    def __init__(self, auth, stream_listener):
        self.stream_listener = stream_listener
        self.auth = auth
        self.fn = None

    def is_running(self):
        return self._is_running.is_set()

    # streams the data and writes to a temporary file
    def _stream_geo_data(self):
        _logger.debug('streaming geo data')
        session = requests.Session()
        # filter for tweets with geo-location data only
        geo_filter = [('locations', [-180, -90, 180, 90])]
        response = session.request(method='POST',
                                   url=config.API_URLS['stream_filter'],
                                   data=geo_filter,
                                   stream=True,
                                   auth=self.auth)

        if response.status_code == 200:
            try:
                self.stream_listener.on_open()
                # warning: iter_lines is not re-entrant safe
                for line in response.iter_lines():
                    if self._closed.is_set():
                        return
                    if line:
                        tweet_json = line.decode('utf-8')
                        self.stream_listener.read_data(tweet_json)
            finally:
                # cleanup
                _logger.info('Stopping data collection of twitter stream')
                self.stream_listener.on_close()
                self._is_running.clear()
                self._closed.clear()
                response.close()
        else:
            raise requests.RequestException('There was an error in the request!')

    def stream_async_geo_data(self):
        if self.is_running():
            _logger.warning('Geo data is already streaming! You cannot have more than 1 streamer at a time')
        else:
            _logger.debug('Running the async geo stream')
            self._is_running.set()
            executor = ThreadPoolExecutor(max_workers=1)
            self.fn = executor.submit(self._stream_geo_data)
            executor.shutdown(wait=False)

    def close_stream(self):
        self._closed.set()
        self.fn.result()
