//package lucene;

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
import org.python.core.*;

//import java.io.*;
import java.util.ArrayList;

import org.json.*;

public class LuceneIndexer {
    public static PyString doc = new PyString("Simple Jython!!!");
        // Change path to where you want the index to be output
        // This same path should be used for searching
    public static String indexPath = "/home/ezabr001/finalproject-i_dont_have_1_lol/JavaIndexer/LuceneIndexer/src/lucene/final_index";
    public LuceneIndexer()
    {

    } 
    public static PyList search(String query1) throws IOException {
        String queryStr = query1;

        IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)));
        IndexSearcher searcher = new IndexSearcher(reader);
        QueryParser parser = new QueryParser("text", new SimpleAnalyzer());
        PyList results = new PyList();
        try {
            Query query = parser.parse(queryStr);
            TopDocs topdocs = searcher.search(query, 20);
            ScoreDoc[] hits = topdocs.scoreDocs;
            for (int i = 0; i < hits.length; i++) {
                int docId = hits[i].doc;
                Document d = searcher.doc(docId);
                PyList currResults = new PyList();
                if(d.get("screen_name") != "") {
                    PyUnicode tmp = new PyUnicode(d.get("screen_name"));
                    currResults.append(tmp);// tmp.add(new PyString(d.get("username")));
                    //System.out.println(d.get("screen_name"));
                }
                if(d.get("text") != ""){
                    PyUnicode tmp = new PyUnicode(d.get("text"));// tmp.add (new PyString(d.get("id")));
                    currResults.append(tmp);
                }
                if(d.get("coordinates") != "")
                    currResults.append(new PyString(d.get("coordinates")));// tmp.add(new PyString(d.get("coordinates")));

                if(d.get("url_title") != ""){
                    PyUnicode tmp = new PyUnicode(d.get("url_title"));
                    currResults.append(tmp);
                }

                results.append(currResults);
                // System.out.println(d.get("screen_name"));
                // System.out.println(d.get("id"));
                // System.out.println(d.get("followers"));
            }
            System.out.println("Found " + hits.length);
        }
        catch (org.apache.lucene.queryparser.classic.ParseException e) {
            System.out.println("ParseException");
        }
        return results;
    }
    public static void main(String[] args) throws IOException, ParseException {
        ArrayList<JSONObject> jsonlist = new ArrayList<JSONObject>();
        JSONObject obj;

        String line1 = null;

        // Gets path to the tweets datafile
        URL path = LuceneIndexer.class.getResource("final.data");
        FileReader fileReader1 = new FileReader(new File(path.getFile()));
        BufferedReader bufferRead = new BufferedReader((fileReader1));


        Directory dir = FSDirectory.open(Paths.get(indexPath));

        Analyzer analyzer = new StandardAnalyzer();
        IndexWriterConfig iwc = new IndexWriterConfig(analyzer);

        IndexWriter writer = new IndexWriter(dir, iwc);


        while ((line1 = bufferRead.readLine()) != null) {
            Document doc = new Document();
            //line1 = line1.replace("\\U", "\\\\U");
            //line1 = line1.replace("\\x", "\\\\x");
            //System.out.println(line1);
            //System.out.println("\n\n");
            obj = new JSONObject(line1);

            // Tweet Text
            if(obj.has("text") && !obj.isNull("text")){
                String txt = obj.getString("text");
                //System.out.println(txt);
                // PyUnicode tmp = new PyUnicode(txt);
                doc.add(new TextField("text", txt, Field.Store.YES));
            }
            else {
                continue;
                // String tmp = "";
                // doc.add(new TextField("text", tmp, Field.Store.YES));
            }

            // User Name
            // if(obj.has("user") && !obj.isNull("user")){
                JSONObject userobj = (JSONObject)obj.get("user");
                String name = userobj.getString("screen_name");
                //System.out.println(name);
                doc.add(new TextField("screen_name", name, Field.Store.YES));
            // }
            // else {
            //     String tmp = "";
            //     doc.add(new TextField("screen_name", tmp, Field.Store.YES));
            // }

            // // Time
            // if(obj.has("created_at") && !obj.isNull("created_at")){
                String timeobj = obj.getString("created_at");
                //System.out.println(timeobj);
                doc.add(new TextField("time", timeobj, Field.Store.YES));
            //}
            // else {
            //     String tmp = "";
            //     doc.add(new TextField("time", tmp, Field.Store.YES));
            // }

            if(obj.has("url_title") && !obj.isNull("url_title")){
                //JSONObject urlobj1 = (JSONObject)obj.get("url_title");
                String urlobj = obj.getString("url_title");
                doc.add(new TextField("url_title", urlobj, Field.Store.YES));
            }
            else {
                String tmp = "";
                doc.add(new TextField("url_title", tmp, Field.Store.YES));
            }

            if(obj.has("place") && !obj.isNull("place")){
                // Location
                JSONObject locobj = (JSONObject)((JSONObject)obj.get("place")).get("bounding_box");
                JSONArray arr = (JSONArray)locobj.get("coordinates");
                if (arr.length() != 0) {
                    Object coordobj = arr.get(0);
                    //System.out.println(coordobj.toString());
                    doc.add(new TextField("coordinates", coordobj.toString(), Field.Store.YES));
                }
            }
            else {
                continue;
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

        //SEARCHING CODE
        // String queryStr = "Champions";

        // IndexReader reader = DirectoryReader.open(FSDirectory.open(Paths.get(indexPath)));
        // IndexSearcher searcher = new IndexSearcher(reader);
        // QueryParser parser = new QueryParser("text", new SimpleAnalyzer());
        // try {
        //     Query query = parser.parse(queryStr);
        //     TopDocs topdocs = searcher.search(query, 10);
        //     ScoreDoc[] hits = topdocs.scoreDocs;
        //     for (int i = 0; i < hits.length; i++) {
        //         int docId = hits[i].doc;
        //         Document d = searcher.doc(docId);
        //         System.out.println(d.get("screen_name"));
        //         System.out.println(d.get("id"));
        //         System.out.println(d.get("followers"));
        //     }
        //     System.out.println("Found " + hits.length);
        // }
        // catch (org.apache.lucene.queryparser.classic.ParseException e) {
        //     System.out.println("ParseException");
        // }
        
    }
}
