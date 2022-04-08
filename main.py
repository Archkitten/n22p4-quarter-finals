# import "packages" from flask
from flask import Flask, render_template
from __init__ import app
from cruddy.app_crud import app_crud
from cruddy.app_crud_api import app_crud_api
from players.app_player import app_player
from players.app_player_api import app_player_api
from sportslocalapi.sportapi import sportapi_bp

app.register_blueprint(sportapi_bp)
app.register_blueprint(app_crud)
app.register_blueprint(app_crud_api)
app.register_blueprint(app_player)
app.register_blueprint(app_player_api)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sports/')
def sports():
    return render_template("sports.html")

@app.route('/scrolling/')
def scrolling():
    return render_template("scrolling.html")



# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
