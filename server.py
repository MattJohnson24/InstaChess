from flask import Flask, redirect, url_for, render_template
import chess
board = chess.Board()
print(board)

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

if __name__ == "__main__":
    app.run(debug=True)