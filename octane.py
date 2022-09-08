#!/usr/bin/python3
import requests, sys, time, subprocess

url = "http://127.0.0.1:3000/api/v1/"

roomid = sys.argv[3] if len(sys.argv) > 3 else "-1"

if sys.argv[1] == "health":
    x = requests.get(url + "health")

elif sys.argv[1] == "room":
    url = url + "room/"
    if sys.argv[2] == "new":
        obj = {'name': 'string'}
        x = requests.post(url, json=obj)
    elif sys.argv[2] == "delete":
        url += roomid
        x = requests.delete(url)
    elif sys.argv[2] == "status":
        url += roomid
        x = requests.get(url)
    elif sys.argv[2] == "switch":
        url += roomid
        obj = {"name": "string", "request": "string"}
        x = requests.post(url, json=obj)

elif sys.argv[1] == "content":
    url = url + "room/" + roomid + "/content"
    if sys.argv[2] == "delete":
        x = requests.delete(url)
    elif sys.argv[2] == "get":
        x = requests.get(url)
    elif sys.argv[2] == "put":
        data = subprocess.run(['xclip', '-o', '-selection'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        x = requests.put(url, data=data)

elif sys.argv[1] == "status":
    url = url + "room/" + roomid + "/status"
    if sys.argv[2] == "delete":
        x = requests.delete(url)
    elif sys.argv[2] == "get":
        x = requests.get(url) 
    elif sys.argv[2] == "put":
        obj = f'''{
                    "device": {subprocess.run(['uname', '-r'], 
                                stdout=subprocess.PIPE).stdout.decode('utf-8')},
                    "hash": "string",
                    "mime": "string",
                    "name": "string",
                    "timestamp": {time.time()},
                    "type": "string"
                }'''
        x = requests.put(url, json=obj)



print(x.text)