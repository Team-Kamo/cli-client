#!/usr/bin/python3
from hmac import digest
import requests, sys, subprocess, os
from datetime import datetime
import time
from hashlib import blake2b

endpoint = "http://127.0.0.1:3000/api/v1/"
config_path = os.getenv('HOME') + '/.octane/'


def newroom():
    obj = {'name': 'string'}
    x = requests.post(endpoint+"room/", json=obj)
    with open(config_path+'id', "w") as f:  # .octane.d/id
        f.write(str(x.json()["id"]))
    return x


def connect(verbose=True):
    url = endpoint + "room/" + roomid
    obj = {"name": "string", "request": "connect"}
    x = requests.post(url, json=obj)
    if verbose: print("Connecting: ", x.status_code)


def disconnect(verbose=True):
    url = endpoint + "room/" + roomid
    obj = {"name": "string", "request": "disconnect"}
    x = requests.post(url, json=obj)
    if verbose: print("Disconnecting: ", x.status_code)
    # if x.status_code != 200: print(x.text)


def send_metadata():
    url = endpoint + "room/" + roomid + "/status"
    data = subprocess.run(['xclip', '-o'], stdout=subprocess.PIPE).stdout
    hashval = blake2b(data, digest_size=32).hexdigest()
    print(hashval)
    obj = {"device": "string",
            "hash": hashval,
            "mime": "text/plain",
            "name": "string",
            "timestamp": int(time.time()),
            "type": "string"}
    x = requests.put(url, json=obj)
    print("Sending metadata: ", x.status_code)


def send_content():
    url = endpoint + "room/" + roomid + "/content"
    headers = {"Content-Type": "text/plain"}
    data = subprocess.run(['xclip', '-o', '-selection'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    x = requests.put(url, headers=headers, data=data)
    print("Copying to server: ", x.status_code)
    print(x.text)


def copy_to_server():
    disconnect()
    connect()
    send_metadata()
    send_content()
    disconnect()


def paste_from_server():
    disconnect(verbose=False)
    connect(verbose=False)
    url = endpoint + "room/" + roomid + "/content"
    x = requests.get(url)
    # print("Pasting: ", x.status_code)
    disconnect(verbose=False)
    print(x.text)
    return x.text


try:
    with open(config_path+'id', "r") as f:
        roomid = f.read()
    # print("Existing ID mounted and loaded: ", roomid)
except:
    # print("No existing ID detected. Generating.")
    x = newroom()

if sys.argv[1] == "copy":
    copy_to_server()
elif sys.argv[1] == "paste":
    paste_from_server()
elif sys.argv[1] == "health":
    x = requests.get(url + "health")
elif sys.argv[1] == "room":
    url = endpoint + "room/"
    if sys.argv[2] == "new":
        x = newroom()
    elif sys.argv[2] == "delete":
        url += roomid
        x = requests.delete(url)
    elif sys.argv[2] == "status":
        url += roomid
        x = requests.get(url)
    elif sys.argv[2] == "connect":
        connect()
    elif sys.argv[2] == "disconnect":
        disconnect()

elif sys.argv[1] == "content":
    url = endpoint + "room/" + roomid + "/content"
    if sys.argv[2] == "delete":
        x = requests.delete(url)
    elif sys.argv[2] == "get":
        x = requests.get(url)
    elif sys.argv[2] == "put":
        # data = "mockup"
        data = subprocess.run(['xclip', '-o', '-selection'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        x = requests.put(url, data=data)
        print("Copying to server: ", x.status_code)

elif sys.argv[1] == "status":
    url = endpoint + "room/" + roomid + "/status"
    if sys.argv[2] == "delete":
        x = requests.delete(url)
    elif sys.argv[2] == "get":
        x = requests.get(url) 
    elif sys.argv[2] == "put":
        # data = b"mockup"
        data = subprocess.run(['xclip', '-o', '-selection'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        hashval = blake2b(data, digest_size=32).hexdigest()
        print(hashval)
        obj = {"device": "string",
                "hash": hashval,
                "mime": "text/plain",
                "name": "string",
                "timestamp": int(time.time()),
                "type": "string"}
        x = requests.put(url, json=obj)
        print("Sending metadata: ", x.status_code)


'''
url = endpoint + "room/" + roomid
obj = {"name": "string", "request": "disconnect"}
x = requests.post(url, json=obj)
print("Disonnecting: ", x.status_code)
'''

# print(x.text)
