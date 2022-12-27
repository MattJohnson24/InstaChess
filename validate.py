from database import *
import bcrypt

def validNewUser(username):
    if users.find_one({'username': username}) != None:
        return False
    else:
        return True

def validNewPassword(password, confirmpassword):
    if password != confirmpassword:
        return False
    else:
        return True

def authToUser(token):
    if token == None:
        return token
    salt="$2a$12$8LeOVbRrNLVIPZ7cp9WgNu"
    authKey = bcrypt.hashpw(token, salt)
    user = authentication.find_one({"authToken":authKey}).get("username")
    return user

def escape(htmlStr):
    return htmlStr.replace("&", "&amp").replace("<", "&lt").replace(">", "&gt")