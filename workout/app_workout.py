import markdown
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from cruddy.model import Matches

from workout.workoutquery import *

# blueprint defaults https://flask.palletsprojects.com/en/2.0.x/api/#blueprint-objects
app_workout = Blueprint('workout', __name__,
                      url_prefix='/workout',
                      template_folder='templates/workout/',
                      static_folder='static',
                      static_url_path='static')


@app_workout.route('/workout')
def workout():
    # defaults are empty, in case game data not found
    # render game and note data in reverse chronological order(display latest notes rec on top)
    return render_template('workout.html', table=workout_all())


# Notes create/add
@app_workout.route('/create/', methods=["POST"])
def create():
    """gets data from form and add to Notes table"""
    if request.form:
        po = Matches(
            request.form.get("date"),
            request.form.get("team1"),
            request.form.get("team2"),
            request.form.get("winner"),
            request.form.get("score"),
            request.form.get("url")
        )
        po.create()
    return redirect(url_for('workout.workout'))

@app_workout.route('/delete/', methods=["POST"])
def delete():
    """gets userid from form delete corresponding record from Users table"""
    if request.form:
        gameid = request.form.get("userid")
        po = game_by_id(gameid)
        if po is not None:
            po.delete()
    return redirect(url_for('workout.game'))



# Search Form
@app_workout.route('/search/')
def search():
    """loads form to search Users data"""
    return render_template("search.html")


# Search request and response
@app_workout.route('/search/term/', methods=["POST"])
def search_term():
    """ obtain term/search request """
    req = request.get_json()
    term = req['term']
    response = make_response(jsonify(workout_ilike(term)), 200)
    return response
