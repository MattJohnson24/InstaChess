from database import *

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
    
def escape(htmlStr):
    return htmlStr.replace("&", "&amp").replace("<", "&lt").replace(">", "&gt")