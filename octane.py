#!/usr/bin/python3
from hmac import digest
import requests, sys, subprocess
from datetime import datetime
import time
from hashlib import blake2b

url = "http://127.0.0.1:3000/api/v1/"

def newroom():
    obj = {'name': 'string'}
    x = requests.post(url+"room/", json=obj)
    with open("id", "w") as f:  # .octane.d/id
        f.write(str(x.json()["id"]))
    return x


try:
    with open("id", "r") as f:
        roomid = f.read()
except:
    x = newroom()


if sys.argv[1] == "health":
    x = requests.get(url + "health")
elif sys.argv[1] == "room":
    url = url + "room/"
    if sys.argv[2] == "new":
        x = newroom()
    elif sys.argv[2] == "delete":
        url += roomid
        x = requests.delete(url)
    elif sys.argv[2] == "status":
        url += roomid
        x = requests.get(url)
    elif sys.argv[2] == "connect":
        url += roomid
        obj = {"name": "string", "request": "connect"}
        x = requests.post(url, json=obj) 
    elif sys.argv[2] == "disconnect":
        url += roomid
        obj = {"name": "string", "request": "disconnect"}
        x = requests.post(url, json=obj)

elif sys.argv[1] == "content":
    url = url + "room/" + roomid + "/content"
    if sys.argv[2] == "delete":
        x = requests.delete(url)
    elif sys.argv[2] == "get":
        x = requests.get(url)
    elif sys.argv[2] == "put":
        data = "mockup"
        # data = subprocess.run(['xclip', '-o', '-selection'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        x = requests.put(url, data=data)

elif sys.argv[1] == "status":
    url = url + "room/" + roomid + "/status"
    if sys.argv[2] == "delete":
        x = requests.delete(url)
    elif sys.argv[2] == "get":
        x = requests.get(url) 
    elif sys.argv[2] == "put":
        data = b"mockup"
        # data = subprocess.run(['xclip', '-o', '-selection'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        hashval = blake2b(data, digest_size=32).hexdigest()
        print(hashval)
        obj = {"device": "string",
                "hash": hashval,
                "mime": "text/plain",
                "name": "string",
                "timestamp": int(time.time()),
                "type": "string"}
        x = requests.put(url, json=obj)


print(x.text)
print(x.status_code)