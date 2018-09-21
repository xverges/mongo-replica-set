#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

from lib import ReplicaServer

def main(argv=None):

    if not argv:
        argv = sys.argv
    if len(argv) != 2:
        print "Bad params " + str(argv)
    else:
        server = argv[1].upper()
        ReplicaServer(server).update_db('db_2')

if __name__ == "__main__":
    main()