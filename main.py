# import datetime
from flask import render_template, Flask
from flask import url_for
from flask import redirect
from flask import request
from flask import flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from sqlalchemy import orm
from flask_sqlalchemy import SQLAlchemy
from flask import session
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zyxw4342vut123srqpo89nmlkjihgf78213123edc1233ba'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///server.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

user_name = 'root'
cnt_enters = '???'
cnt_marshs = '???'
age_acc = '???'
conn = sqlite3.connect('server1.db', check_same_thread=False)
sql = conn.cursor()
conn.commit()

sql.execute("""CREATE TABLE IF NOT EXISTS routes (
   cnt_enters INT,
   cnt_marshs INT
)""")


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),
                     index=True, unique=True, nullable=True)
    password = db.Column(db.String(500), nullable=True)

    # created_date = db.Column(db.DateTime,
    #                          default=datetime.datetime.now)

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        # self.created_date = created_date

    def __repr__(self):
        return f'Пользователь {self.name}.' \
               f'Пароль {self.password}'
        # f'Дата создания {self.created_date}'


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=True)

    is_private = db.Column(db.Boolean, default=True)

    def __init__(self, title: str, content: str, is_private: bool):
        self.title = title
        self.content = content
        self.is_private = is_private

    def __repr__(self):
        return f'Заголовок {self.title}' \
               f'Контент {self.content}' \
               f'Приватность {self.is_private}'


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))
    cnt_ent = db.Column(db.Integer, nullable=True, default=0)
    cnt_marsh = db.Column(db.Integer, nullable=True, default=0)
    age_acc = db.Column(db.Integer, nullable=True, default=1)

    def __init__(self, age: int, city: str, cnt_ent: int, cnt_marsh: int, age_acc: int):
        self.age = age
        self.city = city
        self.cnt_ent = cnt_ent
        self.cnt_marsh = cnt_marsh
        self.age_acc = age_acc


def __repr__(self):
    return f'Возраст {self.age}' \
           f'Город {self.city}' \
           f'Кол-во входов на сайт {self.cnt_ent}' \
           f'Кол-во построенных маршрутов {self.cnt_marsh}' \
           f'Кол-во дней на сайте {self.age_acc}'


@app.route('/')
def index():
    session['name'] = ''
    session['login'] = 0
    return "index"


@app.route('/login', methods=['POST', 'GET'])
def login():
    global user_name
    if 'login' in session and session['login'] == 1:
        return redirect('/about')
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            flash('Something went wrong'
                  'Please check your login or password')
            print(1)
            return render_template('login.html')
        else:
            print(2)
            # user_name = name
            return render_template('site_back.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    # zfasdadaw
    if 'login' in session and session['login'] == 1:
        return redirect('/about')
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        name = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(
            name=name).first()
        if user:
            flash('You already have a account')
            print(2)
            return redirect('/login')
        new_user = User(name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return render_template('site_back.html')


@app.route('/about')
def about():
    return render_template('site_back.html')


@app.route('/profile')
def profile():
    global cnt_marshs, cnt_enters, age_acc
    name = user_name
    try:
        name = user_name

    except:
        print(0)
    return render_template('profile.html', name=name, cnt_enters=cnt_enters, cnt_marshs=cnt_marshs, age=age_acc)


def prof_info():
    return user_name, cnt_enters, cnt_marshs, age_acc


if __name__ == '__main__':
    app.run(debug=True)
