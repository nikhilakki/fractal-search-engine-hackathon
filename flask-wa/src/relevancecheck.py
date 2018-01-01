#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Ankan Roy"

"""
relevanceCheck.py
"""

# Header
from bm25 import BM25

class RelevanceCheck(object):

    def get_tf_from_query(query, df, flag):
        df_new = df.reset_index()

        if flag == 'q':
            bm = BM25(df_new['tokenised question'])
            tf = bm.get_term_frequencies(query)
            idf = bm.get_idf_for_query(query)
            relevance_score = bm.get_bm25_scores(query, tf, idf)
            df_new['relevance_score'] = relevance_score
            df_new.sort_values(['relevance_score'], ascending=False)
            return df_new
        else:
            bm = BM25(df_new['tokenised reviews'])
            tf = bm.get_term_frequencies(query)
            idf = bm.get_idf_for_query(query)
            relevance_score = bm.get_bm25_scores(query, tf, idf)
            df_new['relevance_score'] = relevance_score
            df_new.sort_values(['relevance_score'], ascending=False)
            return df_new
