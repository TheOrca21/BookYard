from flask import Flask, render_template, request, abort, redirect, url_for
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_mail import Mail
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp
import datetime
import random
from extensions import db
from database import Genre, Users
import os

dt = datetime.datetime
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('Secret_Key_LIb')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('Library_DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
db.init_app(app)

try:
    with app.app_context():
        db.engine.connect()  # Test the connection
        print("Connected to the database successfully!")
except Exception as e:
    print("Error connecting to database:", e)
    # Handle connection errors appropriately


class UserForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    id = random.randint(1, 127777)
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    phone = StringField('Phone:', validators=[DataRequired(), Regexp(r'^\d{10}$', message='Please enter a valid 10-digit phone number.')])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user_registration', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        users = Users()  # Create a Users instance
        users.insert_user(form.name.data, form.email.data, form.password.data,
                          form.address.data, form.phone.data)
        return redirect(url_for('index'))
    return render_template('user_registration.html', form=form)


@app.route('/user')
def main_page():
    genre = Genre()
    genres = genre.genre_names
    return render_template('main_page.html', genres=genres, current_time=dt.utcnow())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
