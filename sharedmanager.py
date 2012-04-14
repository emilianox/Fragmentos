#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
#
#       Copyright 2011 Alejandro Lucas Cantero <canteroalejandro@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
4#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from sqlite import sqlite
from dbutils import DBUtils


class SharedManager:

    def __init__(self):

        self.__bdmanager = DBUtils()

    def exportSnippet(self,path,snippets):
        u'''Recibe una bd en forma de lista de listas y los inserta en una nueva BD

        >>> exportSnippet(bd,"ale.db")
        True

        '''

        self.__bdmanager.newDataBase(path)

        self.__sql = sqlite(path)

        self.__sql.realizarAltas('snippet',{"title": 0,
                                            "language": 1,
                                            "contens":2,
                                            "tags":3,
                                            "description":4,
                                            "creation":5,
                                            "starred":6,
                                            "reference":7,
                                            "modified":8,
                                            "uploader":9},snippets)
        return True

def main():
    return 0

if __name__ == '__main__':
    main()
