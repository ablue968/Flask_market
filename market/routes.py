from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Movie, User
from market.forms import RegisterForm, LoginForm, PurchaseForm
from market import db
from flask_login import login_user, logout_user,  login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseForm()

    #How to purchase!
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Movie.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations, you have purshed {p_item_object.name} for {p_item_object.rent_price}€', category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')
        return redirect(url_for('market_page'))

    if request.method =='GET':
        #this is to ensure there is only 1 owner, if we already have one
        #then the movie is removed from the list
        movies = Movie.query.filter_by(owner=None)
        return render_template('market.html', movies = movies, purchase_form=purchase_form)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()

    #creating user!
    if form.validate_on_submit():
        user_to_create= User(
            username=form.username.data , 
            email=form.email.data , 
            password=form.password1.data
            )
        
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully, you'r now logged in as {user_to_create.username}" , category="success")        
        return redirect(url_for('market_page'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f' Ups! There seems to be an error creating the user: {err_msg}', category='success')

    return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    #checking user for login
    if form.validate_on_submit():

        attempted_user = User.query.filter_by(username = form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! Welcome back {attempted_user.username}', category="success")
            return redirect(url_for('market_page'))
        
        flash('Username and password are not match! Please try again.', category="danger")

    return render_template('login.html', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return  redirect(url_for('home_page'))

