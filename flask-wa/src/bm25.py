#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains functions for computing rank scores for documents in
corpus"""

from __future__ import division
__author__ = "Rohan Damodar"

import numpy as np
import math


class BM25():
    """Implementation of 'Best Matching 25' ranking function.

    Attributes
    ----------
    avglen : float
    Average length of document in `corpus`.
    L : float
    Length of the document relative to the average length
    of the document in the corpus.
    """

    def __init__(self, tokenized_documents):
        """Initialize the variables.

        Parameters
        ----------
        tokenized_documents : list of list of strings
            Tokenized corpus.
        """
        self.avglen = sum(list((len(i)) / len(tokenized_documents) for i in tokenized_documents))
        self.L = list(len(i) / self.avglen for i in tokenized_documents)
        self.tokenized_documents = tokenized_documents

    def get_term_frequencies(self, query):
        """Computes the term frequency of query against each document

        Parameters
        ----------
        query : list of string
            Tokenized list of query string.

        Returns
        -------
        term_frequencies : sparse matrix
            Sparse matrix of term frequency of query vs document
        """
        lis = []
        self.m = len(self.tokenized_documents)
        self.n = len(query)
        for i in range(len(self.tokenized_documents)):
            for token in query:
                lis.append(self.tokenized_documents.iloc[i].count(token))
        term_frequencies = np.array(lis).reshape(self.m, self.n)
        return term_frequencies

    def inverse_document_frequencies(self, tokenized_documents):
        """Computes inverse document frequency

        Parameters
        ----------
        tokenized_documents : list of list of strings
            Tokenized corpus.

        Returns
        -------
        idf_values : dict
            Dictionary of inverse document frequencies of each word in the corpus
        """
        idf_values = dict()
        all_tokens_set = set([item for sublist in self.tokenized_documents for item in sublist])
        for tkn in all_tokens_set:
            contains_token = map(lambda doc: tkn in doc, self.tokenized_documents)
            idf_values[tkn] = 1 + math.log(len(self.tokenized_documents) / (sum(contains_token)))
        return idf_values

    def get_idf_for_query(self, query):
        """Computes inverse document frequency of the query

        Parameters
        ----------
        query : list of string
            Tokenized list of query string.

        Returns
        -------
        idfs_for_query :
            Vector of inverse document frequency of the query
        """
        idf_values = self.inverse_document_frequencies(self.tokenized_documents)
        lis = []
        self.n = len(query)
        for token in query:
            for key, value in idf_values.items():
                if token == key:
                    lis.append(value)
            if token not in idf_values.keys():
                lis.append(0)
        idfs_for_query = np.array(lis).reshape(self.n, 1)
        return idfs_for_query

    def get_tfidf(self, tf, idf):
        """Computes TF*IDF scores.

        Parameters
        ----------
        tf : sparse matrix
            Sparse matrix of term frequency of query vs document
        idf : vector
            Vector of inverse document frequency of the query

        Returns
        -------
        tfidf : vector
            Vector of dot product of tf and idf
        """
        self.tfidf = np.dot(tf, idf)
        return self.tfidf

    def get_bm25_scores(self, query, tf, idf):
        """Computes BM25 scores for the query against each document in the corpus.

        Parameters
        ----------
        query : list of string
            Tokenized list of query string.
        tf : sparse matrix
            Sparse matrix of term frequency of query vs document
        idf : vector
            Vector of inverse document frequency of the query

        Returns
        -------
        normalizedBM25 : normalized vector
            BM25 score of query against each document in the corpus

        Formula
        -------
        #####################################################################
        #                                                                   #
        #    BM25 = idf * ((k + 1) * tf) / (k * (1.0 - b + b * (L) + tf)    #
        #                                                                   #
        #####################################################################

        Reference
        ---------
        https://goo.gl/SXCBym

        Data :
        ------
        k = 1.2 - Free smoothing parameter for BM25.
        b = 0.75 - Free smoothing parameter for BM25.
        """
        k = 1.2
        b = 0.75
        bm25 = 0
        lis = []
        for i in range(len(tf)):
            for j in range(len(query)):
                x = (idf[j] * ((k + 1) * tf[i][j]) / (k * (1.0 - b + b * self.L[i] + tf[i][j])))
                bm25 = bm25 + x
            lis.append(bm25)
            x = 0
            bm25 = 0
        normalizedBM25 = np.array([i / sum(lis) for i in lis])
        return normalizedBM25
