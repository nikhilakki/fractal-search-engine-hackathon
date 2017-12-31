
# -*- coding: utf-8 -*-

__author__ = "Nikhil Akki"

"""
mongodbcreate.py is used in initialise.py for appending all the procsssed CSVs to
MongoDB database & collections.

Forked from GitHub user - mprajwala

Url - https://gist.github.com/mprajwala/849b5909f5b881c8ce6a
"""

import os
import pandas as pd
import pymongo
import json

class MongoDBCreate(object):

    def import_content(filepath, port, dbname, tablename):
        """[summary]

        [description]

        Arguments:
            filepath {[type]} -- [description]
            tablename {[type]} -- [description]

        Keyword Arguments:
            port {number} -- [description] (default: {32768})
            dbname {str} -- [description] (default: {'fractal'})
        """
        mng_client = pymongo.MongoClient('localhost', port)
        mng_db = mng_client[dbname]
        collection_name = tablename
        db_cm = mng_db[collection_name]
        cdir = os.path.dirname(__file__)
        file_res = os.path.join(cdir, filepath)

        data = pd.read_csv(file_res)
        data_json = json.loads(data.to_json(orient='records'))
        db_cm.remove()
        db_cm.insert(data_json)