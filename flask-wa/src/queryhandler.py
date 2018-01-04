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

    def query_processing(user_query):
        """
        Function used to preprocess the query
        """
        stop_words = ['that', 'That']
        query_tokens = Preprocessor.tokenise(user_query)
        stopwords_free = [
            words for words in query_tokens if not words in stop_words
        ]
        stemmed_query = Preprocessor.stemmer(stopwords_free)
        WH_flag = Preprocessor.find_WH_sent(stemmed_query)
        stopword_removed_query = Preprocessor.stopword_removal(stemmed_query)

        return stopword_removed_query, WH_flag
