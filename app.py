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
        # return 'Your are logged in as ' + session['username']
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


@app.route('/search', methods=['POST', 'GET'])
def search():
    if not session.get('logged_in'):
        return 'Not authorized.'
    else:
        titlesearch = request.values.get('titlesearch')
        authorsearch = request.values.get('authorsearch')
        MONGO_URI = 'mongodb://localhost'
        # connect to database
        client = MongoClient(MONGO_URI)
        # select the database that will be used
        db = client['author']
        # specify the collection
        collection = db['author1']

        if titlesearch and authorsearch:
            print('search using title and author')
            # return all in database
            data = collection.find()
        elif titlesearch:
            print('search title')
            # search title using variable passed from form
            # this search use a match between words inside the title
            regx = re.compile(titlesearch, re.IGNORECASE)
            #total = collection.find_one({"title": regx})
            # print(total)
            data = collection.find({"title": {'$regex': regx}})
        elif authorsearch:
            print('search author.')
            # search author using variable passed from form
            # this search use a match between words inside the title
            regx = re.compile(authorsearch, re.IGNORECASE)
            data = collection.find({'author.given': {'$regex': regx}})
            print(data)
        else:
            print('both empty')
            print('complety database')
            data = collection.find()

        # transform the collection query for list
        #data = list(collection.find())
        # return data inside the render template page
        return render_template('search.html', data=data)


if __name__ == "__main__":
    app.secret_key = 'secret'
    app.run(debug=True)
