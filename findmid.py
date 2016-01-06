import math

def minDist( coords ):
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
