#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"

"""
relevanceCheck.py 
"""

# Header
from bm25 import BM25


def relevance_finder(query, df, flag):
    df_new = df.reset_index()

    if flag == 'q':
        bm = BM25(df_new['tokenised_Questions'])
        tf = bm.get_term_frequencies(query)
        idf = bm.get_idf_for_query(query)
        relevance_score = bm.get_bm25_scores(query, tf, idf)
        df_new['relevance_score'] = relevance_score
        df_new.sort(['relevance_score'], ascending=False)
        return df_new
    else:
        bm = BM25(df_new['tokenisedReview'])
        tf = bm.get_term_frequencies(query)
        idf = bm.get_idf_for_query(query)
        relevance_score = bm.get_bm25_scores(query, tf, idf)
        df_new['relevance Score'] = relevance_score
        df_new.sort(['relevance_score'], ascending=False)
        return df_new
