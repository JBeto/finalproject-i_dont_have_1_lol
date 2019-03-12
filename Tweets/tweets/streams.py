import tweets.config as config
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

import requests
import logging


_logger = logging.getLogger(__name__)


class FilterStream:
    _close = mp.Event()
    _is_running = mp.Event()

    def __init__(self, auth, stream_listener):
        self.auth = auth
        self.stream_listener = stream_listener

    def _stream_geo_data(self):
        session = requests.Session()
        # filter for tweets with geo-location data only
        geo_filter = [('locations', [-180, -90, 180, 90])]
        response = session.request(method='POST',
                                   url=config.API_URLS['stream_filter'],
                                   data=geo_filter,
                                   stream=True,
                                   auth=self.auth)

        if response.status_code == 200:
            self.stream_listener.on_open()
            _logger.info('Beginning data collection of twitter stream')
            try:
                # warning: iter_lines is not re-entrant safe
                for line in response.iter_lines():
                    if self._close.is_set():
                        return
                    if line:
                        decoded_line = line.decode('utf-8')
                        self.stream_listener.read_data(decoded_line)
            finally:
                _logger.info('Stopping data collection of twitter stream')
                self.stream_listener.on_close()
                response.close()
                self._close.clear()
                self._is_running.clear()
        else:
            raise requests.RequestException('There was an error in the request!')

    def stream_async_geo_data(self):
        if self._is_running:
            _logger.warning('Geo data is already streaming! You cannot have more than 1 streamer at a time')
        else:
            self._is_running.set()
            with ProcessPoolExecutor(max_workers=1) as executor:
                executor.submit(self._stream_geo_data)

    def close_stream(self):
        self._close.set()
