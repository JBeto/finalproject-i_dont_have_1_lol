import tweets.config as config
import tweets.oauth as oauth
import requests
import json


def stream_data(read_data):
    auth = oauth.authenticate()
    session = requests.Session()

    response = session.request(method='POST',
                               url=config.API_URLS['stream_sample'],
                               stream=True,
                               auth=auth)

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                read_data(json.loads(decoded_line))
    else:
        raise requests.RequestException('There was an error in the request!')
