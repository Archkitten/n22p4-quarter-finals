import requests
import json
from json2html import *


def writeStrToFile(file, data):
    with open(file, 'w') as f:
        f.write(data)
        f.close()

def saveJsonStringToFile(str, file):
    json_response = json.dumps(str, indent=4)
    writeStrToFile(file, json_response)


url = "https://odds.p.rapidapi.com/v4/sports"

querystring = {"all":"true"}

headers = {
    "X-RapidAPI-Host": "odds.p.rapidapi.com",
    "X-RapidAPI-Key": "3c101db5femsh08170f558691f17p1b06d8jsn014526dedbe0"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

jsonFile = "templates/teamapi.json"

saveJsonStringToFile(response.text, jsonFile)

with open(jsonFile) as f:
    d = json.load(f)
    e = json2html.convert(json=d)
    g = ("templates/teamapi.html")
    with open(g, "w") as file:
        file.write(str(e))
        print("yes") #to see if the code worked
