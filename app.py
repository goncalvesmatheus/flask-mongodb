from flask import Flask, request, render_template, make_response, url_for, session, redirect
from functools import wraps
from flask_pymongo import PyMongo
from pymongo import MongoClient
from collections import namedtuple
import bcrypt
import re
#from author1 import MyMongo


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'MongoLogin'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MongoLogin'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        session['logged_in'] = True
        #return 'Your are logged in as ' + session['username']
        return render_template('info.html')

    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username or password'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')

"""
@app.route('/info', methods=['GET'])
def info():
    if not session.get('logged_in'):
        return 'Not authorized.'
    else:
        MONGO_URI = 'mongodb://localhost'
        # connect to database
        client = MongoClient(MONGO_URI)
        # select the database that will be used
        db = client['author']
        # specify the collection
        collection = db['author1']
        # query find in database passed for variable
        data = collection.find()
        # transform the collection query for list
        #data = list(collection.find())
        # return data inside the render template page
        return render_template('teste.html', data=data)
"""
@app.route('/search', methods=['POST', 'GET'])
def search():
    if not session.get('logged_in'):
        return 'Not authorized.'
    else:
        titlesearch = request.values.get('titlesearch')
        print (titlesearch)
        MONGO_URI = 'mongodb://localhost'
        # connect to database
        client = MongoClient(MONGO_URI)
        # select the database that will be used
        db = client['author']
        # specify the collection
        collection = db['author1']

        if not titlesearch:
            print('vazio')
            # return all in database
            data = collection.find()
            print(data)
        else:
            print('aceita')
            # search title using variable passed from form
            #data = collection.find( { "title" : titlesearch } )
            regx = re.compile(titlesearch, re.IGNORECASE)
            total = collection.find_one( { "title" : regx })
            print(total)
            data = collection.find( { "title" : {'$regex': regx} } )
            print(data)

        # transform the collection query for list
        #data = list(collection.find())
        # return data inside the render template page
        return render_template('search.html', data=data)


if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(debug=True)
