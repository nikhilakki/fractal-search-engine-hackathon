#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"


"""
preprocessor.py module is used to define functions
whch are required to preprocess the questions and
reviews from the datasets
"""

# Headers
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk

class Preprocessor(object):

    def tokenise(sentance):
        """
        Function used to tokinise the sentances
        in words
        Input : Sentance
        Output : list of words
        """
        tokens = word_tokenize(sentance)
        return tokens


    def stopword_removal(token_words):
        """
        Function used to remove the stopwords.
        Input : List of tokens
        output : List free from stopwords
        """
        stopwords_free = []
        # corpus of english stop words
        stop_words = set(stopwords.words('english'))

        stopwords_free = [
            words for words in token_words if not words in stop_words
        ]

        stopwords_free = [words for words in stopwords_free if len(words) > 1]

        return stopwords_free


    def stemmer(token_word):
        """
        Function used to stem the tokennised words
        Input : List of tokens
        Output : LIst of stem words
        """
        stemmed_word = []
        # corpus of english root words
        snowball_stemmer = SnowballStemmer("english")

        for word in token_word:
            stem_word = snowball_stemmer.stem(word)
            stemmed_word.append(stem_word)

        return stemmed_word


    def spellcheck(token_word):
        """
        Function is used to spell check
        Input : List of Tokens
        Output : List of spell check words
        """


    def find_WH_sent(list_words):
        """
        Function used for POS tgging
        Input : list of words
        Output : Flag ->  True/False
        """
        WH_postag = ['WDT', 'WP', 'WP$', 'WRB']

        postag = nltk.pos_tag(list_words)
        WH_Question = [True for value in postag if value[1] in WH_postag]

        return WH_Question
