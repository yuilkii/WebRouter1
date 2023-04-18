from flask import Flask
import datetime
from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask import flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zyxw4342vut123srqpo89nmlkjihgf78213123edc1233ba'

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///server.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),
                     index=True, unique=True, nullable=True)
    password = db.Column(db.String(500), nullable=True)

    def __init__(self, name: str, pssw: str):
        self.name = name
        self.pssw = pssw

    def __repr__(self):
        return f'Пользователь {self.name}.' \
               f'Пароль {self.pssw}'


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))

    def __init__(self, age: int, city: str):
        self.age = age
        self.city = city

    def __repr__(self):
        return f'Возраст {self.age}' \
               f'Город {self.city}' \
               f'ID группы {self.user}'


@app.route('/')
def index():
    session['name'] = ''
    session['login'] = 0
    return "index"


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'login' in session and session['login'] == 1:
        return redirect('/about')
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('login')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(name=name).first()
        if not user or not check_password_hash(user.password, password):
            flash('Something went wrong'
                  'Please check your login or password')
            return redirect(url_for('login.html'))
        return render_template('site_back.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    #zfasdadaw
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
            flash('Account does not exist!')
            return redirect('registration.html')
        new_user = User(name=name, pssw=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect('login.html')


@app.route('/about')
def about():
    return render_template('site_back.html')


if __name__ == '__main__':
    app.run(debug=True)
