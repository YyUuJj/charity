from cmath import log
from distutils.debug import DEBUG
import re
from flask import Flask, make_response, render_template, request, session, url_for, flash, redirect, abort, g
import sqlite3, os
from DataBase import DataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import RegisterForm
# from admin.admin import admin


app = Flask(__name__)
SECRET_KEY = '12341'
DATABASE = 'tmp/main.db'
app.config['SECRET_KEY'] = '725a259864a0f8c7636a25ddc63a8c966afd6f86'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'main.db')))

login_manager = LoginManager(app)
# login_manager.login_view = 'login'
login_manager.login_message = 'Для начала работы авторизуйтесь'
login_manager.login_message_category = 'success'


@app.route("/")
def index():
    db = get_db()
    dbase = DataBase(db)
    return render_template('index.html', title='Charity')


@app.route("/registration", methods=['POST', 'GET'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        print("Я ДОШЕЛ ДО СЮДА")
        res = dbase.addUser(form.name.data, form.email.data, hash)
        if res:
            flash('Вы успешно зарегистрированы', 'success')
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", 'error')
    return render_template('registration.html', title='Регистрация', form=form)

@app.route('/login')
def login():
    return render_template('login.html', title="Вход")


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    else:
        print('бд подключена')
    return g.link_db

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = DataBase(db)


@login_manager.user_loader
def load_user(user_id):
    print("load user")
    print(dbase)
    return UserLogin().fromDB(user_id, dbase)



if __name__ == "__main__":
    print("Запускаем сайт...")
    app.run(debug=True)
    print("Сайт отключен...")
