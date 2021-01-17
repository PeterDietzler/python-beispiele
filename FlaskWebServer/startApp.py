
"""
https://www.youtube.com/watch?v=C7_jHYTKUbc
"""

from flask import Flask, jsonify, request, render_template
from os import listdir, system
import giphypop

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dirs")
def show_dirs():
    dir = request.args.get("dir")
    files = listdir(dir)
    return jsonify( files)

@app.route("/templates")
def templates():
    name = request.args.get("name")
    g = giphypop.Giphy()
    gif = g.random_gif(tag=name)
    return render_template("index2.html",user_name=name, gif_link = gif.media_url ) 



def Server():
    #system("firefox 'http://localhost:5000/' 'http://localhost:5000/templates?name=cat'")
    #system("firefox http://localhost:5000/templates?name=cat")
    app.run(debug=True)


if __name__ == "__main__":
	app.run(debug=True)
     


