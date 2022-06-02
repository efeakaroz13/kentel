#Copyright (c) 2022 Efe Akaröz

from flask import Flask,render_template,request,redirect,abort,make_response



from auth import auth
from userEditor import userEditor
from cryptography.fernet import Fernet
import os


key= b'9oNjb1Ed5JYbIuc1fDo5QDs6tMlNar7Q-m6PcvBxEQo='
spttext = "D6SFDSDJEFJDNUFJ47H238743HFBSDJAKHNDNSMAJDNAHDJUEHAJDMAHNNMCNYENDJ432HG"
crypter = Fernet(key)

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
                   return render_template("home.html",user_find_error=True,old_search=searchusername)
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

                return render_template("home.html")
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
                return render_template("profile.html",user=user)
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
        open("reports.txt","a").write(f"""{username} by {decrypt(request.cookies.get("username"))}""")
        return render_template("report.html",username=username)
    except:
        return abort(403)
class Admin:
    @app.route("/admin",methods=["POST","GET"])
    def admin():
        if request.method == "POST":
            username = request.args.get("username")
            password = request.args.get("password")
            if username == "admin" and password == "1234":
                
                return """
                    Reports:
                    Users:
                
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

app.run(debug=True)