#!/usr/bin/env python
#mandatory imports
import logging as log
import os

#script imports
import json
import pickle
import nltk
import numpy as np
from nltk.stem import LancasterStemmer

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])

#global variables
USE_INTENTS_FROM_FILE = True
INTENTS_FILE_PATH = "assets/intents.json"
PICKLE_FILE_PATH = "assets/chatbot.pickle"

def generate():

    log.info('Initializing script.')

    log.info('Downloading punkt.')
    nltk.download('punkt')
    stemmer = LancasterStemmer()

    if USE_INTENTS_FROM_FILE:
        log.info(f'Loading intents from file: {INTENTS_FILE_PATH}' )
        with open(INTENTS_FILE_PATH) as file:
            data = json.load(file)
    else:
        #TODO import intents from database
        pass

    log.info('Loading data from intents.')
    #loading data from intent
    words, labels, training, output, docs_x, docs_y = [[] for i in range(6)]
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            t_words = nltk.word_tokenize(pattern)
            words.extend(t_words)
            docs_x.append(t_words)
            docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    log.info('Data loaded from intents.')


    log.info('Generatind data for pickle.')
    output_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        t_words = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            bag.append(1) if w in t_words else bag.append(0)

        output_row = output_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)
        
    training = np.array(training)
    output = np.array(output)

    log.info(f'Writing data to pickle at: {PICKLE_FILE_PATH}')
    with open(PICKLE_FILE_PATH, "wb") as file:
        pickle.dump((words, labels, training, output), file)

    log.info('Finished writing pickle')


if __name__ == '__main__':
    generate()