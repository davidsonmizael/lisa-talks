#!/usr/bin/env python
import os
import logging as log
from pymongo import MongoClient
from dotenv import load_dotenv

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])

load_dotenv()

class MongoDB:
    
    def __init__(self):
        self.MONGODB_URL = f'mongodb://{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/'
        self.client = None

    def connect(self):
        try:
            if self.client is None:
                log.info(f'Connecting to MONGO URL: {self.MONGODB_URL}')
                self.client = MongoClient(self.MONGODB_URL)
            else:
                log.info('Already connected')
        except:
            log.info('Failed to connect to MONGO URL.')
            exit()

    def query(self, database, collection, query, find_one = False):
        if self.client is None:
            self.connect()
            
        try:
            db = self.client[database]
            col = db[collection]
            if find_one:
                return col.find_one(query)
            else:
                return col.find(query)
        except:
            log.exception(f'DB: {database} - {collection}: Failed to run query: {query} ')

    def count(self, database, collection, query):
        if self.client is None:
            self.connect()

        try:
            db = self.client[database]
            col = db[collection]
            return col.find(query).count()
        except:
            log.exception(f'DB: {database} - {collection}: Failed to run query: {query} ')