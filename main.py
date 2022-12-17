import flask
from flask import Flask, render_template, request

# Flask 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", result_list=None)

@app.route("/display_posts", methods=["POST"])
def display_posts():
    keyword = request.form.get('fname')
    # loc = request.form.get('loc')
    
    result = main(keyword)
    print(result)
    return render_template("index.html",result_list=result)

def main(keyword):
    # main fcn here.