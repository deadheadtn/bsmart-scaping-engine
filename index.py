from flask import Flask, render_template, request, redirect , url_for
import flask_login
import requests
import time
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
    print pageN
    if (pageN>1):
        for i in range(1,pageN):
            fullurl=url+pageurl+str(i)
            #print fullurl
            response = requests.get(fullurl)
            soup = BeautifulSoup(response.text, "html.parser")
            for a in soup.findAll('a', {'class': 'product-name'}):
                array.append( a['href'])
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.findAll('a', {'class': 'product-name'}):
            array.append( a['href'])
    return render_template('grabbed.html',len= len(array), array = array)


@app.route('/searchcontent', methods=['GET'])
def content():
    array= []
    url= request.args.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    array.append(soup.find(id=request.args.get('title')))
    array.append(soup.find(id=request.args.get('ref')).text)
    array.append(soup.find(id=request.args.get('image'))['src'])
    array.append(soup.find(id=request.args.get('desc')).text)
    return render_template('content.html',len=len(array),soup=array)



if __name__ =='__main__':
    app.run(debug=True)
