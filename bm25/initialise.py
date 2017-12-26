#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"

"""
initialise.py is used to initialise all the datasets and
other processing when sever starts.
"""

# Headers
from commonutils import *
from preprocessor import *

# Path to the datasets
QA_dataset_path = "../../DataSet/qa_Beauty.json"
review_dataset_path = "../../DataSet/Beauty_5.json"


def question_preprocess(QA_filtered_df):
    """
    Function used to preprosess Questions
    Input:Question dataset
    Output:Tokenised questions
    """
    tokenised_question = []
    for questions in QA_filtered_df:
        tokens = tokenise(questions)
        stopwords_free = stopword_removal(tokens)
        stemmed_word = stemmer(stopwords_free)
        tokenised_question.append(stemmed_word)

    return tokenised_question


def review_preprocess(review_filtered_df):
    """
    Function used to preprosess reviews
    Input:review dataset
    Output:Tokenised review
    """
    tokenised_review = []
    for review in review_filtered_df:
        tokens = tokenise(review)
        stopwords_free = stopword_removal(tokens)
        stemmed_word = stemmer(stopwords_free)
        tokenised_review.append(stemmed_word)
    return tokenised_review


# check the usage of the function from help(cleanJson)
cleanJson(QA_dataset_path)

# check the usage of the function from help(load_QA_dataset)
QA_df = load_QA_dataset()

# check the usage of the function from help(load_reveiws_dataset)
review_df = load_reveiws_dataset(review_dataset_path)

# check the usage of the function from help(question_preprocess)
tokenised_question = question_preprocess(QA_df['question'])
QA_df['tokenised question'] = tokenised_question

# check the usage of the function from help(review_preprocess)
tokenised_review = review_preprocess(review_df['reviewText'])
review_df['tokenised reviews'] = tokenised_review
