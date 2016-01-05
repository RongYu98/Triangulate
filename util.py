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


