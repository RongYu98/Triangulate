from flask import Flask, render_template, request, jsonify
import urllib2
import json
import util

def numTo(lat, long):
    #lat = 40.714224
    #long = -73.961452
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    basic = """https://maps.googleapis.com/maps/api/geocode/json?latlng="""+str(lat)+","+str(long)+"""&key=""" + key
    
    request = urllib2.urlopen(basic)
    result = request.read()
    result = json.loads(result)

    lat = result["results"][0]["geometry"]["location"]["lat"]
    lng = result["results"][0]["geometry"]["location"]["lng"]
    full_address = result["results"][0]["formatted_address"]
    dict = {}
    dict["lat"] = lat
    dict["long"] = lng
    dict["add"] = full_address
    #return jsonify(result)
    return dict



def nameTo(add):
    #add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    add = add.replace(" ","+")
    print add
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    query = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (add, key)


    #%s&go=&qs=n&sk=&sc=8-13&first=%s' % (quoted_query, page)

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
    #return jsonify(result)
    return dict
    

def randStuff():
    #lat = result["results"][0]["geometry"]["location"]["lat"]
    #lng = result["results"][0]["geometry"]["location"]["lng"]
    #full_address = result["results"][0]["formatted_address"]
    pass


def getInfo(query): #currently not in used
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
    longi = str(longi)
    lat = str(lat)
    #query = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?address=%s&radius=500&types=food&name=cruise&key=%s" % (add, key)
    query = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location="+longi+","+lat+"&radius=5000&types=food|cafe&keyword=vegetarian&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)
    i = 0
    l = []
    while (i<5):
        return jsonify(result)
        placeID = result["results"][i]["place_id"]
        i= i+1
        l.append(placeID)
    i = 0
    dic={}
    while (i<5):
        dic[i] = byPlaceID(l[i])
        #make this a dic instead
        print l[i]
        i = i+1
        #print result
    return dic
def byPlaceID(ID):
    query = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+ID+"&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    #https://developers.google.com/places/place-id

    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)
    
    #lat = result["results"][0]["geometry"]["location"]["lat"]
    #lng = result["results"][0]["geometry"]["location"]["lng"]
    full_address = result["result"]["formatted_address"]
    #dict = {}
    #dict["add"] = full_address
    return full_address

    #return result




if __name__=='__main__':
    lat = 40.714224
    long = -73.961452
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    #basic = """https://maps.googleapis.com/maps/api/geocode/json?latlng="""+str(lat)+","+str(long)+"""&key=""" + key

    add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    basic = """https://maps.googleapis.com/maps/api/geocode/json?address="""+add+"""&key="""+key
    print basic
    request = urllib2.urlopen(basic)
    result = request.read()
    result = json.loads(result)
    #lat = result["results"][0]["geometry"]["location"]["lat"]
    #lng = result["results"][0]["geometry"]["location"]["lng"]
    print result["results"][0]["address_components"]
    #return jsonify(result["results"][0])
