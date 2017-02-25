"""
This script produces private and public key pairs, should not be run unless you need new keys
"""

import os
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import pickle

if os.path.exists("keys_public.pkl"):
	quit()

random_generator = Random.new().read

users_private = {}
users_public = {}
for i in range(100):
	key = RSA.generate(1024, random_generator) #generate pub and priv key
	private, public = key.exportKey(), key.publickey().exportKey()
	users_private["user%d"%i] = private
	users_public["user%d"%i] = public

pickle.dump(users_public, open("keys_public.pkl",'wb'))

f = open("keys_private.txt",'wb')
for user in users_private.keys():
	f.write("-----------%s-----------\r\n"%user)
	f.write("%s\r\n"%users_private[user])
f.close()
