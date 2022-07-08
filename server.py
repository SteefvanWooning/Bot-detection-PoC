from operator import index
from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        twitter_handle = request.form["input_handle"]

        vals = main.entrypoint(twitter_handle)

        return render_template("results.html", value=twitter_handle, results=vals)

          
        
       
    
    # Enter the main-page of our webserver application.
    else:
        return render_template("index.html")

