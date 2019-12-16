import requests
import urllib.request
import time
from bs4 import BeautifulSoup
array= []
insertion = []
for i in range(2,6):
    url =  'http://www.comaf.tn/103-robinetterie.html'+str(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.findAll('a', href=True):
        if 'www.venetacucine.com/fr/fournitures/' in a['href']:
            array.append( a['href'][:-7])
    print(array)
for a in array:
    response = requests.get(a)
    soup = BeautifulSoup(response.text, "html.parser")
    name=soup.findAll('h1')[0].text.strip()
    image="https://www.venetacucine.com"+soup.findAll('img')[0]['data-src']
    desc=soup.findAll('p')[0].text.strip()
    provider='5d1f3a07274ffd366408f877'
    category='5d1c2bc2f1f6b8c10544240f'
    sub='Equipements'
    r = requests.post('http://127.0.0.1:5000/productsadd', json={"name": name, "image": image ,"desc": desc,"provider": provider, "Category": category,"SubCategory": sub})
    print(r.status_code)
