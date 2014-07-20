import json
import urllib2

def GetHood(hoodname):
    r = urllib2.Request("http://harfordpark.com/api/properties/")
    f = urllib2.urlopen(r)
    properties = json.load(f)
    if hoodname in properties:
        return properties[hoodname]
    else:
        return []

if __name__ == "__main__":
    print [str(x) for x in GetHood("Harford Park")]
