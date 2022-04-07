from flask import Flask, Blueprint, render_template, request
import requests
from __init__ import app
import json

tennis_pg = Blueprint('tennis', __name__,
                      url_prefix='/tennis/',
                      template_folder='templates',
                      static_folder='static', static_url_path='static/tennis')




@tennis_pg.route('/ranking/', methods=['GET','POST'])
def ranking():

    url = "https://sportscore1.p.rapidapi.com/tennis-rankings/atp"

    querystring = {"page":"1"}

    headers = {
        "X-RapidAPI-Host": "sportscore1.p.rapidapi.com",
        "X-RapidAPI-Key": "2deba3c7c5msh59e591f91803406p14659ajsn14474595701e"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    results = json.loads(response.content.decode("utf-8"))

    print(response.text)
    return render_template("ranking.html", response=response)




