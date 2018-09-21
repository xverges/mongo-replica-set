#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time

from pymongo import MongoClient
from pymongo import ReadPreference


class MongoServerConnection(object):

    def __init__(self, name):
        name = name.upper()
        self.name = name
        self.user = os.environ['ROOT_USER']
        self.password = os.environ['ROOT_PASSWORD']
        self.ip = None
        self.port = None

    def url(self):
        return "mongodb://{0}:{1}@{2}:{3}/".format(
                    self.user,
                    self.password,
                    self.ip,
                    self.port)

    def feed(self):
        client = self.client()
        for database_name in ['db_1', 'db_2']:
            for collection_name in ['col_1']:
                collection = client[database_name][collection_name]
                for count in range(3):
                    id = "{0}_{1}".format(self.name, count)
                    doc = {
                        '_id': id,
                        'server': self.name,
                        'time': time.asctime()
                    } 
                    collection.replace_one({'_id': id}, doc, upsert=True)

    def read(self):
        contents = {}
        client = self.client()
        exclude_dbs = ['admin', 'local']
        for database in [db for db in client.database_names() if db not in exclude_dbs]:
            contents[database] = {}
            for collection in client[database].collection_names():
                contents[database][collection] = tuple(client[database][collection].find())
        return contents

    def update_db(self, database_name):
        client = self.client()
        collection_name = 'col_1'
        collection = client[database_name][collection_name]
        doc = {
            'server': self.name,
            'time': time.asctime()
        } 
        collection.insert_one(doc)

    def client(self):
        raise NotImplementedError()


class StandaloneServer(MongoServerConnection):

    def __init__(self, name):
        MongoServerConnection.__init__(self, name)
        self.ip = 'localhost'
        self.port = os.environ[name + '_PORT']

    def client(self):
        return MongoClient(self.url())

class ReplicaServer(MongoServerConnection):

    def __init__(self, name):
        MongoServerConnection.__init__(self, name)
        self.ip = 'localhost'
        self.port = '27017'

    def client(self):
        replicaset = os.environ['REPLICASET_NAME']
        return MongoClient(self.url(), replicaset=replicaset, read_preference=ReadPreference.NEAREST)
