from app_setup import app
from modules import *
from db_setup import *
from flask import render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from functions import *
from flask_login import login_user, login_required, logout_user

@app.route('/')
def index():
    posts = db.session.query(Posts.id,  Posts.post_name, Posts.post, Posts.intro, Posts.date).all()
    return render_template('index.html', posts = posts)

@app.route('/create', methods=["post", "get"])
@login_required
def create():
    db.create_all()
    if request.method == 'POST':
        answer = ''
        post_name = request.form['post_name']
        intro = request.form['intro']
        post = request.form['post']
        postadd = Posts()
        try:
            res = postadd.add_post(post_name, intro, post)
            if res:
                answer = "Статья добавлена"
                return render_template("create.html", answer = answer)
            else:
                answer = 'Произошла ошибка при добалвении статьи'
                return render_template("create.html", answer=answer)
        except:
            answer = 'Произошла ошибка при добалвении статьи'
            return render_template("create.html", answer=answer)
    else:
        return render_template("create.html")

@app.route('/<int:id>')
@login_required
def post_detail(id):
    posts = Posts.query.get(id)
    return render_template('posts.html', post=posts)

@app.route('/<int:id>/delete')
@login_required
def post_delete(id):
    posts = Posts.query.get_or_404(id)
    try:
        db.session.delete(posts)
        db.session.commit()
        return redirect('/')
    except:
        return "Произошла ошибка при удалении!"


@app.route('/<int:id>/update', methods=["post", "get"])
@login_required
def update(id):
    posts = Posts.query.get(id)
    if request.method == 'POST':
        posts.post_name = request.form['post_name']
        posts.post = request.form['post']
        posts.intro = request.form['intro']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка при редактировании!"
    else:
        return render_template("update.html", post=posts)

@app.route('/login', methods=["post", "get"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        psw = request.form["password"]
        user = Users()
        res = user.check_user(username, psw)
        user_check = Users.query.filter_by(username=username).first()
        if res and user_check:
            login_user(user_check)
            next_page = request.args.get('next')
            return redirect('/')
        else:
            return render_template('login.html', responce = res[1])
    else:
        return render_template("login.html")

@app.route('/new_register', methods=["post", "get"])
def register():
    db.create_all()
    if request.method == 'POST':
        username = request.form['login']
        email = request.form['email']
        psw = request.form['psw']
        psw_check = request.form['psw_check']
        if check_username(username)[0] == True and check_email(email)[0] == True \
                and check_password(psw)[0] == True and psw == psw_check:
            user = Users()
            hash = generate_password_hash(psw)
            res = user.add_user(username, email, hash)
            if res: return redirect('/login')
        return render_template("new_register.html")
    else:
        return render_template("new_register.html")

@app.route('/logout', methods=["post", "get"])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.after_request
def redirect_to(responce):
    if responce.status_code == 401:
        return redirect('/login')
    return responce

if __name__ == "__main__":
    app.run()


