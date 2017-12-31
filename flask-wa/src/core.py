#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Rohan Damodar"

from QueryHandler import query_processing
from relevanceCheck import relevance_finder


class Core():

    def __init__(self, queryJson, QA_df, RV_df):
        self.queryJson = queryJson
        self.QA_df = QA_df
        self.RV_df = RV_df

    def engine(self):
        # Step 1: Extract query from json
        query = str(self.queryJson.values())

        # Step 2 : Process the query
        processed_query, WH_flag = query_processing(query)

        # Step 3 : Extract relevant answers and
        #          relevant reviews.
        relAnswer, relReviews = self.find_relevant_stuff(processed_query, WH_flag)

        # Step 4 : Create return json
        sendBackJson = self.merged(relAnswer, relReviews)

        return sendBackJson

    def find_relevant_stuff(self, processed_query, WH_flag):
        # Check for asinId in recieved dataframes
        val = self.check_asin_id()

        if val == 0:
            relAnswer, relReviews = self.present_in_both(processed_query, WH_flag)
        elif val == 1:
            relAnswer, relReviews = self.present_only_in_rv(processed_query)
        elif val == 2:
            relAnswer, relReviews = self.present_only_in_qa(
                processed_query, WH_flag)
        elif val == 3:
            relAnswer, relReviews = self.not_present_in_both()

        return relAnswer, relReviews

    def check_asin_id(self):
        # check if asinId is present in QA, 0 if True else 1
        x = 0 if len(self.QA_df) != 0 else 1
        # check if asinId is present in RV, 0 if True else 2
        y = 0 if len(self.RV_df) != 0 else 2

        # return the sum
        Sum = x + y
        # such that:
        # 0 = Present in both
        # 1 = NOT present in QA but Present in RV
        # 2 = Present in QA but NOT present in RV
        # 3 = NOT present in both
        return Sum

    def present_in_both(self, processed_query, WH_flag):

        # Create answer json
        if len(WH_flag) == 0:
            newDF = self.QA_df[self.QA_df['questionType'] == "yes/no"]
        else:
            newDF = self.QA_df[self.QA_df['questionType'] == "open-ended"]

        if len(newDF) == 0:
            answerJson = {'answer': "Oops! No relevant answer found for your question type!",
                          'answerSentiment': None, 'qaRelScore': None}
        else:
            flag = 'q'
            df = relevance_finder(processed_query, newDF, flag)
            answer = df['answer'].iloc[0]
            ansSentiment = df['answerSentiment'].iloc[0]
            ansRelScore = df['qa_relevance_score'].iloc[0]
            answerJson = {
                'answer': answer, 'answerSentiment': ansSentiment, 'qaRelScore': ansRelScore}

        # Create review json
        flag = 'r'
        df = relevance_finder(processed_query, self.RV_df, flag)
        reviews = df['reviewText'].iloc[0:5].to_json(orient='values')
        revSentiments = df['reviewSentiment'].iloc[0:5].to_json(
            orient='values')
        revRelScore = df['rv_relevance_score'].iloc[0:5].to_json(
            orient='values')

        reviewJson = {'reviews': reviews,
            'reviewSentiment': revSentiments, 'rvRelScore': revRelScore}

        return answerJson, reviewJson

    def present_only_in_rv(self, processed_query):
        # default
        answerJson = {'answer': None,
            'answerSentiment': None, 'qaRelScore': None}

        flag = 'r'
        df = relevance_finder(processed_query, self.RV_df, flag)
        reviews = df['reviewText'].iloc[0:5].to_json(orient='values')
        revSentiments = df['reviewSentiment'].iloc[0:5].to_json(orient='values')
        revRelScore = df['rv_relevance_score'].iloc[0:5].to_json(orient='values')

        reviewJson = {'reviews': reviews,
            'reviewSentiment': revSentiments, 'rvRelScore': revRelScore}

        return answerJson, reviewJson

    def present_only_in_qa(self, processed_query, WH_flag):

        if len(WH_flag) == 0:
            newDF = self.QA_df[self.QA_df['questionType'] == "yes/no"]
        else:
            newDF = self.QA_df[self.QA_df['questionType'] == "open-ended"]

        if len(newDF) == 0:
            answerJson = {'answer': "Oops! No relevant answer found for your question type!", \
                          'answerSentiment':None, 'qaRelScore':None}
        else:
            flag = 'q'
            df = relevance_finder(processed_query, newDF, flag)
            answer = df['answer'].iloc[0]
            ansSentiment = df['answerSentiment'].iloc[0]
            ansRelScore = df['qa_relevance_score'].iloc[0]
            answerJson = {'answer' : answer, 'answerSentiment' : ansSentiment, 'qaRelScore' : ansRelScore}

        # default
        reviewJson = {'reviews' : None, 'reviewSentiment' : None, 'rvRelScore' : None}

        return answerJson, reviewJson

    def not_present_in_both(self):
        answerJson = {'answer' : None, 'answerSentiment' : None, 'qaRelScore' : None}
        reviewJson = {'reviews' : None, 'reviewSentiment' : None, 'rvRelScore' : None}

        return answerJson, reviewJson

    def merged(self, dic1, dic2):
        dic = dic1.copy()
        dic.update(dic2)
        return dic
