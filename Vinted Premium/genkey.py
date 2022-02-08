import random
import string
import json

from pymongo import MongoClient
with open("config.json","r") as config:
    confg = json.load(config)

cluster = MongoClient(confg["mangourl"])
db = cluster["client"]


def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


for i in range(200):
    x = generate_key(42)
    with open("keylist.txt", 'a+') as txt:
        txt.write(f"{x}\n")

print("Clé généré !")
