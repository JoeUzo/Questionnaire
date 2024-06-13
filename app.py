from flask import Flask, render_template, url_for, redirect, flash, session, abort, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from functools import wraps
from libgravatar import Gravatar
from forms import *
from ques import questions
from get_data import to_dict, tabulate
from mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("ADATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "site_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    age_group = db.Column(db.String)
    gravatar = db.Column(db.String)

    # One-to-Many relationships - Parent.
    first = db.relationship('FirstRange', back_populates='user')
    second = db.relationship('SecondRange', back_populates='user')
    third = db.relationship('ThirdRange', back_populates='user')


class FirstRange(db.Model):
    __tablename__ = "first_range"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    choice = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    # One-to-Many relationship with User() - Child
    user_id = db.Column(db.Integer, db.ForeignKey('site_users.id'))
    user = db.relationship("User", back_populates="first")


class SecondRange(db.Model):
    __tablename__ = "Second_range"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    choice = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    # One-to-Many relationship with User() - Child
    user_id = db.Column(db.Integer, db.ForeignKey('site_users.id'))
    user = db.relationship("User", back_populates="second")


class ThirdRange(db.Model):
    __tablename__ = "Third_range"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=True)
    choice = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('site_users.id'))
    user = db.relationship("User", back_populates="third")


with app.app_context():
    db.create_all()


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(404)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    return render_template('home.html', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data.title()
        user.email = form.email.data.lower()
        user.gravatar = Gravatar(form.email.data.lower()).get_image(size=520, default='robohash')
        password = form.password.data

        if user.query.filter_by(username=user.username.title()).first() or user.query.filter_by(username=user.email).first():
            flash(f"Username or Email address already exists!", 'info')
            return redirect(url_for('register'))

        # user.password = bcrypt.generate_password_hash(password)
        salt_length = randint(16, 32)
        user.password = generate_password_hash(
            password,
            method='pbkdf2:sha3_512:100000',
            salt_length=salt_length
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.title()).first()
        if user is None:
            user = User.query.filter_by(email=form.username.data.lower()).first()
        if not user or not check_password_hash(user.password, form.password.data):
            flash("No user found with that username, or password invalid.")
            return redirect(url_for('login'))
        else:
            session.clear()
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ConsentForm()
    if form.validate_on_submit():
        if form.consent.data == 'Yes':
            session['agree'] = True
            return redirect(url_for('select_age'))
        else:
            return redirect(url_for('logout'))
    return render_template('dashboard.html', form=form)


@app.route('/age', methods=['GET', 'POST'])
@login_required
def select_age():
    form = AgeGroup()

    if form.validate_on_submit():
        age = form.agegroups.data

        add_age(age)
        user = User.query.get(current_user.id)
        print(user.age_group, current_user.id)
        return redirect(url_for('questionnaire'))
    return render_template('agegroup.html', form=form)


@app.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():

    if 'question_index' not in session:
        session['question_index'] = 0

    if 'agree' not in session:
        return redirect(url_for('dashboard'))

    current_ques_index = session['question_index']

    try:
        current_question = questions[current_ques_index]
    except IndexError:
        return redirect(url_for('logout'))

    question = current_question['question']

    form = Questionnaire()
    choices = [option[0] for option in current_question['choices']]
    form.question.choices = choices

    if session['question_index'] == len(questions) - 1:
        form.submit.label.text = 'Submit'

    if form.validate_on_submit():
        choice = form.question.data

        try:
            score = int([option[1] for option in current_question['choices'] if choice in option][0])
        except IndexError:
            score = None

        session['question_index'] += 1
        submit_choices(current_question['question'], choice, score)
        if session['question_index'] < len(questions):
            return redirect(url_for('questionnaire'))
        else:
            return redirect(url_for('completed'))

    return render_template('questionnaire.html', question=question, form=form, no_=session['question_index']+1)


def submit_choices(ques, ch, scr):
    tables = {'1st': FirstRange, '2nd': SecondRange, '3rd': ThirdRange}
    user = User.query.get(current_user.id)

    if 'table' not in session:
        session['table'] = '1st'

    for table in tables:
        if tables[table].query.filter_by(user_id=current_user.id, question=ques).first() is not None:
            tables[table].query.filter_by(user_id=current_user.id, question=ques).delete()

    print(f"this {user.age_group}, {current_user.id}")
    add_choice = tables[user.age_group](
        question=ques,
        user=current_user,
        choice=ch,
        score=scr
    )
    db.session.add(add_choice)
    db.session.commit()


def add_age(opt):
    if opt in ['5 - 17', '18 - 24', '25 - 34']:
        session['table'] = '1st'
    elif opt in ['35 - 44', '45 - 54', '55 - 64']:
        session['table'] = '2nd'
    else:
        session['table'] = '3rd'
    user = User.query.get(current_user.id)
    user.age_group = session['table']
    db.session.commit()
    return


@app.route('/completed')
@login_required
def completed():
    return render_template('completed.html', current_user=current_user)


@app.route('/get-database', methods=['GET', 'POST'])
@admin_only
def get_database():
    table_choices = {'First Range': FirstRange, 'Second Range': SecondRange, 'Third Range': ThirdRange}

    form = ChooseTable()
    form.table.choices = ['Combined'] + [key for key, value in table_choices.items()]
    if form.validate_on_submit():
        if form.table.data == 'Combined':
            data = combined(table_choices)
        else:
            data = db.session.query(table_choices[form.table.data]).all()

        if data:
            all_data = [to_dict(a) for a in data]
            tabulate(all_data)
            return redirect(url_for('download'))
        else:
            flash("No Available Data")
            return redirect(url_for('get_database'))

    return render_template('database.html', form=form)


def combined(dic):
    data = []
    for item in dic:
        lst = db.session.query(dic[item]).all()
        data += lst
    return data


@app.route('/download', methods=['GET', 'POST'])
@admin_only
def download():
    return send_from_directory("static", path="resources/output.xlsx")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('home'))


@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        data = form.data
        Mail(data)
        return redirect(url_for('contact'))
    return render_template("contact.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
