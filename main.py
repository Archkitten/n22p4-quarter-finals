# import "packages" from flask
from flask import Flask, render_template
from __init__ import app



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
