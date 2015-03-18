__author__ = 'Marnee Dearman'
import py2neo
#from py2neo import neo4j
import datetime
import settings
import time

graph_db = py2neo.Graph(settings.DATABASE_URL)
#start over seeding the database
graph_db.delete_all()
