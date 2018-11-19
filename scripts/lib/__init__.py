#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time

import pymongo


class MongoServerConnection(object):

    def __init__(self, name):
        name = name.upper()
        self.name = name
        self.user = os.environ['RW_USER']
        self.password = os.environ['RW_PASSWORD']
        self.ip = None
        self.port = None

    def url(self):
        return "mongodb://{0}:{1}@{2}:{3}/".format(
                    self.user,
                    self.password,
                    self.ip,
                    self.port)

    def feed(self):
        def add_items(collection):
            for count in range(2):
                id = "{0}_{1}".format(self.name, count)
                doc = {
                    '_id': id,
                    'time': time.asctime()
                } 
                collection.replace_one({'_id': id}, doc, upsert=True)

        client = self.client()
        for database_name in ['db_1', 'db_2']:
            for collection_name in ['col_1']:
                collection = client[database_name][collection_name]
                add_items(collection)
        collection = client['local']['not_replicated']
        try:
            add_items(collection)
        except pymongo.errors.OperationFailure as err:
            if "not authorized on local" in err.message:
                print "Not authorized to add items to local collection"
            else:
                raise err

    def read(self):
        def read_collection(contents, database, collection):
            if database not in contents:
                contents[database] = {}
            contents[database][collection] = tuple(client[database][collection].find())
            return contents
        contents = {}
        client = self.client()
        exclude_dbs = ['admin', 'local']
        for database in [db for db in client.database_names() if db not in exclude_dbs]:
            for collection in client[database].collection_names():
                contents = read_collection(contents, database, collection)
        contents = read_collection(contents, 'local', 'not_replicated')
        return contents

    def update_db(self, database_name):
        client = self.client()
        collection_name = 'col_1'
        doc = {
            'server': self.name,
            'time': time.asctime()
        } 
        collection = client['local']['not_replicated']
        collection.insert_one(doc)
        collection = client[database_name][collection_name]
        collection.insert_one(doc)

    def client(self):
        raise NotImplementedError()


class StandaloneServer(MongoServerConnection):

    def __init__(self, name):
        MongoServerConnection.__init__(self, name)
        self.ip = 'localhost'
        self.port = os.environ[name + '_PORT']

    def client(self):
        return pymongo.MongoClient(self.url())

class ReplicaServer(MongoServerConnection):

    def __init__(self, name):
        MongoServerConnection.__init__(self, name)
        self.ip = 'localhost'
        self.port = '27017'

    def client(self):
        replicaset = os.environ['REPLICASET_NAME']
        return pymongo.MongoClient(self.url(),
                                   replicaset=replicaset,
                                   read_preference=pymongo.ReadPreference.NEAREST)

class StandaloneAdmin(StandaloneServer):

    def __init__(self, name):
        StandaloneServer.__init__(self, name)
        self.user = os.environ['ROOT_USER']
        self.password = os.environ['ROOT_PASSWORD']

    def setup_roles(self):
        client = self.client()
        new_role = "listCollections"
        create_role = {
            "privileges": [
                {
                    "resource": {
                        "db": "local",
                        "collection": ""
                    },
                    "actions": ["listCollections"]
                }
            ],
            "roles": []
        }
        try:
            client.admin.command("createRole", new_role, **create_role)
        except pymongo.errors.DuplicateKeyError:
            pass

        roles = [
            {
                "role": "readWriteAnyDatabase",
                "db": "admin"
            },
            {
                "role": new_role,
                "db": "admin"
            },
            {
                "role": "readWrite",
                "db": "local"
            }
        ]
        client.admin.command("updateUser", os.environ['RW_USER'], roles=roles)