import json
#import urllib.request

def download(url):
    print('Beginning file download with urllib2...')
    path ='/var/www/bsmart_admin/server/uploads/brands'
    #urllib.request.urlretrieve(url, path)
    file= str(url).split("/o/")
    print file[1]
    #return {'path' : path, 'name': url}

with open('brds.json') as json_file:
    data = json.load(json_file)

json_file.close()


for a in data:
    #print a['url']
    download(a['url'])

    #a['image']= download(tmp)
    a.pop('wasted', None)
    a.pop('ctgr', None)
    a.pop('provider', None)
    a.pop('user', None)
    data=a

    jsonFile = open("brds.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
