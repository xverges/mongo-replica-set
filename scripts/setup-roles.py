#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

from lib import StandaloneAdmin

def main(argv=None):

    if not argv:
        argv = sys.argv
    if len(argv) != 2:
        print "Bad params " + str(argv)
    else:
        print "Setting up roles..."
        server = argv[1].upper()
        StandaloneAdmin(server).setup_roles()

if __name__ == "__main__":
    main()