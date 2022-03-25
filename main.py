# import "packages" from flask
from flask import Flask, render_template
from __init__ import app

from sportslocalapi.sportapi import sportapi_bp
app.register_blueprint(sportapi_bp)

@app.route('/')
def index():
    return render_template("index.html")



# runs the application on the development server
if __name__ == "__main__":
    app.run(debug=True)
