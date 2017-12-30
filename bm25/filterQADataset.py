#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"

"""
filterQADataset.py module is used to filter the
dataset based on whether query is having W/H
words or not and also send the datasets for relevance check
"""

def filter_question_dataset(WH_flag, QA_df):
    """
    Function used to filter the question dataset
    based on the W/H flag,True or False.
    """
    if len(WH_flag) == 0:
        QA_df = QA_df[QA_df['questionType'] == "yes/no"]
        return QA_df
    else:
        QA_df = QA_df[QA_df['questionType'] == "open-ended"]
        return QA_df

