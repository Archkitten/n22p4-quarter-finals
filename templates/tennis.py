from flask import Flask, Blueprint, render_template, request
import requests
from __init__ import app
import json
from cruddy.app_crud import login_required

tennis_pg = Blueprint('tennis', __name__,
                      url_prefix='/tennis/',
                      template_folder='templates',
                      static_folder='static', static_url_path='static/tennis')


@tennis_pg.route('/ranking/', methods=['GET', 'POST'])
def ranking():
    url = "https://sportscore1.p.rapidapi.com/tennis-rankings/atp"

    querystring = {"page": "1"}

    headers = {
        "X-RapidAPI-Host": "sportscore1.p.rapidapi.com",
        "X-RapidAPI-Key": "2deba3c7c5msh59e591f91803406p14659ajsn14474595701e"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    results = json.loads(response.content.decode("utf-8"))

    print(response.text)
    print(results)
    return render_template("ranking.html", results=results)


@tennis_pg.route('/photo_gallery/')
@login_required
def photo_gallery():
    return render_template("photo_gallery.html")


@tennis_pg.route('/roster/', methods=['GET'])
def roster():
    myToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6IjU1MzEyIiwiZW1haWwiOiJnaXJpc2hraGFuZGVsd2FsQGhvdG1haWwuY29tIiwiVmVyc2lvbiI6IjEiLCJEZXZpY2VMb2dpbklkIjoiMTA2NTk3NTUiLCJuYmYiOjE2NTEwODg4MzEsImV4cCI6MTY1MzY4MDgzMSwiaWF0IjoxNjUxMDg4ODMxfQ.nGPOJ_wpYC7-eMgQb6deZqCGWRZNMvnTf5VOLhNJOqQ'
    head = {'Authorization': 'token {}'.format(myToken)}


    url = "https://app.universaltennis.com/api/v1/club/3810/school"


    # headers = {
    #     "Authorization": "Bearer {JWT_TOKEN}"
    # }

    response = requests.get(url, headers=head)

    results = json.loads(response.content.decode("utf-8"))

    # print(response)
    # print(results)

    return render_template("roster.html", results=results)

@tennis_pg.route('/roster_girls/', methods=['GET'])
def roster_girls():
    myToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNZW1iZXJJZCI6IjU1MzEyIiwiZW1haWwiOiJnaXJpc2hraGFuZGVsd2FsQGhvdG1haWwuY29tIiwiVmVyc2lvbiI6IjEiLCJEZXZpY2VMb2dpbklkIjoiMTA2NTk3NTUiLCJuYmYiOjE2NTEwODg4MzEsImV4cCI6MTY1MzY4MDgzMSwiaWF0IjoxNjUxMDg4ODMxfQ.nGPOJ_wpYC7-eMgQb6deZqCGWRZNMvnTf5VOLhNJOqQ'
    head = {'Authorization': 'token {}'.format(myToken)}


    url = "https://app.universaltennis.com/api/v1/club/3811/school"


    # headers = {
    #     "Authorization": "Bearer {JWT_TOKEN}"
    # }

    response = requests.get(url, headers=head)

    results = json.loads(response.content.decode("utf-8"))

    # print(response)
    # print(results)

    return render_template("roster_girls.html", results=results)
