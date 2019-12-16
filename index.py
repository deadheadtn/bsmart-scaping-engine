# coding=utf-8

from flask import Flask, render_template, request, redirect , url_for
import flask_login
import requests
import time
import json
import urllib2
import pymongo
import hashlib
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

def download(url):
    print 'Beginning file download with urllib2...'
    ext1= url.split(".")
    filename= hashlib.md5(url).hexdigest()
    ext=filename+"."+ext1[len(ext1)-1]
    path= str('/var/www/bsmart_admin/server/uploads/products/')+str(ext)
    headers = {'user-agent': 'test-app/0.0.1'}
    r = requests.get(url, headers=headers)
    open(path, 'wb').write(r.content)
    aa= {'path' : 'products/'+ext, 'name': ext}
    print aa
    return aa

@app.route('/searchcontent', methods=['GET','POST'])
def content():
    uri = "mongodb://%s:%s@%s" % ("seif", "test1234", "51.77.147.246")
    myclient = pymongo.MongoClient(uri)

    if request.method == "GET":
        listprod= []
        array1= []
        req = urllib2.Request('https://api.bsmart.tn/api/category')
        opener = urllib2.build_opener()
        f = opener.open(req)
        jsoncat = json.loads(f.read())
        req = urllib2.Request('https://api.bsmart.tn/api/provider')
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
                prod.append(soup.find(id=request.args.get('ref')).text.split(' ')[3])
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('ref')}).split(' ')[3])
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
        return render_template('content.html',len=len(listprod),listprod=listprod,lenc=len(jsoncat['categories']),cat=jsoncat['categories'],lenp=len(jsonproviders['providers']),provider=jsonproviders['providers'])
    else:
        listprod= []
        array1= []
        cat = request.form['category']
        subcat= request.form['subcategory']
        provider = request.form['provider']
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
                prod.append(soup.find(id=request.args.get('ref')).text.split(' ')[3])
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('ref')}).split(' ')[3])
            if(imagetag=='id'):
                prod.append(soup.find(id=request.args.get('image'))['src'])
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('image')})['src'])
            if(desctag=='id'):
                prod.append(soup.find(id=request.args.get('desc')))
            else:
                prod.append(soup.findAll("div", {"class": request.args.get('desc')}).text)
            listprod.append(prod)
        #return render_template('content.html',len=len(listprod),listprod=listprod)
            imaage=download(str(prod[2]))
            jsonprod= {"name": str(prod[0])}
            #jsonprod= {"name": str(prod[0]),"reference": prod[1], "image": imaage ,"description": '',"providers": str(provider), "category": str(cat),"subcategory": str(subcat)}
            print jsonprod
            x = myclient.products.insert_one(jsonprod)
            print x
        return render_template('content.html',len=len(listprod),listprod=listprod,lenc=len(jsoncat),cat=jsoncat,lenp=len(jsonproviders),provider=jsonproviders)


if __name__ =='__main__':
    app.run(host='0.0.0.0',debug=True)
