#!/usr/bin/env python
# -*- coding: utf-8 -*-

from snippetmanager import SnippetManager
from dbutils import DBUtils
dbu = DBUtils()

path = dbu.getPathDatabasesDir() + 'MikeSourceCode.db'

sm = SnippetManager(path)
leng = sm.getAllLenguajes()
#~ for l in leng: 
    #~ print l[0]
print leng
