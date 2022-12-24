from flask import Flask, redirect, url_for, render_template, request
from database import *
from validate import *
import bcrypt
import chess
#board = chess.Board()
#print(board)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/guest")
def play():
    return render_template("play.html")

@app.route("/login")
def login():
    return render_template("login.html")


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
        return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8081,debug=True)