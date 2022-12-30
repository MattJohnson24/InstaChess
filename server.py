from flask import Flask, redirect, url_for, render_template, request, make_response
from database import *
from validate import *
import bcrypt
import secrets
import chess
import chesshelper
from flask_socketio import SocketIO, send, join_room
import json
import random
import gameover

token = "$2a$12$8LeOVbRrNLVIPZ7cp9WgNu"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/play")
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
                response = make_response(redirect('/play'))
                response.set_cookie('auth', authToken)
                return response
            else:
                return render_template("login.html")
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

@app.route("/create", methods = ['POST'])
def create():
    time = escape(request.form['time'])
    color = escape(request.form['color'])
    print(time)
    print(color)
    code = secrets.token_urlsafe(30)
    authentication = request.cookies.get('auth')
    if authentication == None:
        return redirect('/login')
    user = authToUser(authentication)
    if user == None:
        return redirect('/login')
    board = chess.Board()
    if color == "Random":
        randnum = random.randrange(0,2)
        print(randnum)
        if  randnum > .5:
            color = "White"
        else:
            color = "Black"
    seconds = int(time)*10
    if color == "White":
        games.insert_one({"owner": user, "id": code, "time": time, "board": board.fen(), "White": user, "Black": "", "wtime": seconds, "btime": seconds, "chat": []})
    else:
        games.insert_one({"owner": user, "id": code, "time": time, "board": board.fen(), "White": "", "Black": user, "wtime": seconds, "btime": seconds, "chat": []})

    return redirect('/game/'+code)

@app.route("/game/<code>", methods = ['GET'])
def game(code):
    game = games.find_one({"id": code})
    board = game.get("board")
    user = request.cookies.get("auth")
    user = authToUser(user)
    if user == None:
        return redirect("/login")
    if game.get("White") == "" and user != None and user != game.get("owner"):
        socketio.emit('newUser', {'user': user}, to=code)
        games.update_one({"id": code}, {"$set": {"White": user}})
        game = games.find_one({"id": code})
    if game.get("Black") == "" and user != None and user != game.get("owner"):
        socketio.emit('newUser', {'user': user}, to=code)
        games.update_one({"id": code}, {"$set": {"Black": user}})
        game = games.find_one({"id": code})
    currentBoard = chess.Board(board)
    boardmtx = chesshelper.make_matrix(currentBoard)
    blackside = game.get("Black")
    winner, result = gameover.game_status(currentBoard)
    wtime = game.get("wtime")
    btime = game.get("btime")
    chat = game.get("chat")
    if winner == "":
        if wtime == "0":
            winner = "Black wins"
            result = "TIME OUT"
        elif btime == "0":
            winner = "White wins"
            result = "TIME OUT"
        else:
            winner = ""
            result = ""
    print(winner)
    print(result)
    if user == blackside:
        return render_template("game.html", code=code, chat=chat, wtime=wtime, btime=btime, winner=winner, result=result, user1=game.get("White"),user2=game.get("Black"),color="Black", a1=boardmtx[7][0], a2=boardmtx[6][0], a3=boardmtx[5][0], a4=boardmtx[4][0], a5=boardmtx[3][0], a6=boardmtx[2][0], a7=boardmtx[1][0], a8=boardmtx[0][0], 
    b1=boardmtx[7][1], b2=boardmtx[6][1], b3=boardmtx[5][1], b4=boardmtx[4][1], b5=boardmtx[3][1], b6=boardmtx[2][1], b7=boardmtx[1][1], b8=boardmtx[0][1],
    c1=boardmtx[7][2], c2=boardmtx[6][2], c3=boardmtx[5][2], c4=boardmtx[4][2], c5=boardmtx[3][2], c6=boardmtx[2][2], c7=boardmtx[1][2], c8=boardmtx[0][2],
    d1=boardmtx[7][3], d2=boardmtx[6][3], d3=boardmtx[5][3], d4=boardmtx[4][3], d5=boardmtx[3][3], d6=boardmtx[2][3], d7=boardmtx[1][3], d8=boardmtx[0][3],
    e1=boardmtx[7][4], e2=boardmtx[6][4], e3=boardmtx[5][4], e4=boardmtx[4][4], e5=boardmtx[3][4], e6=boardmtx[2][4], e7=boardmtx[1][4], e8=boardmtx[0][4],
    f1=boardmtx[7][5], f2=boardmtx[6][5], f3=boardmtx[5][5], f4=boardmtx[4][5], f5=boardmtx[3][5], f6=boardmtx[2][5], f7=boardmtx[1][5], f8=boardmtx[0][5],
    g1=boardmtx[7][6], g2=boardmtx[6][6], g3=boardmtx[5][6], g4=boardmtx[4][6], g5=boardmtx[3][6], g6=boardmtx[2][6], g7=boardmtx[1][6], g8=boardmtx[0][6],
    h1=boardmtx[7][7], h2=boardmtx[6][7], h3=boardmtx[5][7], h4=boardmtx[4][7], h5=boardmtx[3][7], h6=boardmtx[2][7], h7=boardmtx[1][7], h8=boardmtx[0][7])
    else:
        return render_template("game.html", code=code, chat=chat, wtime=wtime, btime=btime, winner=winner, result=result, user1=game.get("White"),user2=game.get("Black"),color="White",a1=boardmtx[7][0], a2=boardmtx[6][0], a3=boardmtx[5][0], a4=boardmtx[4][0], a5=boardmtx[3][0], a6=boardmtx[2][0], a7=boardmtx[1][0], a8=boardmtx[0][0], 
    b1=boardmtx[7][1], b2=boardmtx[6][1], b3=boardmtx[5][1], b4=boardmtx[4][1], b5=boardmtx[3][1], b6=boardmtx[2][1], b7=boardmtx[1][1], b8=boardmtx[0][1],
    c1=boardmtx[7][2], c2=boardmtx[6][2], c3=boardmtx[5][2], c4=boardmtx[4][2], c5=boardmtx[3][2], c6=boardmtx[2][2], c7=boardmtx[1][2], c8=boardmtx[0][2],
    d1=boardmtx[7][3], d2=boardmtx[6][3], d3=boardmtx[5][3], d4=boardmtx[4][3], d5=boardmtx[3][3], d6=boardmtx[2][3], d7=boardmtx[1][3], d8=boardmtx[0][3],
    e1=boardmtx[7][4], e2=boardmtx[6][4], e3=boardmtx[5][4], e4=boardmtx[4][4], e5=boardmtx[3][4], e6=boardmtx[2][4], e7=boardmtx[1][4], e8=boardmtx[0][4],
    f1=boardmtx[7][5], f2=boardmtx[6][5], f3=boardmtx[5][5], f4=boardmtx[4][5], f5=boardmtx[3][5], f6=boardmtx[2][5], f7=boardmtx[1][5], f8=boardmtx[0][5],
    g1=boardmtx[7][6], g2=boardmtx[6][6], g3=boardmtx[5][6], g4=boardmtx[4][6], g5=boardmtx[3][6], g6=boardmtx[2][6], g7=boardmtx[1][6], g8=boardmtx[0][6],
    h1=boardmtx[7][7], h2=boardmtx[6][7], h3=boardmtx[5][7], h4=boardmtx[4][7], h5=boardmtx[3][7], h6=boardmtx[2][7], h7=boardmtx[1][7], h8=boardmtx[0][7])


