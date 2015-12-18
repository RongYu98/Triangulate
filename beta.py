from urllib2 import urlopen
import urllib2

if __name__=='__main__':      
    webp=urllib2.urlopen("http://stuy.enschool.org/").read()
    x = webp.find("AMC")
    #page = urlopen('http://stuy.enschool.org/').read()
    print x
    
