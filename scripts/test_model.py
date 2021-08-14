#!/usr/bin/env python
import os
import logging as log
import numpy as np
import nltk
import pickle
import json
import random
from nltk.stem import LancasterStemmer
from tensorflow.python.keras.models import model_from_json
from core.connection.mongodb import MongoDB

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])

#global variables
USE_INTENTS_FROM_FILE = False
INTENTS_FILE_PATH = "assets/intents.json"
TESTINPUTS_FILE_PATH = "assets/test_inputs.json"
PICKLE_FILE_PATH = "assets/chatbot.pickle"
JSON_FILE_PATH = "assets/chatbotmodel.json"
HDF5_FILE_PATH = "assets/chatbotmodel.h5"

stemmer = LancasterStemmer()

def load_data():
    
    log.info('Loading data from intent.')

    try:
        if USE_INTENTS_FROM_FILE:
            log.info(f'Loading intents from file: {INTENTS_FILE_PATH}' )
            with open(INTENTS_FILE_PATH, 'r') as file:
                data = json.load(file)
        else:
            log.info('Loading intents from MONGO DB')
            try:
                db = MongoDB()
                data = {'intents': list(db.query('lisa', 'chatbot-intents', {}))}
            except:
                log.exception('Failed to load intents from MONGO DB')
                exit()
    except:
        log.exception('Failed to load intent.')
        exit()

    log.info('Loading data for tests.')

    try:
        if USE_INTENTS_FROM_FILE:
            log.info(f'Loading intents from file: {TESTINPUTS_FILE_PATH}' )
            with open(TESTINPUTS_FILE_PATH, 'r') as file:
                test_inputs = json.load(file)["inputs"]
        else:
            log.info('Loading test inputs from MONGO DB')
            try:
                db = MongoDB()
                test_inputs = list(db.query('lisa', 'chatbot-testdata', {}))
                print(test_inputs)
            except:
                log.exception('Failed to load test inputs from MONGO DB')
                exit()
    except:
        log.exception('Failed to load test inputs.')
        exit()

    log.info('Loading generated model.')
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            chatbot_model = model_from_json(file.read())
        chatbot_model.load_weights(HDF5_FILE_PATH)
        log.info('Loaded model from file.')
    except:
        log.exception('Failed to load model.')
        exit()

    log.info('Loading data from pickle.')
    try:
        with open(PICKLE_FILE_PATH, 'rb') as file:
            words, labels, training, output = pickle.load(file)
        log.info('Loaded data from pickle.')
    except:
        log.exception('Failed to load pickle.')
        exit()

    return data, test_inputs, chatbot_model, words, labels, training, output

def bag_of_words(input, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(input)
    s_words = [stemmer.stem(w.lower()) for w in s_words]
    for sw in s_words:
        for i, w in enumerate(words):
            if w == sw:
                bag[i] = 1
    
    return np.array(bag)

def predict(chatbot_model, txt_input, data, words, labels):
    try:
        ct = bag_of_words(txt_input, words)
        ct_array = [ct]
        ct_array = np.array(ct_array)
        
        if np.all((ct_array == 0)):
            return None, None
            
        result = chatbot_model.predict(ct_array[0:1])
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[0][result_index] > 0.7:
            log.info(f'Prediction score for {txt_input} is {result[0][result_index]}')
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            
            return tag, random.choice(responses)
        else:
            return None, None
    except:
        log.exception('Failed to predict value')

def test():
    log.info('Testing generated model')
    data, tagged_inputs, chatbot_model, words, labels, training, output = load_data()
    
    success_count = 0
    word_count = 0
    for i in tagged_inputs:
        label = i["tag"]
        txt_input_list = i["inputs"]

        log.info(f'Starting tests using the following dictionary of words for label "{label}": {txt_input}')

        for txt_input in txt_input_list:
            word_count += 1
            log.info(f'Testing with word: "{txt_input}"')
            tag, result = predict(chatbot_model, txt_input, data, words, labels)
            if result is None:
                log.info(f'Failed to find a match for: "{txt_input}"')
            else:
                log.info(f'[!] Predicted response for "{txt_input}": "{result}"')
                if label == tag:
                    log.info(f'[!] Predicted tag for "{txt_input}" matches expected result: {label}')
                    success_count += 1

            log.info("-"*20)

    log.info(f'This model predicted responses for {success_count} out of {word_count} inputs.')

if __name__ == '__main__':
    test()