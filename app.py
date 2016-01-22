from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import urllib2
import json
import util

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def main():
    lat = 40.714224
    long = -73.961452
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    basic = """https://maps.googleapis.com/maps/api/geocode/json?latlng="""+str(lat)+","+str(long)+"""&key=""" + key
    
    request = urllib2.urlopen(basic)
    result = request.read()
    result = json.loads(result)
    #lat = result["results"][0]["geometry"]["location"]["lat"]
    #lng = result["results"][0]["geometry"]["location"]["lng"]
    print result["results"][0]
    return jsonify(result["results"][0])
    #return jsonify(result)

@app.route("/name")
def nameToNumbers():
    add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    query = "https://www.maps.googleapis.com/maps/api/geocode/json?address="+add+"&key="+key
    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)
    return jsonify(result)

@app.route("/test",methods=["GET","POST"])
def test():
    if request.method == "GET":
        return render_template("test.html")
    else:
        #request.method == "GET":
        if request.form["submit"] == "Find By Name":
            query = request.form["place"]
            #print(request.form["place"])
            stuff = util.nameTo(query)
            if (stuff["ERROR"] != "NO"):
                return render_template("test.html", error = stuff["ERROR"])
            print ("lat: "+str(stuff["lat"])+"  long: "+str(stuff["long"]))
            dictio = {}
            dictio = util.nearHere(stuff["long"], stuff["lat"])
            if dictio["ERROR"] == "NO":
                dictio.pop("ERROR", None)
            else:
                string = dictio["ERROR"]
                dictio.pop("ERROR", None)
                dictio[-1] = string
            #return result
            return render_template("test.html", loc = query, lat = stuff["lat"], lng = stuff["long"], add = stuff["add"], result = dictio)
        elif request.form["submit"] == "Find On Map":
            lat = request.form["lat"]
            long = request.form["long"]
            print (long + "----" + lat)
            stuff = util.numTo( lat, long )
            if (stuff["ERROR"] != "NO"):
                return render_template("test.html", error = stuff["ERROR"])
            return render_template("map.html", lati = stuff["lat"], longi = stuff["long"])
        else:
            lat = request.form["lat"]
            long = request.form["long"]
            print (long + "----" + lat)
            stuff = util.numTo( lat, long )
            if (stuff["ERROR"] != "NO"):
                return render_template("test.html", error = stuff["ERROR"])
            dictio = util.nearHere(long, lat)
            if dictio["ERROR"] == "NO":
                dictio.pop("ERROR", None)
            else:
                err = dictio["ERROR"]
                dictio.pop("ERROR", None)
                dictio[-1] = err
            return render_template("test.html", loc = "Latitude: "+str(lat)+" Longitude: "+str(long), lat = stuff["lat"], lng = stuff["long"], add = stuff["add"], result = dictio )


