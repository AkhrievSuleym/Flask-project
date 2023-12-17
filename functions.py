from db_setup import db

def isspecial(string):
    '''Проверяет имеет ли следующая строка спецсимволы'''
    special = ('.', ',', '!', '?', ':', '"', '\'', '@', '#',\
    '$', '%', '&', '*', '^', '\\', '/', '|', '~', '{', '}', '[', ']')
    for char in string:
        if char in special:
            return True
    return False

def check_username(username):
    in_db = db.session.execute(f"SELECT COUNT(*)\
                                    FROM users\
                                    WHERE username = '{username}';")
    error = ''
    if in_db == 0:
        for char in username:
            if not ('A' <= char <= 'Z' or 'a' <= char <= 'z' or char == '_'):
                error += "Invalid characters in username, "
                break
        if username[0] == '_':
            error += "your username mustn't start with _ "

        if len(username) < 6:
            error += "username must be at least 6 characters, "
    else:
        error = "User with this username already exists"
    if error != '':
        return (True, "Success")
    else:
        return (False, error)

def check_email(email):
    in_db = db.session.execute(f"SELECT COUNT(*)\
                                FROM users\
                                WHERE email = '{email}';")
    error = ''
    if in_db == 0:
        if email[0:email.find('@')] == '' or email[email.find('@')] == ' '\
            or email.find('@') == len(email) - 1:
            error = "Incorrect email"
    else:
        error = "User with this email already exists"
    if error != '':
        return (True, "Success")
    else:
        return (False, error)

def check_password(password):
    if password != None and len(password) >= 8:
        digit = 0
        uppercase = 0
        lowercase = 0
        special = 0
        for char in password:
            if char.isdigit() == True:
                digit = 1
            if char.isupper() == True:
                uppercase = 1
            if char.islower() == True:
                lowercase = 1
            if isspecial(char) == True:
                special = 1
        if digit == 1 and uppercase == 1 and lowercase == 1 and special == 1:
            return (True, "Success")
        else:
            return (False, "Password should contain various symbols")
    else:
        return (False, "Password lenth must be at least 8 characters")
