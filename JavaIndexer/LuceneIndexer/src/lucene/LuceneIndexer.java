package lucene;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URL;
import java.nio.file.Paths;
import java.text.ParseException;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.RAMDirectory;
import org.apache.lucene.util.Version;
import org.apache.lucene.index.DirectoryReader;

//import java.io.*;
import java.util.ArrayList;

import org.json.*;

public class LuceneIndexer {

    public static void main(String[] args) throws IOException, ParseException {
        ArrayList<JSONObject> jsonlist = new ArrayList<JSONObject>();
        JSONObject obj;

        String line1 = null;

        // Gets path to the tweets datafile
        URL path = LuceneIndexer.class.getResource("tweets.data");
        FileReader fileReader1 = new FileReader(new File(path.getFile()));
        BufferedReader bufferRead = new BufferedReader((fileReader1));

        // Change path to where you want the index to be output
        // This same path should be used for searching
        String indexPath = "<Enter data path to Index data folder>";

        Directory dir = FSDirectory.open(Paths.get(indexPath));

        Analyzer analyzer = new StandardAnalyzer();
        IndexWriterConfig iwc = new IndexWriterConfig(analyzer);

        IndexWriter writer = new IndexWriter(dir, iwc);


        while ((line1 = bufferRead.readLine()) != null) {
            Document doc = new Document();
            //line1 = line1.replace("\\U", "\\\\U");
            //line1 = line1.replace("\\x", "\\\\x");
            System.out.println(line1);
            //System.out.println("\n\n");
            obj = new JSONObject(line1);

            // Tweet Text
            String txt = obj.getString("text");
            //System.out.println(txt);
            doc.add(new TextField("text", txt, Field.Store.YES));

            // User Name
            JSONObject userobj = (JSONObject)obj.get("user");
            String name = userobj.getString("screen_name");
            //System.out.println(name);
            doc.add(new TextField("screen_name", name, Field.Store.YES));

            // Time
            String timeobj = obj.getString("created_at");
            //System.out.println(timeobj);
            doc.add(new TextField("time", timeobj, Field.Store.YES));

            // Location
            JSONObject locobj = (JSONObject)((JSONObject)obj.get("place")).get("bounding_box");
            JSONArray arr = (JSONArray)locobj.get("coordinates");
            if (arr.length() != 0) {
                Object coordobj = arr.get(0);
                //System.out.println(coordobj.toString());
                doc.add(new TextField("coordinates", coordobj.toString(), Field.Store.YES));
            }

            // URL
            /*
            JSONArray urlarr = (JSONArray)((JSONObject)obj.get("entities")).get("urls");
            if (urlarr.length() != 0) {
                JSONObject urlobj = ((JSONObject)urlarr.get(0));
                if (urlobj.has("unwound")) {
                    String urltitle = ((JSONObject)urlobj.get("unwound")).getString("title");
                    System.out.println(urltitle);
                    break;
                }
            }
            */

            writer.addDocument(doc);  // writing new document to the index
        }

        int numIndexed = writer.getDocStats().maxDoc;
        writer.close();
        System.out.println(numIndexed);

        /* SEARCHING CODE
        String queryStr = "Champions";

        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)));
        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser("text", new SimpleAnalyzer());
        try {
            Query query = parser.parse(queryStr);
            TopDocs topdocs = searcher.search(query, 10);
            ScoreDoc[] hits = topdocs.scoreDocs;
            for (int i = 0; i < hits.length; i++) {
                int docId = hits[i].doc;
                Document d = searcher.doc(docId);
                System.out.println(d.get("username"));
                System.out.println(d.get("id"));
                System.out.println(d.get("followers"));
            }
            System.out.println("Found " + hits.length);
        }
        catch (org.apache.lucene.queryparser.classic.ParseException e) {
            System.out.println("ParseException");
        }
        */
    }
}
