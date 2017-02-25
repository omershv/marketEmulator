import json
import urllib2
from Crypto.PublicKey import RSA
import pickle

user = "user99"

keys = private_key = open("keys_private.txt",'rb').read()
key = keys[keys.index(user):]
key = key[key.index("-----BEGIN RSA PRIVATE KEY-----"):]
key = key[:key.index("-----END RSA PRIVATE KEY-----") + len("-----END RSA PRIVATE KEY-----")]

privateKey = RSA.importKey(key)



users = pickle.load(open("keys_public.pkl",'rb'))
public_key_object = RSA.importKey(users[user])
token = privateKey.sign(user,"")[0]

data = {
        'auth': {"user": user, "token": token},
		'type': "buy",
		"commodity": 1,
		'price': 500
}

req = urllib2.Request('http://127.0.0.1')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data))
print response.read()