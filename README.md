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
javac LuceneIndexer.java -cp /<path to lucene7.7.1>/lucene-7.7.1/core/lucene-core-7.7.1.jar:/<path to lucene7.7.1>/lucene-7.7.1/queryparser/lucene-queryparser-7.7.1.jar:/<path to lucene7.7.1>/lucene-7.7.1/analysis/common/lucene-analyzers-common-7.7.1.jar:/<path to lucene7.7.1>/lucene-7.7.1/demo/lucene-demo-7.7.1.jar:/<path to JSON-java>JSON-java/json-20180813.jar:/<path to jython>/jython.jar  

(optional) Once we have Lucene Indexer compiled we can create the indexer using this. However since a final_indexer is already in the repo this step isnt necessary.
java -cp /<path to lucene7.7.1>/lucene-7.7.1/core/lucene-core-7.7.1.jar:/<path to lucene7.7.1>/lucene-7.7.1/queryparser/lucene-queryparser-7.7.1.jar:/<path to lucene7.7.1>/lucene-7.7.1/analysis/common/lucene-analyzers-common-7.7.1.jar:/<path to lucene7.7.1>/lucene-7.7.1/demo/lucene-demo-7.7.1.jar:/<path to JSON-java>JSON-java/json-20180813.jar:/<path to jython>/jython.jar:. LuceneIndexer    

This will create an indexer with the indexer name specified in LuceneIndexer.java.

The next step is to run the map.py script from the LuceneIndexer.java directory:
jython /Frontend/map.py


### Architecture
In the Frontend folder there is a map.py script that runs the webserver and a folder called templates.
In templates it contains our html file that gives us the design for the page.  

