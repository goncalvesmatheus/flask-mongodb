# Project using Flask + MongoDB
The project was developed using Flask and MongoDB.
We can create a user account in the system, add the username and password in the database. We use the hash code to create an encrypted password.


## Start
Need to have a MongoDB service started in localhost.
After that, just start the author1.py, wich will be responsible to add JSON information in the table inside the database service.

```
python3 author1.py
```
And now start the app.py and open in the Browser http://127.0.0.1:5000 
```
python3 aoo.py
```


### Documentation

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Flask is a lightweight WSGI web application framework.
* [MongoDB](https://docs.mongodb.com/) - MongoDB is a general purpose, document-based, distributed database built for modern application developers and for the cloud era.
* [PyMongo](https://pymongo.readthedocs.io/en/stable/) - PyMongo is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python.