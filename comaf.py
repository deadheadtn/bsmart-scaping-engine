import requests
import urllib.request
import time
from bs4 import BeautifulSoup
array= []
insertion = []

url =  'http://www.comaf.tn/103-robinetterie.html'
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
    provider='5df6c7b11be228d380424860'
    category='5df11b01254f591192d12204'
    sub='5df11c1a254f591192d12226'
#    print(name+' '+ref+' '+image+' '+desc)
    r = requests.post('http://127.0.0.1:5000/productsadd', json={"name": name,"ref": ref ,"image": image ,"desc": desc,"provider": provider, "Category": category,"SubCategory": sub})
    print(r.status_code)
