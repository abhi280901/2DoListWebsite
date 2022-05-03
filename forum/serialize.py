# Simple serialization examples

class Sculpture:
    name = ''
    createdDate = ''
    size=[]
    weight='0'

class Painting:
    name = ''
    createdDate = ''
    size=[]

class Artist:
    firstName=''
    lastName=''
    birthDate=''
    birthCity=''
    deathDate=''
    works=[]

chicago = Sculpture()
chicago.name='Chicago'
chicago.createdDate='1967'
chicago.size=[15.2,"square"]
chicago.weight='162 tonnes'

guernica = Painting()
guernica.name='Guernica'
guernica.createdDate='1937'
guernica.size=[7.8,3.5,"metres"]

picasso = Artist()
picasso.firstName='Pablo'
picasso.lastName='Picasso'
picasso.birthDate='25 October 1881'
picasso.birthCity='Malaga'
picasso.deathDate='8 April 1973'
picasso.works=[chicago, guernica]

# pickling
import pickle

print(picasso.works[0].name)

bytedata = pickle.dumps(picasso)

print(bytedata)

picasso_loaded = pickle.loads(bytedata)

print(picasso_loaded.works[0].name)


# json - cannot serialize classes
import json

print(guernica.size)
# cannot 'dump' Guernica because it is a class, so dump the size list as a test
jsondata=json.dumps(guernica.size) 
print(jsondata)
guernica_loaded=json.loads(jsondata)
print(guernica_loaded)
