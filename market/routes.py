from market import app
from flask import render_template
from market.models import Movie

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    movies = Movie.query.all()

    return render_template('market.html', movies = movies)