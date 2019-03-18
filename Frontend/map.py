import LuceneIndexer
import sys
from flask import Flask, render_template, request, redirect
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from math import sin, cos, sqrt, atan2, radians

reload(sys)
sys.setdefaultencoding('UTF8')
app = Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD'] = True

GoogleMaps(app, key="AIzaSyDkiY8lH2q-OxrAGJuuZ_bc4v6bqTtiK1Q")

mymap = Map(
     identifier="view-side",
     lat=37.4419,
     lng=-122.1419,
     markers=[(37.4419, -122.1419)]
  )
sndmap = Map(
   identifier="sndmap",
   lat=37.4419,
   lng=37.4419,
   style="height:500px;width:800px;margin:0;",
   #style="height:500px;width:800px;margin:0;",
   #lat=request.form['lat'],
   #lng=request.form['lng'],
   markers=[
   {
     'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
     'lat': 37.4419,
     'lng': -122.1419,
     'infobox': "<b>EZHello World</b>"
  },
  {
     'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
     'lat': 37.4300,
     'lng': -122.1400,
     'infobox': "<b>Hello World from other place</b>"
  }
  ]
  )


def calcBBoxCenter(topleft, botright):
    tlx = topleft[0]
    tly = topleft[1]
    brx = botright[0]
    bry = botright[1]

    return [((brx + tlx) / 2), ((bry + tly) / 2) ]

def calcDist(tweetLoc, currLoc):
    R = 6373.0

    twtlat = radians(float(tweetLoc[1]))
    twtlon = radians(float(tweetLoc[0]))
    currlat = radians(float(currLoc[1]))
    currlon = radians(float(currLoc[0]))

    londist = currlon - twtlon
    latdist = currlat - twtlat

    a = sin(latdist / 2)**2 + cos(twtlat) * cos(currlat) * sin(londist / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return (distance)

@app.route('/', methods = ['POST', 'GET'])
def mapview():
  global mymap
  global sndmap
  if request.method == 'POST':
    indxr = LuceneIndexer()
    print (indxr.doc)
    results = indxr.search(request.form.get('query'))
    curr_loc = [request.form.get('lng'),request.form.get('lat')]

    result_markers = []
    for result in results:
      name = unicode(result[0], 'unicode-escape')
      text = unicode(result[1], 'unicode-escape')
      bbox = eval(result[2])
      center = calcBBoxCenter(bbox[1], bbox[3])
      url_title = result[3]
      tmp_dict = {}
      tmp_dict['icon'] = 'http://maps.google.com/mapfiles/ms/micons/purple-pushpin.png'
      tmp_dict['lat'] = center[1]
      tmp_dict['lng'] = center[0]
      tmp_dict['infobox'] = "<h4>" + name + "</h4>" + text + "<h6>" + url_title + "</h6>"
      if(calcDist(center, curr_loc) < 500000):
        result_markers.append(tmp_dict)
      # print ("About to print evaluated coord!")
      # print (coord[3])

    print("Made it here! About to update map.")
    sndmap = Map(
       identifier="sndmap",
       lat=request.form.get('lat'),
       lng=request.form.get('lng'),
       style="height:500px;width:800px;margin:0;",
       zoom=5,
       markers=result_markers
      #  [
      #  {
      #    'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
      #    'lat': 37.441,
      #    'lng': 37.441,
      #    'infobox': "<b>EZHello1232 World</b>"
      # },
      # {
      #    'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
      #    'lat': 37.4300,
      #    'lng': -122.1400,
      #    'infobox': "<b>Hello World from other place</b>"
      # }
      # ]
      )
  return render_template('example.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
     app.run(debug=True)
