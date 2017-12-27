
# -*- coding: utf-8 -*-
__author__    = "Nikhil Akki"
# MVC Framework
from flask import Flask, request, render_template, redirect, jsonify # Web Framework
# NoSQL Database
from flask_pymongo import PyMongo # NoSQL DB lib
# HTML Forms & Validation
from flask_wtf import FlaskForm # Flask Forms
from wtforms import StringField # Form fields
from wtforms.validators import DataRequired, Length # form validation

# Search Form
class SearchForm(FlaskForm):
    '''
    Search class is used in creating HTML forms with required validations
    '''
    query     = StringField('Query', validators=[DataRequired(), Length(max=120)])
    productId = StringField('ASIN ID', validators=[DataRequired(), Length(max=32)])
# Inits
app   = Flask(__name__) # Flask app init
mongo = PyMongo(app) # Mongo db object init

# Flask app configurations
app.config['SECRET_KEY'] = "asdjfkn2k4n2k3n4&FASghDV*^(SAD"
# app.config['MONGO_PORT'] = 32772
app.config['MONGO_URI']  = "mongodb://fractal:rohanankanvinodnikhil@localhost:27017/fractal"
# app.config['MONGO_DBNAME'] = "fractal"

# Views / Routes
@app.route('/', methods=('GET', 'POST'))
def index():
    '''index view displays history of searches and gives the option to put in
    new search query.

    End point - http://127.0.0.1/
    '''
    form     = SearchForm()
    searches = mongo.db.search_queries.find()
    if form.validate_on_submit():
        query = {
            'Search' : form.query.data,
            'ASIN_ID': form.productId.data,
        }
        print(query)
        db = mongo.db.search_queries.insert_one(jsonify(query))
        return redirect('/')
    return render_template('index.html', form=form, searches=searches)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)

