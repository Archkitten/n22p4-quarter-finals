# import "packages" from flask
from flask import render_template
from __init__ import app
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api
from sportslocalapi.sportapi import sportapi_bp
from tennis.tennis import tennis_pg
from cruddy.app_notes import app_notes
from cruddy.app_content import app_content
from games.app_games import app_games
from workout.app_workout import app_workout

app.register_blueprint(sportapi_bp)
app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)
app.register_blueprint(tennis_pg)
app.register_blueprint(app_notes)
app.register_blueprint(app_content)
app.register_blueprint(app_games)
app.register_blueprint(app_workout)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/announcements/')
def announcements():
    return render_template("announcements.html")

@app.route('/sports/')
def sports():
    return render_template("sports.html")

@app.route('/scrolling/')
def scrolling():
    return render_template("scrolling.html")

@app.route('/physicaltherapy/')
def physicaltherapy():
    return render_template("physicaltherapy.html")

@app.route('/scoreboard/')
def scoreboard():
    return render_template("scoreboard.html")

@app.route('/teamapi/')
def teamapi():
    return render_template("teamapi.html")

@app.route('/workouts/')
def workouts():
    return render_template("workouts.html")


@app.route('/rules/')
def rules():
    return render_template("rules.html")

@app.route('/contactus/')
def contactus():
    return render_template("contactus.html")

@app.route('/school_rank/')
def school_rank():
    return render_template("school_rank.html")

@app.route('/calendar/')
def calendar():
    return render_template("calendar.html")

@app.route('/calendar1/')
def calendar1():
    return render_template("calendar1.html")


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True,port=8082)
