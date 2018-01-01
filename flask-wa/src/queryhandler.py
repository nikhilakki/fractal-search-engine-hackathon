#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"

"""
QueryHandler.py module is used to handle the query
comming from user input.
"""

# Header
import nltk
from preprocessor import Preprocessor

class QueryHandler(object):

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
        query_tokens = Preprocessor.tokenise(user_query)
        stemmed_query = Preprocessor.stemmer(query_tokens)
        WH_flag = Preprocessor.find_WH_sent(stemmed_query)
        stopword_removed_query = Preprocessor.stopword_removal(stemmed_query)

        return stopword_removed_query, WH_flag







