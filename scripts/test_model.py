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

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])

#global variables
USE_INTENTS_FROM_FILE = True
INTENTS_FILE_PATH = "assets/intents.json"
PICKLE_FILE_PATH = "assets/chatbot.pickle"
JSON_FILE_PATH = "assets/chatbotmodel.json"
HDF5_FILE_PATH = "assets/chatbotmodel.h5"

stemmer = LancasterStemmer()

log.info('Loading data from intent.')

try:
    if USE_INTENTS_FROM_FILE:
        log.info(f'Loading intents from file: {INTENTS_FILE_PATH}' )
        with open(INTENTS_FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        pass
except:
    log.exception('Failed to load intent.')
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


if USE_INTENTS_FROM_FILE:
    log.info(f'Loading intents from file: {INTENTS_FILE_PATH}' )
    with open(INTENTS_FILE_PATH) as file:
        data = json.load(file)
else:
    #TODO import intents from database
    pass

log.info('Testing generated model')


def bag_of_words(input, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(input)
    s_words = [stemmer.stem(w.lower()) for w in s_words]
    for sw in s_words:
        for i, w in enumerate(words):
            if w == sw:
                bag[i] = 1
    
    return np.array(bag)

def predict(txt_input):
    try:
        ct = bag_of_words(txt_input, words)
        ct_array = [ct]
        ct_array = np.array(ct_array)
        
        if np.all((ct_array == 0)):
            return None
            
        result = chatbot_model.predict(ct_array[0:1])
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[0][result_index] > 0.7:
            log.info(f'Prediction score for {txt_input} is {result[0][result_index]}')
            for tg in data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            
            return random.choice(responses)
        else:
            return None
    except:
        log.exception('Failed to predict value')

def test():
    test_inputs = [
        'hi', 'hello', 'bye bye', 'bye', 'what is your name', 'what can i call you', 
        'what do you have to eat?', 'can i see the menu?', 'are you open?', 'what time do you open',
        'how old are you?', 'what is your age?', 'how are you doing?']
    random.shuffle(test_inputs)

    log.info(f'Starting tests using the following dictionary of words: {test_inputs}')
    for i in test_inputs:
        log.info(f'Testing with word: "{i}"')
        result = predict(i)
        if result is None:
            log.info(f'Failed to find a match for: "{i}"')
        else:
            log.info(f'[!] Predicted response for "{i}": "{result}"')
        log.info("-"*20)

if __name__ == '__main__':
    test()