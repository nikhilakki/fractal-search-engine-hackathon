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