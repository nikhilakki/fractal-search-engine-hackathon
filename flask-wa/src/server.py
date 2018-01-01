# -*- coding: utf-8 -*-
__author__ = "Nikhil Akki"
# MVC Framework
from flask import Flask, render_template # Web Framework
# NoSQL Database
from flask_pymongo import PyMongo # NoSQL DB lib
# HTML Forms & Validation
from flask_wtf import FlaskForm # Flask Forms
from wtforms import StringField # Form fields
from wtforms.validators import DataRequired, Length # form validation
from core import Core

# Search Form
class SearchForm(FlaskForm):
    '''
    Search class is used in creating HTML forms with required validations
    '''
    query = StringField('Query', validators=[DataRequired(), Length(max=120)])
    productId = StringField('ASIN ID', validators=[DataRequired(), Length(max=32)])

# Inits
app = Flask(__name__) # Flask app init

# Flask app configurations
app.config['SECRET_KEY'] = "asdjfkn2k4n2k3n4&FASghDV*^(SAD"
# Mongodb URI along with DB name ('fractal')
app.config['MONGO_URI'] = "mongodb://localhost:32768/fractal"

mongo = PyMongo(app) # Mongo db object init

# Views / Routes
@app.route('/', methods=('GET', 'POST'))
def index():
    '''index view displays history of searches and gives the option to put in
    new search query.

    End point - http://127.0.0.1/
    '''
    form = SearchForm()
    searches = [] # mongo.db.search_queries.find()
    result = mongo.db.reviews.find()
    output = []
    if form.validate_on_submit():
        query = {
            'Search' : form.query.data,
            'ASIN_ID': form.productId.data,
        }
        print(query)
        db = mongo.db.search_queries.insert_one(query)
        qa_Df = mongo.db.qa.find({'asin': form.productId.data})
        rv_Df = mongo.db.reviews.find({'asin': form.productId.data})
        co = Core(query, qa_Df, rv_Df)
        output = co.engine()
        return render_template('index.html', form=form, searches=searches, output=output)
    return render_template('index.html', form=form, searches=searches, output=output)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
