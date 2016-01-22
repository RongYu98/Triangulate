from flask import Flask, render_template, request, jsonify
import urllib2
import json

def numTo(lat, long):
    #lat = 40.714224
    #long = -73.961452
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    basic = """https://maps.googleapis.com/maps/api/geocode/json?latlng="""+str(lat)+","+str(long)+"""&key=""" + key
    print basic
    request = urllib2.urlopen(basic)
    result = request.read()
    result = json.loads(result)

    dict = {}
    if (result["status"] != "OK"):
        dict["ERROR"] = result["status"]
    else:
        lat = result["results"][0]["geometry"]["location"]["lat"]
        lng = result["results"][0]["geometry"]["location"]["lng"]
        full_address = result["results"][0]["formatted_address"]
        dict["lat"] = lat
        dict["long"] = lng
        dict["add"] = full_address
        dict["ERROR"] = "NO"
    #return jsonify(result)
    return dict



def nameTo(add):
    #add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    add = add.replace(" ","+")
    print add
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    query = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (add, key)
    print query

    #%s&go=&qs=n&sk=&sc=8-13&first=%s' % (quoted_query, page)

    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)

    dict = {}
    if (result["status"] != "OK"):
        dict["ERROR"] = result["status"]
    else:
        lat = result["results"][0]["geometry"]["location"]["lat"]
        lng = result["results"][0]["geometry"]["location"]["lng"]
        full_address = result["results"][0]["formatted_address"]
        dict["lat"] = lat
        dict["long"] = lng
        dict["add"] = full_address
        dict["ERROR"] = "NO"
    #return jsonify(result)
    return dict
    

def randStuff():
    #lat = result["results"][0]["geometry"]["location"]["lat"]
    #lng = result["results"][0]["geometry"]["location"]["lng"]
    #full_address = result["results"][0]["formatted_address"]
    pass


def getInfo(query): #currently not in used #unfixed
    #this will return a dict of 'loc = "Latitude: "+str(lat)+" Longitude: "+str(long), lat = stuff["lat"], lng = stuff["long"], add = stuff["add"]'
    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)
    lat = result["results"][0]["geometry"]["location"]["lat"]
    lng = result["results"][0]["geometry"]["location"]["lng"]
    full_address = result["results"][0]["formatted_address"]
    dict = {}
    dict["lat"] = lat
    dict["long"] = lng
    dict["add"] = full_address
    return dict

def nearHere(longi, lat):
    #note, some places WILL NOT WORK
    longi = str(longi)
    lat = str(lat)
    #query = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?address=%s&radius=500&types=food&name=cruise&key=%s" % (add, key)
    #query = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location="+lat+","+longi+"&radius=5000&types=food|cafe&keyword=vegetarian&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    query = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location="+lat+","+longi+"&radius=500&types=food|cafe&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    print query
    #print "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ"
    #print
    print "Lat: "+str(lat)
    print "long: "+str(longi)
    #print "Reached here----------"
    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)
    #print result
    dic={}
    if result["status"]!="OK":
        dic["ERROR"] = result["status"]
        return dic
    else:
        dic["ERROR"] = "NO"
    i = 0
    l = []
    while (i<5):
        #print jsonify(result)
        #return jsonify(result)
        try:
            placeID = result["results"][i]["place_id"]
            print placeID
            l.append(placeID)
        except:
            print "No more results"
        i= i+1
    i = 0
    while (i<5):
        try:
            dic[i] = byPlaceID(l[i])
        except:
            print "No more results"
        #make this a dic instead
        #print l[i]
        i = i+1
        #print result

    #print dic
    return dic
def byPlaceID(ID):
    query = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+ID+"&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    #https://developers.google.com/places/place-id

    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)
    #print result

    full_address = result["result"]["formatted_address"]
    #dict = {}
    #dict["add"] = full_address
    return full_address

    #return result

#*******~USER FUNCTIONS~*******#
import random
from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import md5 

def add(filename, username, content, NUMID):
        conn = MongoClient()
        c = conn["main"]
        q = {'user':username, 'content':content, 'NUMID':NUMID}
        c[filename].insert(q)

def register(uname,pword):
    m=md5.new()
    m.update(pword)
    f = open("database/users.txt", 'r')
    for line in f.readlines():
        if uname == line.split(',')[0]:
            return False
    f.close()
    f = open("database/users.txt",'a')
    f.write("%(user)s,%(phash)s\n"%({"user":uname,"phash":m.hexdigest()}))
    f.close()
    return True
    
def authenticate(uname, pword):
    m = md5.new()
    m.update(pword)
    f = open("database/users.txt",'r')
    for line in f.readlines():
        if uname == line.split(',')[0] and m.hexdigest() == line.split(',')[1].strip():
            f.close()
            return True
    f.close()
    return False

def getposts(title):
    conn = MongoClient()
    c = conn["main"]
    info = c[title].find()
    return info

def gettitles():
    conn = MongoClient()
    c = conn["main"]
    titles = []
    B = c.collection_names(False)
    for f in B:
        titles.append(f)
    return titles


if __name__=='__main__':
    lat = 40.714224
    long = -73.961452
    #key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    #basic = """https://maps.googleapis.com/maps/api/geocode/json?latlng="""+str(lat)+","+str(long)+"""&key=""" + key

    #add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    #basic = """https://maps.googleapis.com/maps/api/geocode/json?address="""+add+"""&key="""+key
    #print basic
    #request = urllib2.urlopen(basic)
    #result = request.read()
    #result = json.loads(result)
    #lat = result["results"][0]["geometry"]["location"]["lat"]
    #lng = result["results"][0]["geometry"]["location"]["lng"]
    #print result["results"][0]["address_components"]
    #return jsonify(result["results"][0])
    #nearHere(-73.961452,40.714224)
    #nearHere(-73.7815126,42.3903615) 
    print(nameTo("100-11 Metropolitan Ave, Forest Hills, NY 11375, United States"))
