#import geocoder
#import datetime
#import pymongo

#client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
#time1 = datetime.datetime.now().strftime('%d-%m-%Y')
"""
def loc():
    g = geocoder.ip('me')
    return g.latlng

def record():
    try:
        time2 = datetime.datetime.now().strftime(' %H-%M-%S')
        l = loc()
        lat, long = l[0], l[1]
        mydb = client["Data"]
        inf = mydb.pothole
        #for rec in inf.find():
            #if lat not in rec['latitude']:
        rd = {'date': time1, 'time': time2, 'latitude': lat, 'longitude': long}
        inf.insert_one(rd)
    except:
        pass
"""