from abc import ABC, abstractmethod
import logging


_logger = logging.getLogger(__name__)


class StreamListener(ABC):
    @abstractmethod
    def on_open(self):
        pass

    @abstractmethod
    def on_close(self):
        pass

    @abstractmethod
    def read_data(self, json_data):
        pass


class FileStream(StreamListener):
    def __init__(self, filename):
        self._filename = filename
        self._file = None
        self.tweets_gathered = 0

    def on_open(self):
        self._file = open(self._filename, 'w')
        _logger.debug('Opening the output file')

    def on_close(self):
        self._file.close()
        _logger.debug('Closing the output file')

    def read_data(self, json_data):
        self._file.write(json_data)
        self._file.write('\n')
        self.tweets_gathered += 1
