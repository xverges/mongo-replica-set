#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pprint
import pymongo


from lib import StandaloneServer


def main():
    for server in ['FIRST', 'SECOND']:
        print "----{}----".format(server)
        try:
                pprint.pprint(StandaloneServer(server).read())
        except pymongo.errors.OperationFailure as err:
                print err.message

if __name__ == "__main__":
    main()
