from abc import ABC, abstractmethod
from lxml.html import fromstring
import multiprocessing
import requests
import json


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


class URLTitleListener(StreamListener):
    def __init__(self, filename, workers=8):
        self.filename = filename
        self.file = None
        self.queue = multiprocessing.Queue()
        self.pool = multiprocessing.Pool(workers, self._add_url_title)

    def on_open(self):
        self.file = open(self.filename, 'w')
        # self.pool.apply()

    def on_close(self):
        self.file.close()
        self.pool.close()
        self.pool.join()

    def _write_json_data(self, dict_data):
        self.file.write(json.dumps(dict_data))
        self.file.write('\n')

    def _add_url_title(self):
        while True:
            tweet_json = self.queue.get(True)
            tweet_dict = json.loads(tweet_json)

            self._write_json_data(tweet_dict)

    def read_data(self, json_data):
        data = json.loads(json_data)
        if 'created_at' in data and data['place'] is not None:
            self.queue.put(json_data)
