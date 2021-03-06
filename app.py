#Copyright (c) 2022 Efe Akaröz

import contextlib
import re
from click import password_option
from flask import Flask,render_template,request,redirect,abort,make_response
import requests
import pyrebase
import random
import json
from auth import auth
from userEditor import userEditor
from cryptography.fernet import Fernet
import os
import time


key= b'9oNjb1Ed5JYbIuc1fDo5QDs6tMlNar7Q-m6PcvBxEQo='
spttext = "D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG"
crypter = Fernet(key)


firebaseConfig = {
  "apiKey": "AIzaSyBlNavL892O3pRipHmjVygFD7Rvh50Kh44",
  "authDomain": "messagingapppy.firebaseapp.com",
  "databaseURL": "https://messagingapppy.firebaseio.com",
  "projectId": "messagingapppy",
  "storageBucket": "messagingapppy.appspot.com",
  "messagingSenderId": "930410213927",
  "appId": "1:930410213927:web:d2c6669258f4bd0fab1402",
  "measurementId": "G-T4PVT8SJJF"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def encrypt(text):

    return crypter.encrypt(str(text).encode()).decode()

def decrypt(text):
    #crypter.decrypt(str(text).encode())
    return crypter.decrypt(text.encode()).decode()

app = Flask(__name__)
@app.route("/",methods=["POST","GET"])
def index():
    if request.method == "POST":
        username = request.cookies.get("username")
        if username != None:
            #do thing
            username = decrypt(username)
            password = decrypt(request.cookies.get("password"))
            if auth.sign_in(username,password) == 200:
                searchusername = request.form.get("search")
                if userEditor.getUserData(searchusername) == 404:
                   return render_template("home.html",user_find_error=True,old_search=searchusername,username = username)
                else: 
                    return redirect("/user/{}".format(searchusername))
            else:
                return redirect("/")
        else:
            return redirect("/")
    username_cookie = request.cookies.get("username")
    if username_cookie == None:
        return render_template("index.html")
    else:
        try:
            username = decrypt(username_cookie)
            password = decrypt(request.cookies.get("password"))
            if auth.sign_in(username,password) == 200:

                return render_template("home.html",username=username)
            else:
                return render_template("index.html")
        except:
            return render_template("index.html")

@app.route("/user/<username>")
def usernameThing(username):
    user = userEditor.getUserData(username)
    #Auth
    viewerusername = request.cookies.get("username")
    viewerpassword = request.cookies.get("password")
    if viewerusername != None:
        try:
            #for wrong decrypt credentials and preventing internal server errors
            viewerusername = decrypt(viewerusername)
            viewerpassword = decrypt(viewerpassword)
            if auth.sign_in(viewerusername,viewerpassword) == 200:
                if viewerusername == user["username"]:
                    return render_template("profile.html",user=user,self_view=True,username = username)
                else:
                    return render_template("profile.html",user=user,self_view=False,username = username)
            else:
                #No authentication because they entered the wrong credentials to cookies

                return render_template("profile.html",auth=False,user=user,username=user["username"]) 
        except:
            #Return the thing without the auth
            return render_template("profile.html",auth=False,user=user,username=user["username"]) 

    
    return render_template("profile.html",user=user,username=user["username"],auth=False)

@app.route("/login",methods=["POST","GET"])
def login():
    response = make_response(redirect("/"))
    next = request.args.get("next")
    if next != None:
        response = redirect(next)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        response.set_cookie("username",encrypt(username))
        response.set_cookie("password",encrypt(password))
        if auth.sign_in(username,password) == 200:
            return response
        else:
            return render_template("login.html",error="Username or password is not correct")
    return render_template("login.html")

@app.route("/register",methods = ["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fullName = request.form.get("fullName")
        if userEditor.getUserData(username) != 404:
            return abort(403)
        else:
            response = make_response(redirect("/"))
            response.set_cookie("username",encrypt(username))
            response.set_cookie("password",encrypt(password))
            response.set_cookie("fullName",encrypt(fullName))
            auth.sign_up(username,password,fullName,"noavatar")

            return response
    return render_template("register.html",auth=auth,userEditor=userEditor)

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy-policy.html")

@app.route("/report/<username>")
def userNameReport(username):
    try:
        open("reports.txt","a").write(f"""{username} by {decrypt(request.cookies.get("username"))}\n\n""")
        return render_template("report.html",username=username)
    except:
        return abort(403)
class Admin:
    @app.route("/admin",methods=["POST","GET"])
    def admin():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            if username == "admin" and password == "1234":
                
                return f"""
                    Reports:{open("reports.txt","r").readlines()}<br><br>
                    Users:{len(os.listdir("users"))}
                
                """
            else:
                return abort(403)
        return """
            <form action="" method="POST">
                <input type="text" placeholder="Username" name="username"><br>
                <input type="password" placeholder="Password" name="password"><br>
                <button type="submit">Login</button>
            </form>
        
        """


@app.route("/inbox")
def inbox():
    username = request.cookies.get("username")
    if username != None:
        try:
            username = decrypt(username)
            password = decrypt(request.cookies.get("password"))
            if auth.sign_in(username,password) == 200:
                counter = db.child("Users").child(username).child("counter").get().val()
                if counter == None:
                    counter = 0
                else:
                    pass

                data = {
                    "counter":counter+1
                }
                db.child("Users").child(username).update(data)
                inboxData = json.loads(requests.get(firebaseConfig["databaseURL"]+"/Users/{}/inbox.json".format(username)).content)
                if inboxData == None:
                    conv_exits=False
                else:
                    conv_exits=True

                return render_template("Inbox.html",conv_exists=conv_exits)
            else:
                return redirect("/login?next=/inbox")
        except:
            return redirect("/login")
    else:
        return redirect("/login?next=/inbox")

@app.route("/new_chat",methods=["POST","GET"])
def chatcreate():
    if request.method == "POST":
        username = request.cookies.get("username")
        if username == None:
            return abort(403)
        else:
            username = decrypt(username)
            reciever = request.form.get("username")
            if username == reciever:
                return redirect("/inbox")
            password = decrypt(request.cookies.get("password"))
            if auth.sign_in(username,password) == 200:
                userGetterReciever = userEditor.getUserData(reciever)
                userGetterReciever["password"] = "*"
                if userGetterReciever == 404:
                    return render_template("newchat.html",error_user_nf=True)
                else:
                    chatid = f"BLACKLIVESMATTER{random.randint(2273457364573,3498576384987)}"
                    data = {
                        "creator":username,
                        "reciever":userGetterReciever,
                        "timeCreated":time.ctime(time.time()),
                        "chatid":chatid
                    }
                    allConvsUserHave = json.loads(requests.get("https://messagingapppy.firebaseio.com/Users/{}.json".format(username)).content)
                    exists = False
                    try:
                        for conv in allConvsUserHave["inbox"]:
                            convreciever_usrename = allConvsUserHave["inbox"][conv]["reciever"]["username"]
                            convcreate_usrename = allConvsUserHave["inbox"][conv]["creator"]
                            if userGetterReciever["username"] == convcreate_usrename or convreciever_usrename:
                                exists=True
                                break

                    except:
                        exists = False
                    if exists == False:
                        db.child("conv").child(chatid).set(data)
                        db.child("Users").child(username).child("inbox").child(chatid).update(data)
                        db.child("Users").child(userGetterReciever["username"]).child("inbox").child(chatid).update(data)
                    else:
                        pass

                    return redirect("/inbox")
            else:
                return abort(403)
    username = request.cookies.get("username")

    if username != None:
        try:
            username = decrypt(username)
            password = decrypt(request.cookies.get("password"))
            if auth.sign_in(username,password ) == 200:
                return render_template("newchat.html")

            else:
                return redirect("/login?next=/new_chat")
            
        except:
            return redirect("/login?next=/new_chat")
    else:
        return redirect("/login?next=/new_chat")

@app.route("/api/dmbox")
def api():
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username != None:
        username = decrypt(username)
        password = decrypt(password)
        if auth.sign_in(username,password) == 200:
            #Loading inbox
            inbox_=[]
            ConvsDatabase = json.loads(requests.get(firebaseConfig["databaseURL"]+f"/Users/{username}/inbox.json").content)
            if ConvsDatabase == None:
                inbox_ = []
            else:
                for c in ConvsDatabase:
                    recieverVariable = ConvsDatabase[c]["reciever"]["username"]
                    creatorUsernameVariable = ConvsDatabase[c]["creator"]
                    if recieverVariable == username:
                        usernameForView = creatorUsernameVariable
                    else:
                        usernameForView = recieverVariable
                    
                    data = {
                        "username":usernameForView,
                        "chatid":ConvsDatabase[c]["chatid"],
                        
                    }
                    inbox_.insert(0,data)
            return {"auth":True,"inbox":inbox_}
        else:
            return {"auth":False}
    else:
        return {"auth":False}

@app.route("/chat/<chatid>")
def chat(chatid):
    
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username == None:
        return redirect("/login")
    else:
        try:
            username = decrypt(username)
            password = decrypt(password)
            if auth.sign_in(username,password) == 200:
                chat_credentials = json.loads(requests.get(firebaseConfig["databaseURL"]+"/conv/{}.json".format(chatid)).content)
                if chat_credentials == None:
                    return render_template("/inbox")
                else:
                    creatorChat = chat_credentials["creator"]
                    reciever_chat = chat_credentials["reciever"]["username"]
                    if username == creatorChat:
                        viewusername = reciever_chat
                    else:
                        viewusername = creatorChat
                    response = make_response(render_template("chat.html",chat_credentials=chat_credentials,viewusername=viewusername,chatid=chatid,username=username))
                    response.set_cookie("chat",chatid)
                    return response
            else:
                return redirect("/login")
        except:
            return redirect("/login")


@app.route("/msg/send/<chat>",methods=["POST"])
def post_send_msg(chat):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if username == None:
        return {"success":False,"nousername":True}
    else:
        try:
            username = decrypt(username)
            password=  decrypt(password)
            # chatcredentials = json.loads(requests.get(firebaseConfig["databaseURL"]+"/conv/{}.json".format(chat)).content)
            # chatcreatorusername  =chatcredentials["creator"]
            # recieverchatusername = chatcredentials["reciever"]["username"]
            # if username == chatcreatorusername or recieverchatusername == username:
            msg = request.form.get("msg")
            if msg.strip()=="":
                return {"success":False,"e":"strip"}
            else:
                data = {
                    "content":msg,
                    "sender":username,
                    "time":time.time(),
                    "success":True
                    
                }
                db.child("conv").child(chat).child("msgs").push(data)
                db.child("conv").child(chat).update({"lastmsg":msg})
                return data
            # else:
            #     return abort(403)


        except Exception as e:
            return{"success":False,"e":e}

@app.route("/fetch/msgs")
def fetch():
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    chat = request.cookies.get("chat")
    chatcredentials = json.loads(requests.get(firebaseConfig["databaseURL"]+"/conv/{}.json".format(chat)).content)
    creatorchat = chatcredentials["creator"]
    reciever = chatcredentials["reciever"]["username"]
    
    try:
        if decrypt(username) != creatorchat and decrypt(username) != reciever:
            
            return abort(403)
    except:
        return abort(403)
    if username == None:
        return {"success":False}
    else:
        try:
            username = decrypt(username)
            password=  decrypt(password)
            chatdata=[]
            cdata = json.loads(requests.get(firebaseConfig["databaseURL"]+"/conv/{}/msgs.json".format(chat)).content)
            for c in cdata:
                chatdata.insert(0,cdata[c])
            if chatdata == None:
                chatdata = []
            else:
                pass
            return {"success":True,"val":chatdata}
        except:
            return {"success":False}
    

@app.route("/getUsername")
def getUsername():
    try:
        return {"username":decrypt(request.cookies.get("username"))}
    except:
        return abort(403)

@app.route("/create_msg/<reciever>")
def create_username(reciever):
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    try:
        username = decrypt(username)
        password = decrypt(password)






        if username == reciever:
            return redirect("/inbox")
        

        password = decrypt(request.cookies.get("password"))

        if auth.sign_in(username,password) == 200:
            userGetterReciever = userEditor.getUserData(reciever)
            userGetterReciever["password"] = "*"
            if userGetterReciever == 404:
                return redirect("/user/"+reciever)
            else:
                chatid = f"BLACKLIVESMATTER{random.randint(2273457364573,3498576384987)}"
                data = {
                    "creator":username,
                    "reciever":userGetterReciever,
                    "timeCreated":time.ctime(time.time()),
                    "chatid":chatid
                }
                allConvsUserHave = json.loads(requests.get("https://messagingapppy.firebaseio.com/Users/{}.json".format(username)).content)
                exists = False
                try:
                    for conv in allConvsUserHave["inbox"]:
                        convreciever_usrename = allConvsUserHave["inbox"][conv]["reciever"]["username"]
                        convcreate_usrename = allConvsUserHave["inbox"][conv]["creator"]
                        if userGetterReciever["username"] == convcreate_usrename or convreciever_usrename:
                            exists=True
                            break

                except:
                    exists = False
                if exists == False:
                    db.child("conv").child(chatid).set(data)
                    db.child("Users").child(username).child("inbox").child(chatid).update(data)
                    db.child("Users").child(userGetterReciever["username"]).child("inbox").child(chatid).update(data)
                else:
                    pass

                return redirect("/inbox")
        else:
            return {"status":403}








        
    except:
        return abort(403)
   


@app.route("/logout")
def logout():
    response=  make_response(redirect("/"))
    response.set_cookie("username",max_age=0)
    return response

if __name__ == "__main__":
    app.run(debug=True,threaded=True)
