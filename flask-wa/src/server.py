# -*- coding: utf-8 -*-
__author__ = "Nikhil Akki"
# MVC Framework
from flask import Flask, render_template, redirect, request, url_for# Web Framework
# NoSQL Database
from flask_pymongo import PyMongo # NoSQL DB lib
# HTML Forms & Validation
from flask_wtf import FlaskForm # Flask Forms
from wtforms import Form, BooleanField, StringField, PasswordField, validators # form validation
from core import Core


# Search Form
class SearchForm(FlaskForm):
    """
    Search class is used in creating HTML forms with required validations
    """
    query = StringField('Query', validators=[validators.DataRequired(), validators.Length(max=120)])
    productId = StringField('ASIN ID', validators=[validators.DataRequired(), validators.Length(max=32)])

# Inits
app = Flask(__name__) # Flask app init

# Flask app configurations
app.config['SECRET_KEY'] = "asdjfkn2k4n2k3n4&FASghDV*^(SAD"
app.config['MONGO_URI'] = "mongodb://localhost:32769/new"

mongo = PyMongo(app) # Mongo db object init

# Views / Routes
@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    """index view displays history of searches and gives the option to put in
    new search query.

    End point - http://127.0.0.1/
    """
    form = SearchForm()
    result = mongo.db.reviews.find()
    if form.validate_on_submit():
        query = {
            'Search' : form.query.data,
            'ASIN_ID': form.productId.data,
        }
        user_query = query.get('Search')
        qa_Df = mongo.db.qa.find({'asin': form.productId.data})
        rv_Df = mongo.db.reviews.find({'asin': form.productId.data})
        co = Core(user_query, qa_Df, rv_Df)
        output = co.engine()
        return render_template('app/dashboard.html', form=form, output=output, query=query)
    return render_template('app/dashboard.html', form=form)

@app.route('/')
def about():
    return render_template('app/about.html')

# Run Flask App
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
