# Twitter Geolocations

##### Team Members: Ed Zabrensky, Siddharth Menon, Joshua Beto

## Description

Our project uses the Twitter Streaming API to collect geolocated tweets. Using these tweets, we build indices based on location, name, and url titles included in the Tweet. We display these results using the Google Maps API, and can limit the number of results shown.

## Twitter Stream

### Requirements
* Python 3.6
* Bash


### Quick-Start

* Navigate to the `Tweets` directory
* Run `./install.sh` to install the Python dependencies in a virtual environment called `venv`
* Run `./scraper.sh <CONSUMER_KEY> <CONSUMER_SECRET> <ACCESS_TOKEN> <ACCESS_SECRET>`
* The output should be the following files: `tweets.data` and `tweets_url.data`

CONSUMER_KEY = Twitter API Consumer Key \
CONSUMER_SECRET = Twitter API Consumer Secret \
ACCESS_TOKEN = Twitter API Access Token \
ACCESS_SECRET = Twitter API Access Token Secret

You can retrieve these keys by first making a Twitter development account and creating an app. The process is documented here: https://developer.twitter.com/en/docs/basics/developer-portal/overview

## Lucene Index / Geolocation Extension

### Requirements
* JVM
* Java 8.0
* Bash


### Quick-Start

