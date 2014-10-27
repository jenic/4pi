#!/usr/bin/python
import urllib.request
stuff = {}

def getParts(url):
    parts = [x for x in url.split('/') if x]
    stuff['board'] = parts[2]
    stuff['thread'] = str(parts[-1])
    return parts[2:]

def buildURI(parts):
    return 'http://a.4cdn.org/%s.json' % '/'.join(parts)

def buildIMG(f):
    return 'http://i.4cdn.org/%s/%s' % (stuff['board'], f)

def getJSON(url):
    uri = buildURI(getParts(url))
    f = urllib.request.urlopen(uri)
    return f.readline()

def serialize(data):
    import json
    return json.loads(data.decode())['posts']

def getIMG(obj):
    import os, errno
    parts = [ [x['tim'], x['ext'] ] for x in obj if 'tim' in x]
    print('Have ' + str(len(parts)))
    r = []

    try:
        os.makedirs(stuff['thread'])
        print("Created dir: " + stuff['thread'])
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    try:
        os.chdir(stuff['thread'])
        print("CWD now:" + os.getcwd())
    except OSError as exception:
        raise

    for a in parts:
        f = ''.join(map(str,a))
        if os.path.isfile(f):
            print(f + ' already exists, skipping')
            continue

        print("Fetching " + f)
        r.append(urllib.request.urlretrieve(buildIMG(f), f))

    return r

def main():
    import sys
    if len(sys.argv) < 2:
        return 0

    for url in sys.argv[1:]:
        print("Getting " + url)
        getIMG(serialize(getJSON(url)))

if __name__ == "__main__":
    main()
