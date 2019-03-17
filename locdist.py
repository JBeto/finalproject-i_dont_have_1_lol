from math import sin, cos, sqrt, atan2, radians

def calcBBoxCenter(topleft, botright):
    tlx = topleft[0]
    tly = topleft[1]
    brx = botright[0]
    bry = botright[1]

    return [((brx + tlx) / 2), ((bry + tly) / 2) ]

def calcDist(tweetLoc, currLoc):
    R = 6373.0

    twtlat = radians(tweetLoc[1])
    twtlon = radians(tweetLoc[0])
    currlat = radians(currLoc[1])
    currlon = radians(currLoc[0])

    londist = currlon - twtlon
    latdist = currlat - twtlat

    a = sin(latdist / 2)**2 + cos(twtlat) * cos(currlat) * sin(londist / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return (distance)

#bbox = [[124.445405,8.231283],[124.445405,8.520874],[124.811596,8.520874],[124.811596,8.231283]]
# Longitude, Latitude
bbox = [ [-105.301758, 39.964069],
           [-105.301758, 40.094551],
           [-105.178142, 40.094551],
           [-105.178142, 39.964069]]
topleft = bbox[1]
bottomright = bbox[3]
twtcoord = calcBBoxCenter(topleft, bottomright)

currlat = 40.0150
currlong = -105.2705
currcoord = [currlat, currlong]
#Kansas: 39.0119° N, 98.4842° W
#Riverside: 33.9806° N, 117.3755° W
#Boulder: 40.0150° N, 105.2705° W

dist = calcDist(twtcoord, currcoord)

print (dist, " km")
