#!/usr/bin/env python
import os
import logging as log
from pymongo import MongoClient
from dotenv import load_dotenv

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])

load_dotenv()

#global variables
MONGODB_URL = f'mongodb://{os.getenv("MONGODB_HOST")}:{os.getenv("MONGODB_PORT")}/'

def test():
    try:
        log.info(f'Connecting to MONGO URL: {MONGODB_URL}')
        client = MongoClient(MONGODB_URL)
        db=client.admin
        serverStatusResult=db.command("serverStatus")
        log.info('Connection successfully.')
    except:
        log.exception('Failed to connect to MongoDB')
        exit()

if __name__=='__main__':
    test()