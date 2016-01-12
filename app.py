from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import urllib2
import json
import util

app = Flask(__name__)

def verify():
    if 'log' in session:
        return session['log'] == 'verified'
    else:
        session['log'] == 'unverified'
        return False
    
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
	print "HKHDASH"
        if request.form["submit"] == "Find By Name":
            query = request.form["place"]
            print(request.form["place"])
            stuff = util.nameTo(query)
            return render_template("test.html", loc = query, lat = stuff["lat"], lng = stuff["long"], add = stuff["add"])
        else:
            lat = request.form["lat"]
            long = request.form["long"]
            print (long + "----" + lat)
            stuff = util.numTo( lat, long )
            return render_template("test.html", loc = "Latitude: "+str(lat)+" Longitude: "+str(long), lat = stuff["lat"], lng = stuff["long"], add = stuff["add"] )

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

@app.route("/testss")
def NearHere():
    l = util.nearHere("48.859294","2.347589")
    i = 0
    dict = {}
    while (i<5):
        dict[i] = l[i]
        i+=1
    return render_template("test.html", result = dict)

@app.route("/tests")
def nearHere():
    add = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"
    key = "AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    
    query = "https://maps.googleapis.com/maps/api/place/radarsearch/json?location=48.859294,2.347589&radius=5000&types=food|cafe&keyword=vegetarian&key=AIzaSyC1HeKfjwS4x0KYw_Wgl5-IxLBELfa4oO0"
    request = urllib2.urlopen(query)
    result = request.read()
    result = json.loads(result)

    i = 0
    l = []
    #print result
    while (i<5):
        placeID = result["results"][i]["place_id"]
        i= i+1
        l.append(placeID)

    #print result
    #print l
>>>>>>> 22973ec0a416f40c2d48602258548c46a427620a

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
