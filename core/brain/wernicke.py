#!/usr/bin/env python
import os
import logging as log
import numpy as np
import nltk
import pickle
import json
import random
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.stem import RSLPStemmer
from dotenv import load_dotenv
from tensorflow.python.keras.models import model_from_json
import json
from datetime import datetime
from core.brain.temporal_lobe import TemporalLobe

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])
load_dotenv()

LANGUAGE = os.getenv("LANGUAGE")

#global variables
USE_INTENTS_FROM_FILE = False
if LANGUAGE == "portuguese":
    INTENTS_FILE_PATH = "assets/intents-portuguese.json"
else:
    INTENTS_FILE_PATH = "assets/intents.json"
PICKLE_FILE_PATH = "assets/chatbot.pickle"
JSON_FILE_PATH = "assets/chatbotmodel.json"
HDF5_FILE_PATH = "assets/chatbotmodel.h5"

"""
Wernicke's Area is the part of the brain responsible for language comprehension
"""

class Wernicke:

    def __init__(self):
        self.chatbot_model = None
        self.data = None
        self.words = []
        self.labels = []
        self.stop_words = stopwords.words(LANGUAGE)
        self.temporal_lobe = TemporalLobe()
        if LANGUAGE == "portuguese":
            self.stemmer = RSLPStemmer()
        else:
            self.stemmer = LancasterStemmer()

    def load_intents(self):
        try:
            if USE_INTENTS_FROM_FILE:
                log.info(f'Loading intents from file: {INTENTS_FILE_PATH}' )
                with open(INTENTS_FILE_PATH, 'r') as file:
                    self.data = json.load(file)
            else:
                log.info('Loading intents from MONGO DB')
                try:
                    self.data = self.temporal_lobe.retrieve_intents()
                except:
                    log.exception('Failed to load intents from MONGO DB')
                    exit()
        except:
            log.exception('Failed to load intent.')
            exit()

    def load_model(self):
        log.info('Loading model from pickle.')
        try:
            with open(JSON_FILE_PATH, 'r') as file:
                self.chatbot_model = model_from_json(file.read())
            self.chatbot_model.load_weights(HDF5_FILE_PATH)
            log.info('Loaded model from file.')
        except:
            log.exception('Failed to load model.')
            exit()

        log.info('Loading data from pickle.')
        try:
            with open(PICKLE_FILE_PATH, 'rb') as file:
                self.words, self.labels, _, _ = pickle.load(file)
            log.info('Loaded data from pickle.')
        except:
            log.exception('Failed to load pickle.')
            exit()
    

    def load(self):
        self.load_intents()
        self.load_model()

    def bag_of_words(self, input):
        bag = [0 for _ in range(len(self.words))]
        s_words = nltk.word_tokenize(input)
        s_words = [w for w in s_words if not w.lower() in self.stop_words]
        s_words = [self.stemmer.stem(w.lower()) for w in s_words]
        for sw in s_words:
            for i, w in enumerate(self.words):
                if w == sw:
                    bag[i] = 1
        
        return np.array(bag)


    def predict(self, txt_input):
        if self.chatbot_model is None:
            self.load()

        try:
            tag = None
            score = None
            response = None
            ct = self.bag_of_words(txt_input)
            ct_array = [ct]
            ct_array = np.array(ct_array)
            
            if np.all((ct_array == 0)):
                return None
                
            result = self.chatbot_model.predict(ct_array[0:1])
            result_index = np.argmax(result)
            tag = self.labels[result_index]

            score = result[0][result_index]
            
            if score > 0.7:
                log.info(f'Prediction for "{txt_input}" returned label "{tag}" with score {score}')
                for tg in self.data['intents']:
                    if tg['tag'] == tag:
                        response = random.choice(tg['responses'])
                
                return tag, score, response
            else:
                log.info(f'Not able to predict a value to: "{txt_input}"')
                return None
        except:
            
            log.exception('Failed to predict value')
            return None
