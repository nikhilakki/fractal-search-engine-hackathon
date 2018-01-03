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
    '''
    Search class is used in creating HTML forms with required validations
    '''
    query = StringField('Query', validators=[validators.DataRequired(), validators.Length(max=120)])
    productId = StringField('ASIN ID', validators=[validators.DataRequired(), validators.Length(max=32)])

# Inits
app = Flask(__name__) # Flask app init

# Flask app configurations
app.config['SECRET_KEY'] = "asdjfkn2k4n2k3n4&FASghDV*^(SAD"
# Mongodb URI along with DB name ('fractal')
app.config['MONGO_URI'] = "mongodb://localhost:32770/new"

mongo = PyMongo(app) # Mongo db object init

# Views / Routes
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


@app.route('/dashboard', methods=('GET', 'POST'))
# @login_required
def dashboard():
    '''index view displays history of searches and gives the option to put in
    new search query.

    End point - http://127.0.0.1/
    '''
    # if 'username' in session:
    form = SearchForm()
    # searches = mongo.db.search_queries.find()
    result = mongo.db.reviews.find()
    if form.validate_on_submit():
        query = {
            'Search' : form.query.data,
            'ASIN_ID': form.productId.data,
        }

        # query_values = str(query.values())
        # query = query_values[1]
        print(query)
        # db = mongo.db.search_queries.insert_one(query)
        qa_Df = mongo.db.qa.find({'asin': form.productId.data})
        rv_Df = mongo.db.reviews.find({'asin': form.productId.data})
        co = Core(query, qa_Df, rv_Df)
        output = co.engine()
        return render_template('app/dashboard.html', form=form, output=output, query=query)
    return render_template('app/dashboard.html', form=form)#, searches=searches)
    # else:
        # return "<h1>Unauthorised!</h1>"

@app.route('/')
def about():
    return render_template('app/about.html')

# Run Flask App
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
