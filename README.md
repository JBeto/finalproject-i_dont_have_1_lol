# Twitter Geolocations

##### Team Members: Ed Zabrensky, Siddharth Menon, Joshua Beto

## Description

Our project uses the Twitter Streaming API to collect geolocated tweets. Using these tweets, we build indices based on location, name, and url titles included in the Tweet. We display these results using the Google Maps API, and can limit the number of results shown.

## What's Included?

* The tweet data is included in the form of a zip file on Google Docs: https://drive.google.com/open?id=1mgS_NXTQot8IfSjySKdXW5dIyH-T--na

* The source files for the Tweet Stream are included in the `tweets` folder under `Tweets` while the Lucene Index / Geolocations are included in the `src` folder under `Queries`.

## Overall Architecture
The overall architecture is split up into 3 components:
* Python for the Tweet Stream
* Java for Lucene Indexing
* Jython for the Geolocation extension


## Twitter Stream

### Requirements
* Python 3.6
* Pip installed for Python 3.6
* Bash


### Quick-Start

* Navigate to the `Tweets` directory
* Run `./install.sh` to install the Python dependencies in a virtual environment called `venv`
* Alternatively, you can create and activate the virtual environment manually through the `virtualenv` package and install the dependencies with:  `pip install -r requirements.txt`
* Run `./crawler.sh <CONSUMER_KEY> <CONSUMER_SECRET> <ACCESS_TOKEN> <ACCESS_SECRET>`
* The output should be the following files: `tweets.data` and `tweets_url.data`

CONSUMER_KEY = Twitter API Consumer Key \
CONSUMER_SECRET = Twitter API Consumer Secret \
ACCESS_TOKEN = Twitter API Access Token \
ACCESS_SECRET = Twitter API Access Token Secret

You can retrieve these keys by first making a Twitter development account and creating an app. The process is documented here: https://developer.twitter.com/en/docs/basics/developer-portal/overview

### Architecture
The architecture is split into a few basic modules. Their functionalities are listed below:

`streams` module: Handles any logic that deals with the Twitter Stream API (Connection, Reconnecting, Tweets, etc.). This module also adds the `url_title` field to the Tweet JSON through the map_urls function

`listener` module: Callback that the streams module calls on when the data is collected. This module allows us to record the number of Tweets streamed and writes the data to its corresponding file.

`config` module: Handles any configuration data including the Twitter API keys, endpoints, and output file names.

`oauth` module: Handles any oauth authentication. This module is used by the streams module to connect to the Twitter endpoints.

`app` module: Handles our main logic and calls our `streams` module. This module uses user input to determine when to stop streaming.

* Removing duplicates is handled after the fact with a `check.py` script that adds each Tweet JSON to a `set` and writes to the final output file: `tweets_url_no_dup.data`

## Lucene Index / Geolocation Extension

### Requirements
* JVM
* Java 8.0
* Bash
* Lucene Core (from http://lucene.apache.org/core/)
* org.json library (https://github.com/stleary/JSON-java)


### Quick-Start
Make sure lucene 7.7.1 is downloaded and extracted (from http://lucene.apache.org/core/)
The .jar files we will need are:
* lucene-analyzers-common-7.7.1.jar
* lucene-core-7.7.1.jar
* lucene-demo-7.7.1.jar
* lucene-queryparser-7.7.1.jar

Make sure the json library .jar file is downloaded (download .jar file from https://github.com/stleary/JSON-java)

If required, setup the environment in IntelliJ:
	Go to File -> Project Structure
	Under Modules, set Module SDK to Java 11
		Click the + button, and "add JARs or directories".
		Add the previously downloaded .jar files

* Copy tweets data file to the same folder as LuceneIndexer.java

* Change indexPath in LuceneIndexer.java to desired path to where you want the index to be stored

### Architecture
Running LuceneIndexer.java with the above settings and data files, will create an index that will be stored where indexPath is set. 

## Flask Front end Creating Lucene Index.

### Requirements
* JVM
* Java 8.0
* Lucene core
* Flask
* Flask_google maps (https://github.com/rochacbruno/Flask-GoogleMaps)
* Jython 2.7.1
* org.python.core

### Quick-start
Navigate to the Frontend directory. In Map.py edit the google maps API key to your own API key.
To compile the LuceneIndexer.java in the JavaIndexer/LuceneIndexer/src/lucene we need to compile it with the correct classpaths.
To compile LuceneIndexer:
javac LuceneIndexer.java -cp /path to lucene7.7.1/lucene-7.7.1/core/lucene-core-7.7.1.jar:/path to lucene7.7.1/lucene-7.7.1/queryparser/lucene-queryparser-7.7.1.jar:/path to lucene7.7.1/lucene-7.7.1/analysis/common/lucene-analyzers-common-7.7.1.jar:/path to lucene7.7.1/lucene-7.7.1/demo/lucene-demo-7.7.1.jar:/path to JSON-java/JSON-java/json-20180813.jar:/path to jython/jython.jar  

(optional) Once we have Lucene Indexer compiled we can create the indexer using this. However since a final_indexer is already in the repo this step isnt necessary.
java -cp /path to lucene7.7.1/lucene-7.7.1/core/lucene-core-7.7.1.jar:/path to lucene7.7.1/lucene-7.7.1/queryparser/lucene-queryparser-7.7.1.jar:/path to lucene7.7.1/lucene-7.7.1/analysis/common/lucene-analyzers-common-7.7.1.jar:/path to lucene7.7.1/lucene-7.7.1/demo/lucene-demo-7.7.1.jar:/path to JSON-java/JSON-java/json-20180813.jar:/path to jython/jython.jar:. LuceneIndexer    

This will create an indexer with the indexer name specified in LuceneIndexer.java.

The next step is to run the map.py script from the LuceneIndexer.java directory:
jython /Frontend/map.py


### Architecture
In the Frontend folder there is a map.py script that runs the webserver and a folder called templates.
In templates it contains our html file that gives us the design for the page and also contains the code for getting the query to the map.py script and also gathers the user's browser location.


