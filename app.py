from flask import Flask,render_template,request,redirect
from auth import auth
from userEditor import userEditor

print(userEditor.getUserData("efeakaroz13"))
