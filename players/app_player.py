"""control dependencies to support player app routes and APIs"""
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required

from players.playerquery import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_player = Blueprint('player', __name__,
                     url_prefix='/player',
                     template_folder='templates/players/',
                     static_folder='static',
                     static_url_path='static')

""" Blueprint is established to isolate Application control code for player operations, key features:
    1.) 'Players' table control methods, controls relationship between Player Actions and Database Model
    2.) Control methods are achieved using app routes for each player operations
    3.) login required to restrict player operations to identified players
"""


# Default URL for Blueprint
@app_player.route('/')
@login_required  # Flask-Login uses this decorator to restrict acess to logged in players
def player():
    playername = request.form.get('player_name')
    """obtains all Players from table and loads Admin Form"""
    return render_template("player.html", table=players_all(), playername=playername)


# Flask-Login directs unauthorised players to this unauthorized_handler
@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized players to Login page."""
    return redirect(url_for('player.player_login'))


# if login url, show phones table only
@app_player.route('/login/', methods=["GET", "POST"])
def player_login():
    # obtains form inputs and fulfills login requirements
    if request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        if login(email, password):       # zero index [0] used as email is a tuple
            return redirect(url_for('player.player'))

    # if not logged in, show the login page
    return render_template("playerlogin.html")

@app_player.route('/logout')
@login_required
def player_logout():
    logout_user()
    return redirect(url_for('player.player_login'))



@app_player.route('/authorize/', methods=["GET", "POST"])
def player_authorize():
    # check form inputs and creates player
    if request.form:
        # validation should be in HTML
        player_name = request.form.get("player_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password1 = request.form.get("password1")
        password2 = request.form.get("password1")           # password should be verified
        if authorize(player_name, email, phone, password1):    # zero index [0] used as player_name and email are type tuple
            return redirect(url_for('player.player_login'))
    # show the auth player page if the above fails for some reason
    return render_template("playerauthorize.html")


# player create/add
@app_player.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Players table"""
    if request.form:
        po = Players(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
            request.form.get("phone")
        )
        po.create()
    return redirect(url_for('player.player'))


# player read
@app_player.route('/read/', methods=["POST"])
def read():
    """gets playerid from form and obtains corresponding data from Players table"""
    table = []
    if request.form:
        playerid = request.form.get("playerid")
        po = player_by_id(playerid)
        if po is not None:
            table = [po.read()]  # placed in list for easier/consistent use within HTML
    return render_template("player.html", table=table)


# player update
@app_player.route('/update/', methods=["POST"])
def update():
    """gets playerid and name from form and filters and then data in  Players table"""
    if request.form:
        playerid = request.form.get("playerid")
        name = request.form.get("name")
        po = player_by_id(playerid)
        if po is not None:
            po.update(name)
    return redirect(url_for('player.player'))


# player delete
@app_player.route('/delete/', methods=["POST"])
def delete():
    """gets playerid from form delete corresponding record from Players table"""
    if request.form:
        playerid = request.form.get("playerid")
        po = player_by_id(playerid)
        if po is not None:
            po.delete()
    return redirect(url_for('player.player'))


# Search Form
@app_player.route('/search/')
def search():
    """loads form to search Players data"""
    return render_template("search.html")


# Search request and response
@app_player.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(players_ilike(term)), 200)
    return response
