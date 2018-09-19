#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pprint

from lib import ReplicaServer

def main():
    for server in ['FIRST', 'SECOND']:
        pprint.pprint(ReplicaServer(server).read())

if __name__ == "__main__":
    main()