@app.route("/legalmoves/<code>/<piece>", methods = ['GET'])
def legalmoves(code, piece):
    game = games.find_one({"id": code})
    board = game.get("board")
    currentBoard = chess.Board(board)
    moves = list(currentBoard.legal_moves)
    whiteside = game.get("White")
    blackside = game.get("Black")

    auth = request.cookies.get("auth")
    if auth == None:
        return ""
    user = authToUser(auth)
    if user == whiteside and currentBoard.turn == False:
        return ""
    if user == blackside and currentBoard.turn == True:
        return ""

    piecemoves = ""
    for each in moves:
        if str(each)[0:2] == piece:
            piecemoves += str(each)[2:]
    return piecemoves

@app.route("/move/<code>", methods = ['POST'])
def move(code):
    game = games.find_one({"id": code})
    board = game.get("board")
    currentBoard = chess.Board(board)
    move = request.form["move"]
    piece = request.form["piece"]

    updateboard = chess.Move.from_uci(piece+move)
    currentBoard.push(updateboard)
    games.update_one({"id": code}, {"$set": {"board": currentBoard.fen()}})
    socketio.emit('newMove', {'board': currentBoard.fen()}, to=code)
    return redirect("/game/"+code)

@socketio.on('message')
def handle_message(msg):
    if "comment" in msg:
        msg = escape(msg)
        jsonformat = json.loads(msg)
        comment = jsonformat.get("comment")
        code = jsonformat.get("code")
        print(comment)
        print(code)
        game = games.find_one({"id": code})
        chat = game.get("chat")
        auth = request.cookies.get("auth")
        user = authToUser(auth)
        chat.append(user+": "+comment)
        games.update_one({"id": code}, {"$set": {"chat": chat}})
        socketio.emit('newMessage', {'messages': user+": "+comment}, to=code)

@socketio.on('initialDataRequest')
def initialSend(data):
    authID = data['authToken']
    room = data['code']
    if authID == "none":
        return
    username = authToUser(authID)
    if username == None:
        return
    else:
        join_room(room)
        socketio.emit('newMessage', {'messages': username+" entered the room."}, to=room)

@app.route("/turn/<code>", methods = ['GET'])
def turn(code):
    game = games.find_one({"id": code})
    board = game.get("board")
    currentBoard = chess.Board(board)
    if currentBoard.turn == True:
        return "white"
    else:
        return "black"
    
@app.route("/whitetime/<code>", methods = ['POST'])
def whitetime(code):
    games.update_one({"id": code}, {"$set": {"wtime": request.form['time']}})
    if request.form['time'] == "0":
        socketio.emit('newUser', {'time': request.form['time']}, to=code)
    return "1"

@app.route("/blacktime/<code>", methods = ['POST'])
def blacktime(code):
    print(type(request.form['time']))
    games.update_one({"id": code}, {"$set": {"btime": request.form['time']}})
    if request.form['time'] == "0":
        socketio.emit('newUser', {'time': request.form['time']}, to=code)
    return "1"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0",port=8081,debug=True)