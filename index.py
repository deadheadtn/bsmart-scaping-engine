from flask import Flask, render_template, request, redirect , url_for
import flask_login
import requests
import time
import json
import urllib2
from bs4 import BeautifulSoup

app=Flask(__name__)
app.secret_key = 'super_secret_string_very_very_very_very_very_very_bsmart_very_very_very_'  # Change this!
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'email':'foobar' ,'password': 'secret'}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    if request.form['password'] == users['password'] :
        return render_template('home.html')
    else:
        return 'Bad login'

@app.route('/logout')
def logout():
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/searchpage', methods=['GET'])
def query_example():
    array= []
    url= request.args.get('url')
    pageurl= request.args.get('pageurl')
    pageN= int(request.args.get('pagen'))
    prodlink = request.args.get('prodlink')
    if (pageN>1):
        for i in range(1,pageN):
            fullurl=url+pageurl+str(i)
            #print fullurl
            response = requests.get(fullurl)
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.findAll('a', {'class': prodlink}):
                array.append( a['href'])
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.findAll('a', {'class': 'product-name'}):
            array.append( a['href'])
    return render_template('grabbed.html',len= len(array), array = array)


@app.route('/searchcontent', methods=['GET','POST'])
def content():
    if request.method == "GET":
        listprod= []
        array1= []
        req = urllib2.Request('https://api.bsmart.tn/categories')
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsoncat = json.loads(f.read())
        req = urllib2.Request('https://api.bsmart.tn/providerslist')
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonproviders = json.loads(f.read())
        url1= request.args.get('url')
        pageurl= request.args.get('pageurl')
        pageN= int(request.args.get('pagen'))
        prodlink= request.args.get('prodlink')
        if (pageN>1):
            for i in range(1,pageN):
                fullurl=url1+pageurl+str(i)
                #print fullurl
                response = requests.get(fullurl)
                soup = BeautifulSoup(response.text, "html.parser")
                for a in soup.findAll('a', {'class': prodlink}):
                    array1.append( a['href'])
        else:
            response = requests.get(url1)
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.findAll('a', {'class': 'product-name'}):
                array1.append( a['href'])

        titletag= request.args.get('titletag')
        imagetag= request.args.get('imagetag')
        reftag= request.args.get('reftag')
        desctag= request.args.get('desctag')
        for url in array1:
            response = requests.get(url)
            prod= []
            soup = BeautifulSoup(response.text, "html.parser")
            if(titletag=='id'):
                prod.append(soup.find(id=request.args.get('title')))
            elif(titletag=='h1'):
                prod.append(soup.findAll('h1')[0].text.strip())
            elif(titletag=='h2'):
                prod.append(soup.findAll('h2')[0].text.strip())
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('title')}))
            if(reftag=='id'):
                prod.append(soup.find(id=request.args.get('ref')).text)
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('ref')}))
            if(imagetag=='id'):
                prod.append(soup.find(id=request.args.get('image'))['src'])
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('image')})['src'])
            if(desctag=='id'):
                prod.append(soup.find(id=request.args.get('desc')))
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('desc')}))
            listprod.append(prod)
        #return render_template('content.html',len=len(listprod),listprod=listprod)
        return render_template('content.html',len=len(listprod),listprod=listprod,lenc=len(jsoncat),cat=jsoncat,lenp=len(jsonproviders),provider=jsonproviders)
    else:
        listprod= []
        array1= []
        cat = request.form['category']
        subcat= request.form['subcategory']
        provider = request.form['provider']
        req = urllib2.Request('https://api.bsmart.tn/categories')
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsoncat = json.loads(f.read())
        req = urllib2.Request('https://api.bsmart.tn/providerslist')
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsonproviders = json.loads(f.read())
        url1= request.args.get('url')
        pageurl= request.args.get('pageurl')
        pageN= int(request.args.get('pagen'))
        prodlink= request.args.get('prodlink')
        if (pageN>1):
            for i in range(1,pageN):
                fullurl=url1+pageurl+str(i)
                response = requests.get(fullurl)
                soup = BeautifulSoup(response.text, "html.parser")
                for a in soup.findAll('a', {'class': prodlink}):
                    array1.append( a['href'])
        else:
            response = requests.get(url1)
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.findAll('a', {'class': 'product-name'}):
                array1.append( a['href'])

        titletag= request.args.get('titletag')
        imagetag= request.args.get('imagetag')
        reftag= request.args.get('reftag')
        desctag= request.args.get('desctag')
        for url in array1:
            response = requests.get(url)
            prod= []
            soup = BeautifulSoup(response.text, "html.parser")
            if(titletag=='id'):
                prod.append(soup.find(id=request.args.get('title')))
            elif(titletag=='h1'):
                prod.append(soup.findAll('h1')[0].text.strip())
            elif(titletag=='h2'):
                prod.append(soup.findAll('h2')[0].text.strip())
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('title')}))
            if(reftag=='id'):
                prod.append(soup.find(id=request.args.get('ref')).text)
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('ref')}))
            if(imagetag=='id'):
                prod.append(soup.find(id=request.args.get('image'))['src'])
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('image')})['src'])
            if(desctag=='id'):
                prod.append(soup.find(id=request.args.get('desc')))
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('desc')})[0].text.strip())
            listprod.append(prod)
        #return render_template('content.html',len=len(listprod),listprod=listprod)
            jsonprod= {"name": str(prod[0]),"ref": prod[1].encode('utf-8'), "image": str(prod[2]) ,"desc": prod[3],"provider": str(provider), "Category": str(cat),"SubCategory": str(subcat)}
            print (jsonprod)
            r = requests.post('https://api.bsmart.tn/productslist', json=jsonprod)
            print(r.content)
            print(r.status_code)
        return render_template('content.html',len=len(listprod),listprod=listprod,lenc=len(jsoncat),cat=jsoncat,lenp=len(jsonproviders),provider=jsonproviders)


if __name__ =='__main__':
    app.run(host='0.0.0.0',debug=True)