@app.route("/maps",methods=["GET","POST"]) #will currently only apply to the second box
def maps():
    if request.method == "GET":
        return render_template("test.html")
    else:
        if request.form["submit"] == "Find By Name":
            query = request.form["place"]
            stuff = util.nameTo(query)
            if (stuff["ERROR"] != "NO"):
                return render_template("test.html", error = stuff["ERROR"])
            print ("lat: "+str(stuff["lat"])+"  long: "+str(stuff["long"]))
            dictio = {}
            dictio = util.nearHere(stuff["long"], stuff["lat"])
            if dictio["ERROR"] == "NO":
                dictio.pop("ERROR", None)
            else:
                string = dictio["ERROR"]
                dictio.pop("ERROR", None)
                dictio[-1] = string
            return render_template("test.html", loc = query, lat = stuff["lat"], lng = stuff["long"], add = stuff["add"], result = dictio)
        ####################################
        elif request.form["submit"] == "Find On Map":
            lat = request.form["lat"]
            long = request.form["long"]
            stuff = util.numTo( lat, long )
            print(stuff)
            if (stuff["ERROR"] != "NO"):
                return render_template("test.html", error = stuff["ERROR"])
            base = [stuff["add"], stuff["lat"], stuff["long"]]

            dictio = {}
            dictio = util.nearHere(stuff["long"], stuff["lat"])
            if dictio["ERROR"] == "NO":
                dictio.pop("ERROR", None)
            #dictio should now haev a list of five places by name

            lis = []
            i = 0
            while (i<5):
                try:
                    print (dictio[i])
                    placeinfo = nameTo(dictio[i]);
                    print placeinfo
                    print "________________________"
                    lis.append([ placeinfo["add"], placeinfo["lat"], placeinfo["long"]])
                    #lis[i][0] = placeinfo["add"]
                    #lis[i][1] = placeinfo["lat"]
                    #lis[i][2] = placeinfo["long"]
                except:
                    print "No more results"
                i+=1
            print lis
            return render_template("map3.html", base = base, places = lis)
            return render_template("map.html",  base = base)
        else:
            lat = request.form["lat"]
            long = request.form["long"]
            print (long + "----" + lat)
            stuff = util.numTo( lat, long )
            if (stuff["ERROR"] != "NO"):
                return render_template("test.html", error = stuff["ERROR"])
            dictio = util.nearHere(long, lat)
            if dictio["ERROR"] == "NO":
                dictio.pop("ERROR", None)
            else:
                err = dictio["ERROR"]
                dictio.pop("ERROR", None)
                dictio[-1] = err
            return render_template("test.html", loc = "Latitude: "+str(lat)+" Longitude: "+str(long), lat = stuff["lat"], lng = stuff["long"], add = stuff["add"], result = dictio )
    
    return render_template("maps.htm", places = stuffs, base = itself)
    #my_list should be a [][], the [] should be numbered, a seperate one for each place. [][0] == name, [][1] == lat, [][2] == long, base should be about itself.
        
@app.route("/tests")
def nearHere():
    add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    
    query = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location=48.859294,2.347589&radius=5000&types=food|cafe&keyword=vegetarian&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    #query = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location=48859294,2347589&radius=5000&types=food|cafe&keyword=vegetarian&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)

    ##
    return result["status"]
    return jsonify(results)

    ###################################
    
    i = 0
    l = []
    #print result
    while (i<5):
        placeID = result["results"][i]["place_id"]
        i= i+1
        l.append(placeID)

    #print result
    #print l

    #return jsonify(l)
    i = 0
    dic = {}
    while (i<5):
        query = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+l[i]+"&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
        request = urllib2.urlopen(query)
        result = request.read()
        result = json.loads(result)
        #return result["result"]["formatted_address"]
        #print result["result"]["formatted_address"]
        dic[i] = result["result"]["formatted_address"]
        i+=1

    return jsonify(dic)
    #this one is different from the others
    return jsonify(result)
    #return jsonify(util.byPlaceID(l[0]))

#*******~USER FUNCTIONS~*******#

def verify():
    if 'log' in session:
        return session['log'] == 'verified'
    else:
        session['log'] = 'unverified'
        return False

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if verify():
        return redirect(url_for('home'))
    if request.method == "POST":
        form = request.form
        button = form['button']
        if button == "Register":
            return redirect(url_for("register"))
        else:
            uname = form['username']
            session['username'] = uname
            pword = form['password']
            if util.authenticate(uname,pword):
                session['log'] = 'verified'
                session['username'] = uname
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="Incorrect Username or Password")

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        form = request.form
        uname = form['username']
        pword = form['password']
        button = form['button']
        if button == 'Login':
            return redirect(url_for('login'))
        if util.register(uname,pword):
            session['log'] = 'verified'
            session['username'] = uname
            return redirect(url_for('home'))
        else:
            return render_template('register.html',err="That username is taken!")

@app.route('/home', methods=["GET","POST"])
def home():
    if verify():
        user=''
        if 'username' in session:
            user=session['username']
        else:
            user = session['username'] = "Null"
        return render_template('home.html', user=user, posts=util.gettitles())
    return redirect(url_for("login"))

@app.route('/logout')
def logout():
    if verify():
        session['log'] = "unverified"
    session['action'] = "Logged Out!"
    return redirect(url_for('login'))


if (__name__ == "__main__"):
        app.debug = True
        app.secret_key = "secret"
        app.run(host='0.0.0.0', port=8000)
