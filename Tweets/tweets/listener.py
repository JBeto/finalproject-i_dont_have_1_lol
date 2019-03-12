from abc import ABC, abstractmethod
import logging
import sys


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
        self.filename = filename
        self.file = None

    def on_open(self):
        self.file = open(self.filename, 'w')
        _logger.debug('Opening the output file')

    def on_close(self):
        self.file.close()
        _logger.debug('Closing the output file')

    def read_data(self, json_data):
        self.file.write(json_data)
        self.file.write('\n')


class ListStream(StreamListener):
    def __init__(self):
        self.data = []

    def on_open(self):
        _logger.debug('Writing to the list')

    def on_close(self):
        _logger.debug('End write to list')

    def read_data(self, json_data):
        self.data.append(json_data)

    def byte_size(self):
        return sys.getsizeof(self.data)
