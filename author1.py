import json
from collections import namedtuple
import http.client
import mimetypes
from pprint import pprint
from pymongo import MongoClient


MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)

db = client['author']
collection = db['author1']


conn = http.client.HTTPSConnection("api.crossref.org")
payload = ''
headers = {}
conn.request("GET", "/works/", payload, headers)
res = conn.getresponse()
data = res.read()

dadosPegado = json.loads(data)

print(dadosPegado['status'])
collection.insert_one(dadosPegado)

print('Estado {} '.format(['status']))

for autores in dadosPegado['message']['items']:
     collection.insert_one(autores)
     for autor in autores["author"]:
          print('______________Autor________________')
          print('Given -> {}'.format(autor["given"]))
          print('family -> {}'.format(autor["family"]))
          print('sequence -> {}'.format(autor["sequence"]))
          print('______________afilliation________________')
          for affiliation in autor['affiliation']:
               print('Name -> {}'.format(affiliation["name"]))



