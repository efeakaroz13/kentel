#Copyright (c) 2022 Efe Akaröz

from flask import Flask,render_template,request,redirect
from auth import auth
from userEditor import userEditor

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods = ["POST","GET"])
def register():
    return render_template("register.html")

app.run(debug=True)