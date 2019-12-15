import json
import urllib.request

def download(url):
    print('Beginning file download with urllib2...')
    path ='/var/www/bsmart_admin/server/uploads/brands'
    urllib.request.urlretrieve(url, path)
    return {'path' : path, 'name': url}

with open('brds.json') as json_file:
    data = json.load(json_file)

json_file.close()


for a in data:
    tmp= a['url']
    a['image']= download(tmp)
    data=a
    jsonFile = open("brds.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
