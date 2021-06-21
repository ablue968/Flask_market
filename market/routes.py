from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Movie, User
from market.forms import RegisterForm
from market import db
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    movies = Movie.query.all()

    return render_template('market.html', movies = movies)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create= User(
            username=form.username.data , 
            email=form.email.data , 
            password=form.password1.data
            )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f' Ups! There seems to be an error creating the user: {err_msg}', category='danger')

    return render_template('register.html', form = form)

