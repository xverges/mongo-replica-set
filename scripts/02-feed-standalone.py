#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from lib import StandaloneServer


def main():
    StandaloneServer('FIRST').feed()
    StandaloneServer('SECOND').feed()

if __name__ == "__main__":
    main()
