from db_setup import db, manager
from werkzeug.security import check_password_hash
from datetime import datetime
from flask_login import UserMixin

def unpackIterable(iterator):
    output = ()
    for obj in iterator:
        output += (obj,)
    return output

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, unique = True)
    email = db.Column(db.Text, unique = True)
    password = db.Column(db.Text)

    def add_user(self, username, email, hash):
        self.email = email
        self.username = username
        self.password = hash
        try:
            res = db.session.execute(f"SELECT COUNT(*) FROM users WHERE email = '{email}' OR username = '{username}';")
            if unpackIterable(res)[0][0] > 0:
                return (False, 'Такой e-mail или пользователь уже зарегистрированы!')
            else:
                db.session.add(self)
                db.session.commit()
                return (True, 'Пользователь добавлен!')
        except:
            db.session.rollback()
            return (False, 'Ошибка добавления в БД!')

    def check_user(self, username, hash):
        res = db.session.execute(f"SELECT COUNT(*) FROM users WHERE username = '{username}';")
        if unpackIterable(res)[0][0] == 1:
            res = db.session.execute(f"SELECT password FROM users WHERE username = '{username}';")
            if check_password_hash(unpackIterable(res)[0][0], hash) == True:
                return (True, "WELCOME!")
            else:
                return (False, f"Wrong password, try again")
        else:
            return (False, f"Wrong login, try again")

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post_name = db.Column(db.Text, unique = True)
    intro = db.Column(db.Text, unique = True)
    post = db.Column(db.Text, unique = True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def add_post(self, name, intro, post_about):
        self.post_name = name
        self.intro = intro
        self.post = post_about
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
