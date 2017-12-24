#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
__author__    = "Rohan Damodar"

import numpy as np
import math

class BM25():

	def __init__(self, tokenized_documents):
		'''
		Initialize the variables.
		'''
		self.avglen = sum(list((len(i))/len(tokenized_documents) for i in tokenized_documents))
		self.L = list(len(i)/self.avglen for i in tokenized_documents)
		self.tokenized_documents = tokenized_documents

	def get_term_frequencies(self, query):
	    lis = []
	    self.m = len(self.tokenized_documents)
	    self.n = len(query)
	    for i in range(len(self.tokenized_documents)):
	        for token in query:
	            lis.append(self.tokenized_documents.iloc[i].count(token))
	    term_frequencies = np.array(lis).reshape(self.m,self.n)
	    return term_frequencies

	def inverse_document_frequencies(self, tokenized_documents):
	    idf_values = dict()
	    all_tokens_set = set([item for sublist in self.tokenized_documents for item in sublist])
	    for tkn in all_tokens_set:
	        contains_token = map(lambda doc: tkn in doc, self.tokenized_documents)
	        idf_values[tkn] = 1 + math.log(len(self.tokenized_documents)/(sum(contains_token)))
	    return idf_values

	def get_idf_for_query(self, query):
	    idf_values = self.inverse_document_frequencies(self.tokenized_documents)
	    lis = []
	    self.n = len(query)
	    for token in query:
	        for key, value in idf_values.items():
	            if token == key:
	                lis.append(value)
	        if token not in idf_values.keys():
	        	lis.append(0)
	    idfs_for_query = np.array(lis).reshape(self.n,1)
	    return idfs_for_query

	def get_tfidf(self, tf, idf):
		self.tfidf = np.dot(tf,idf)
		return self.tfidf

	def get_bm25_scores(self, query, tf, idf):
		'''
		Constants for BM25 calculation:
		##############################################################################################################
        #                                                                                                            #
        #                     BM25 = idf * ((k + 1) * tf) / (k * (1.0 - b + b * (L) + tf)                            #
        #                                                                                                            #
		##############################################################################################################
		reference: http://opensourceconnections.com/blog/2015/10/16/bm25-the-next-generation-of-lucene-relevation/ '''
		##############################################################################################################
		k = 1.2
		b = 0.75
		##############################################################################################################
		bm25 = 0
		lis = []
		for i in range(len(tf)):
			for j in range(len(query)):
				x = (idf[j]*((k+1)*tf[i][j])/(k*(1.0-b+b*self.L[i]+tf[i][j])))
				bm25 = bm25 + x
			lis.append(bm25)
			x = 0
			bm25 = 0
		normalizedBM25 = np.array([i/sum(lis) for i in lis])
		return normalizedBM25
