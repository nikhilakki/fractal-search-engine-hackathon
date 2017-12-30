#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"

"""
QueryHandler.py module is used to handle the query
comming from user input.
"""

# Header
import nltk
from preprocessor import *


def input_query():
    """
    Funtion used to get the query from the UI
    """
    user_query = "will this lotion work on my wrinkles?"
    return user_query


def query_processing(user_query):
	"""
    Function used to preprocess the query
    """
    query_tokens  = tokenise(user_query)
    stemmed_query = stemmer(query_tokens)
    stopword_removed_query = stopword_removal(stemmed_query)
    return stopword_removed_query

def find_WH_queries(stemmed_query):
    """
    Funtion used to find the query is having
    W/H word or not.
    """
    WH_flag = find_WH_sent(stemmed_query)
    return WH_flag





