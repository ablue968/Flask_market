from flask_bcrypt import check_password_hash
from sqlalchemy.orm import backref
from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


#documentation say I need this for login manager to work
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=5000)
    movies = db.relationship('Movie', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 6:
            return f'{str(self.budget)[:-3], str(self.budget[-3:])}€'
        
        return f"{self.budget}€"
    
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    #In here I define all the functions to do:

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.rent_price

    def can_sell(self, item_obj):
        return item_obj in self.movies



class Movie(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    box_office = db.Column(db.Integer(), nullable=False)
    director = db.Column(db.String(length=12), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    rent_price = db.Column(db.Integer(), nullable= False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))


    def __repr__(self):
        return f'Movie: {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.rent_price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.rent_price
        db.session.commit()