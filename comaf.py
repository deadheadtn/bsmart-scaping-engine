import requests
import urllib.request
import time
from bs4 import BeautifulSoup
array= []
insertion = []

url =  'http://www.comaf.tn/107-cuvettes-et-accessoires.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
for a in soup.findAll('a', {'class': 'product-name'}):
    array.append( a['href'])
print(array)
for a in array:
    response = requests.get(a)
    soup = BeautifulSoup(response.text, "html.parser")
    name=soup.findAll('h1')[0].text.strip()
    ref=soup.findAll('span', {'class': 'editable'})[0].text
    image=soup.findAll('img', {'id': 'bigpic'})[0]['src']
    desc=soup.findAll('div',{'class':'rte align_justify'})[0].text.strip()
    provider='5d1f3a07274ffd366408f87a'
    category='5d1c2b71f1f6b8c10544240d'
    sub='Sanitaire'
#    print(name+' '+ref+' '+image+' '+desc)
    r = requests.post('http://127.0.0.1:5000/productsadd', json={"name": name,"ref": ref ,"image": image ,"desc": desc,"provider": provider, "Category": category,"SubCategory": sub})
    print(r.status_code)
