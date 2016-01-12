from flask import Flask, render_template, request, jsonify
import urllib2
import json
import math

def geoMin( coords ):
    totx = 0
    toty = 0
    for coord in coords:
        latdegs = coord[0] * math.pi / 180
        longdegs = coord[1] * math.pi / 180
        x = math.cos(latdegs) * math.cos(longdegs)
        y = math.cos(latdegs) * math.sin(longdegs)
        z = math.sin(latdegs)
        totx += x
        toty += y
    avgx = totx/len(coords)
    avgy = toty/len(coords)
    lon = math.atan(avgy, avgx)
    hyp = math.sqrt(x * x + y * y)
    lat = math.atan2(z, hyp)
    finalcoord = lat, lon
    return finalcoord

def twoPointDist(a, b, unit):
    radEarth = 0
    if unit == "imperial":
        radEarth = 3959
    elif unit == "metric":
        radEarth = 6371
    """
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    basic = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(a[0])+","+str(a[1])+"&destinations="+str(b[0])+","+str(b[1])+"&units="+unit+"&key="+key
    request = urllib2.urlopen(basic)
    result = request.read()
    result = json.loads(result)
    #print result
    distance = result['rows'][0]['elements'][0]['distance']['text']
    distance =  distance.split(" ")[0]
    print distance
    return float(distance)
    """
    aLat = math.radians(a[0])
    aLong = math.radians(a[1])
    bLat = math.radians(b[0])
    bLong = math.radians(b[1])
    latDiff = abs(aLat - bLat)
    lonDiff = abs(aLong - bLong)
    var1 = math.sin(latDiff / 2) ** 2 + math.cos(aLat) * math.cos(bLat) * math.sin(lonDiff / 2) ** 2
    var2 = 2 * math.atan2(math.sqrt(var1), math.sqrt(1 - var1))
    d = radEarth * var2
    print d

"""
Possible Algorithm:
     lat=asin(sin(lat1)*cos(d)+cos(lat1)*sin(d)*cos(tc))
     IF (cos(lat)=0)
        lon=lon1      // endpoint a pole
     ELSE
        lon=mod(lon1-asin(sin(tc)*sin(d)/cos(lat))+pi,2*pi)-pi
     ENDIF
"""
def eightPoints( coord, dist):
    pi = math.pi
    pointArray = []
    lat1 = coord[0]
    lon1 = coord[1]
    directions = [0, pi/4, pi/2, 3*pi/4, pi, 5*pi/4, 3*pi/2, 7*pi/4]
    for i in range(8):
        tc = directions[i]
        lat = asin(sin(lat1)*cos(dist)+cos(lat1)*sin(dist)*cos(tc))
        lon = 0
        if (cos(lat) == 0):
            lon = lon1
        else:
            lon = (lon1-asin(sin(tc)*sin(dist)/cos(lat))+pi)%(2*pi)-pi
        pointArray[i] = (lat, lon)
    return pointArray
            

In Progress:

def findCurrPoint( coords, locations, unit ):
    currentPoint = geoMin( coords )
    minDist = 0
    for coord in coords:
        minDist += twoPointDist(currentPoint, coord, unit )
    for x in range(len(coords)):
        tmpDist = 0
        for y in range(x+1, len(coords)):
            tmpDist += twoPointDist(coords[x], coords[y], unit )
        if tmpDist < minDist:
            minDist = tmpDist
            currentPoint = coords[x]
    return currentPoint


def minDistPoint(currentPoint):
    testDist = 0;
    if unit == "imperial":
        testDist = 6225
    if unit == "metric":
        testDist = 10018
    pointArray = eightPoints(currentPoint, testDist)
    
    

pointa = (40.769750, -73.740648)
pointb = (40.7180139,-74.0160826)
twoPointDist(pointa, pointb, "imperial")
