#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from lib import StandaloneServer

def main():
    StandaloneServer('FIRST').update_db('db_2')

if __name__ == "__main__":
    main()
