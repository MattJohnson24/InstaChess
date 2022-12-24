from flask import Flask, redirect, url_for, render_template, request, make_response
from database import *
from validate import *
import bcrypt
import secrets
import chess
#board = chess.Board()
#print(board)
token = "$2a$12$8LeOVbRrNLVIPZ7cp9WgNu"
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/guest")
def play():
    return render_template("play.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
            username = escape(request.form['username'])
            entered_password = escape(request.form['password'])
            password = users.find_one({'username': username})
            if password == None:
                return render_template("login.html")
            password = password['password']
            entered_password = entered_password.encode('utf-8')
            validLogin = bcrypt.checkpw(entered_password, password)
            if validLogin:
                authToken = secrets.token_urlsafe(80)
                hashedAuthToken = bcrypt.hashpw(authToken.encode('utf-8'), token)
                authentication.insert_one({"username": username, 'authToken': hashedAuthToken})
                response = make_response(redirect('/guest'))
                response.set_cookie('auth', authToken)
                return response
            else:
                return response
    else:
        response = make_response(render_template("login.html"))
        response.set_cookie('auth', '', expires=0)
        return response
    


@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            confirmpassword = escape(request.form['confirmpassword'])
            if validNewUser(username) == False:
                print("INVALIDUSER")
                return render_template("register.html", validUser=False)
            elif validNewPassword(password, confirmpassword) == False:
                print("INVALIDPASS")
                return render_template("register.html")
            else:
                print("VALID")
                password = password.encode('utf-8')
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(password, salt)
                users.insert_one({'username': username, 'password': hash, 'rating': 800, 'wins': 0, 'draws': 0, 'losses': 0})
                return redirect("/login")
    else:
        response = make_response(render_template("register.html"))
        response.set_cookie('auth', '', expires=0)
        return response

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8081,debug=True)