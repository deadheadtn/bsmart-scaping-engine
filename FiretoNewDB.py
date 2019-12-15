import json
import requests

def download(url):
    print('Beginning file download with urllib2...')
    file= str(url).split("/o/")
    ext1= file[1].split(".")
    ext= ext1[1].split("?")[0]
    ff= file[1].split("&token=")
    filename=ff[1]+'.'+ext
    path= str('/var/www/bsmart_admin/server/uploads/brands')+str(filename)
    headers = {'user-agent': 'test-app/0.0.1'}
    r = requests.get(url, headers=headers)
    open(path, 'wb').write(r.content)
    aa= {'path' : 'brands/'+filename, 'name': filename}
    return aa

with open('brds.json') as json_file:
    data = json.load(json_file)

json_file.close()
data1= []

for a in data:
    url= a['url']
    #download(url)
    a['image']= download(url)
    a.pop('wasted', None)
    a.pop('ctgr', None)
    a.pop('provider', None)
    a.pop('user', None)
    data1.append(a)

jsonFile = open("brds_array.json", "w+")
jsonFile.write(json.dumps(data1))
jsonFile.close()
